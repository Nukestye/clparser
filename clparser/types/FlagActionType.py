from enum import Enum


class FlagActionType(Enum):
    # Can be either True or False, cannot be both
    # Set: 0 or 1
    BOOL = 1
    # Must only be numbers, any length
    # Set: 0 - 9
    NUMERICAL = 2
    # Must only be characters, no numbers are allowed
    # Set: A - Z, a - z
    NON_NUMERICAL = 3
    # Can be both numerical and non-numerical, also includes special characters
    # Set: 0 - 7, A - Z, a - z
    STRING = 4
