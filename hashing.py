import sys
from typing import Union, Tuple
from string import printable as ASCII_TABLE

# NOTE: HashTables in this file use 16 buckets instead of 6 in the examples

sys.set_int_max_str_digits(0) # Disable string conversion length limit in python

def hash_function(value:Union[str, int, float, Tuple]) -> str:
    """Hashes a provided value

    Parameters
    ----------
    value : Union[str, int, float, Tuple]
        The value to hash

    Returns
    -------
    str
        The hash for the value (always 128 characters)
    """
    value = str(value)
    hash = 1
    for character in value:
        hash *= ASCII_TABLE.index(character)

    hash = str(hash)
    if len(hash) < 128:
        for number in range(128-len(hash)):
            if number > 99: # Only single digit values allowed
                number //= 100
            elif number > 9:
                number //=10
            hash += str(number)
    elif len(hash) > 128:
        hash = hash[0:128]
    
    return int(hash)
