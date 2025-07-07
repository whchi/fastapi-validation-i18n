"""
Compatibility layer for pydantic v1 and v2 auto-detection.
"""
import sys
from typing import Any, Dict, List, Type, Union

# Store pydantic version information
_pydantic_version: str = ""
_is_pydantic_v2: bool = False

def _detect_pydantic_version() -> None:
    """Detect the pydantic version and set global variables."""
    global _pydantic_version, _is_pydantic_v2
    
    try:
        import pydantic
        _pydantic_version = pydantic.__version__
        # Check if it's v2 by looking for v2-specific features
        _is_pydantic_v2 = hasattr(pydantic, 'field_validator') and hasattr(pydantic, 'Field')
        
        # Double-check with version string
        if _pydantic_version.startswith('2.'):
            _is_pydantic_v2 = True
        elif _pydantic_version.startswith('1.'):
            _is_pydantic_v2 = False
    except ImportError:
        raise ImportError("pydantic is required but not installed")

# Detect version on module import
_detect_pydantic_version()

def is_pydantic_v2() -> bool:
    """Return True if pydantic v2 is being used."""
    return _is_pydantic_v2

def get_pydantic_version() -> str:
    """Return the pydantic version string."""
    return _pydantic_version

def get_validation_error_class() -> Type[Exception]:
    """Return the appropriate ValidationError class for the pydantic version."""
    if _is_pydantic_v2:
        try:
            from pydantic_core import ValidationError
            return ValidationError
        except ImportError:
            # Fallback to pydantic.ValidationError if pydantic_core is not available
            from pydantic import ValidationError
            return ValidationError
    else:
        from pydantic import ValidationError
        return ValidationError

def get_all_validation_error_classes() -> List[Type[Exception]]:
    """Return all ValidationError classes that might be used."""
    errors = []
    seen_classes = set()
    
    # Always include pydantic.ValidationError
    try:
        from pydantic import ValidationError
        if ValidationError not in seen_classes:
            errors.append(ValidationError)
            seen_classes.add(ValidationError)
    except ImportError:
        pass
    
    # For v2, also include pydantic_core.ValidationError
    if _is_pydantic_v2:
        try:
            from pydantic_core import ValidationError as CoreValidationError
            if CoreValidationError not in seen_classes:
                errors.append(CoreValidationError)
                seen_classes.add(CoreValidationError)
        except ImportError:
            pass
    
    return errors

def get_field_validator():
    """Return the appropriate field validator decorator for the pydantic version."""
    if _is_pydantic_v2:
        from pydantic import field_validator
        return field_validator
    else:
        from pydantic import validator
        return validator

def get_field_class():
    """Return the appropriate Field class for the pydantic version."""
    if _is_pydantic_v2:
        from pydantic import Field
        return Field
    else:
        from pydantic.fields import Field
        return Field

__all__ = [
    'is_pydantic_v2', 
    'get_pydantic_version', 
    'get_validation_error_class',
    'get_all_validation_error_classes',
    'get_field_validator',
    'get_field_class'
]