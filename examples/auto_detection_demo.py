#!/usr/bin/env python3
"""
Example demonstrating the auto-detection feature for pydantic v2.
This example shows how the library automatically detects and handles both
pydantic v1 and v2 without requiring manual configuration.
"""
import sys
from pathlib import Path

# Add the package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from pydantic import BaseModel, ValidationError

# Import the library with auto-detection
from fastapi_validation_i18n import setup, is_pydantic_v2, get_pydantic_version
from fastapi_validation_i18n.compat import get_field_class, get_all_validation_error_classes
from fastapi_validation_i18n._helpers import translate_errors
from fastapi_validation_i18n.translator import Translator

def demo_auto_detection():
    """Demonstrate the auto-detection feature."""
    print("=== FastAPI Validation i18n Auto-Detection Demo ===")
    print(f"Detected Pydantic version: {get_pydantic_version()}")
    print(f"Is Pydantic v2: {is_pydantic_v2()}")
    
    # Get the appropriate Field class automatically
    Field = get_field_class()
    print(f"Using Field class: {Field.__module__}.{Field.__name__}")
    
    # Show all detected ValidationError classes
    error_classes = get_all_validation_error_classes()
    print(f"Detected ValidationError classes: {[cls.__name__ for cls in error_classes]}")
    
    # Create a FastAPI app with auto-detection
    app = FastAPI(title="Auto-Detection Demo")
    
    # Setup the i18n middleware with auto-detection
    setup(app, locale_path='tests/locale')
    print("✓ FastAPI setup completed with auto-detection")
    
    # Create a model using the auto-detected Field class
    class UserModel(BaseModel):
        name: str = Field(max_length=10, min_length=2)
        age: int = Field(ge=0, le=150)
        email: str = Field(pattern=r'^[^@]+@[^@]+\.[^@]+$')
    
    print("\n--- Testing validation error handling ---")
    
    # Test validation with invalid data
    try:
        UserModel(
            name="x",  # Too short
            age=-1,    # Negative age
            email="invalid-email"  # Invalid email format
        )
    except Exception as e:
        print(f"✓ Caught validation error: {type(e).__name__}")
        
        # Verify it's one of our expected error types
        if any(isinstance(e, error_type) for error_type in error_classes):
            print("✓ Error type matches auto-detected classes")
            
            # Test translation
            translator = Translator('en-US', locale_path='tests/locale')
            errors = list(translate_errors(translator, e.errors()))
            print(f"✓ Successfully translated {len(errors)} errors:")
            for error in errors:
                print(f"  - {error['type']}: {error['msg']}")
        else:
            print(f"✗ Error type {type(e)} not in expected classes")
    
    # Test with valid data
    print("\n--- Testing with valid data ---")
    try:
        user = UserModel(
            name="Alice",
            age=25,
            email="alice@example.com"
        )
        print(f"✓ Valid user created: {user.name}, {user.age}, {user.email}")
    except Exception as e:
        print(f"✗ Unexpected error with valid data: {e}")
    
    print("\n✓ Auto-detection demo completed successfully!")

if __name__ == "__main__":
    demo_auto_detection()