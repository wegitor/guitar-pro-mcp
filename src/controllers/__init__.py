"""
Controllers for Guitar Pro file management.

This package contains controllers for:
- GuitarProController: Guitar Pro file loading, editing, and manipulation
"""

# Import controllers so they can be imported from the controllers package
from .guitar_pro import GuitarProController

__all__ = ['GuitarProController']
