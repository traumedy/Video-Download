#!/usr/bin/env python3

"""utils.py - Utility functions
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"


def value_to_bool(value):
    """Helper function to convert QSettings.value() to bool

    Returns:
        bool: Evaluated bool value
    """
    return value.lower() == 'true'\
        if isinstance(value, str)\
        else bool(value)
