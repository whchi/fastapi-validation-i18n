#!/usr/bin/env python3
"""
Test script to verify translation functionality with auto-detection.
"""
import sys
from pathlib import Path

# Add the package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi_validation_i18n import Translator
from fastapi_validation_i18n._helpers import translate_errors
from fastapi_validation_i18n.compat import get_field_class, get_all_validation_error_classes
from pydantic import BaseModel

def test_translation_with_auto_detection():
    """Test that translation works with auto-detected validation errors."""
    print("Testing translation with auto-detection...")
    
    Field = get_field_class()
    
    class TestModel(BaseModel):
        name: str = Field(max_length=5)
        age: int = Field(ge=0)
    
    # Create translator
    translator = Translator('en-US', locale_path=str(Path.cwd()) + '/tests/locale')
    
    # Generate validation errors
    try:
        TestModel(name="this_is_way_too_long", age=-1)
    except Exception as e:
        # Check that it's one of our expected error types
        expected_types = get_all_validation_error_classes()
        if any(isinstance(e, error_type) for error_type in expected_types):
            print(f"✓ Caught expected validation error: {type(e).__name__}")
            
            # Test translation
            try:
                errors = e.errors()
                print(f"✓ Got {len(errors)} validation errors")
                
                # Translate the errors
                translated_errors = list(translate_errors(translator, errors))
                print(f"✓ Translated {len(translated_errors)} errors")
                
                for error in translated_errors:
                    print(f"  - {error['type']}: {error['msg']}")
                    
            except Exception as translation_error:
                print(f"✗ Translation failed: {translation_error}")
        else:
            print(f"✗ Unexpected error type: {type(e)}")
    
    print("✓ Translation test completed!")

if __name__ == "__main__":
    test_translation_with_auto_detection()