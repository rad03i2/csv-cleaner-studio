"""CSV Cleaner Studio public API."""
from .core import CSVError, CleanOptions, CleanReport, clean_file, clean_text

__version__ = "1.0.0"
__author__ = "Radwan Abdulhadi Ahmed / @rad03i2"

__all__ = ["CSVError", "CleanOptions", "CleanReport", "clean_file", "clean_text"]
