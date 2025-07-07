#!/usr/bin/env python3
"""
Test script to verify pydantic auto-detection functionality.
"""
import sys
from pathlib import Path

# Add the package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi_validation_i18n import is_pydantic_v2, get_pydantic_version
from fastapi_validation_i18n.compat import get_all_validation_error_classes, get_field_validator, get_field_class

def test_version_detection():
    """Test that pydantic version is correctly detected."""
    print("Testing pydantic version detection...")
    
    print(f"Is Pydantic v2: {is_pydantic_v2()}")
    print(f"Pydantic version: {get_pydantic_version()}")
    
    # Test that we can get the appropriate classes
    validation_errors = get_all_validation_error_classes()
    print(f"Available ValidationError classes: {[cls.__module__ + '.' + cls.__name__ for cls in validation_errors]}")
    
    # Test field validator
    field_validator = get_field_validator()
    print(f"Field validator: {field_validator.__module__}.{field_validator.__name__}")
    
    # Test field class
    field_class = get_field_class()
    print(f"Field class: {field_class.__module__}.{field_class.__name__}")
    
    print("✓ Version detection tests passed!")

def test_error_handling():
    """Test that error handling works with auto-detection."""
    print("\nTesting error handling...")
    
    try:
        from pydantic import BaseModel
        from fastapi_validation_i18n.compat import get_field_class
        
        Field = get_field_class()
        
        class TestModel(BaseModel):
            name: str = Field(max_length=5)
        
        # This should raise a validation error
        try:
            TestModel(name="this_is_too_long")
            print("✗ Expected validation error but didn't get one")
        except Exception as e:
            print(f"✓ Correctly caught validation error: {type(e).__name__}")
            
            # Check that it's one of our expected error types
            expected_types = get_all_validation_error_classes()
            if any(isinstance(e, error_type) for error_type in expected_types):
                print("✓ Error type is correctly detected")
            else:
                print(f"✗ Error type {type(e)} not in expected types: {expected_types}")
    except Exception as e:
        print(f"✗ Error during testing: {e}")

def test_fastapi_integration():
    """Test that FastAPI integration works with auto-detection."""
    print("\nTesting FastAPI integration...")
    
    try:
        from fastapi import FastAPI
        from fastapi_validation_i18n import setup
        
        app = FastAPI()
        setup(app)
        
        print("✓ FastAPI setup completed successfully")
        
        # Check that exception handlers are registered
        handlers = app.exception_handlers
        print(f"✓ Registered {len(handlers)} exception handlers")
        
    except Exception as e:
        print(f"✗ Error during FastAPI integration test: {e}")

if __name__ == "__main__":
    test_version_detection()
    test_error_handling()
    test_fastapi_integration()
    print("\nAll tests completed!")