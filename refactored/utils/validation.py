from typing import Callable, Any


def get_valid_input(prompt: str, validation_func: Callable[[str], bool], error_message: str) -> str:
    """
    Get and validate user input.
    
    Args:
        prompt: Message to display to the user
        validation_func: Function that returns True if input is valid, False otherwise
        error_message: Message to display if validation fails
        
    Returns:
        Validated user input
    """
    while True:
        value = input(prompt).strip()
        if validation_func(value):
            return value
        print(error_message)


def validate_name(name: str) -> bool:
    """
    Validate a name (first or last name).
    
    Args:
        name: Name to validate
        
    Returns:
        True if name is valid, False otherwise
    """
    return len(name) > 1 and name.isalpha()


def validate_number(num_str: str) -> bool:
    """
    Validate that input is a valid number.
    
    Args:
        num_str: String to validate as a number
        
    Returns:
        True if input can be converted to a number, False otherwise
    """
    try:
        float(num_str)
        return True
    except ValueError:
        return False


def validate_positive_number(num_str: str) -> bool:
    """
    Validate that input is a positive number.
    
    Args:
        num_str: String to validate as a positive number
        
    Returns:
        True if input is a valid positive number, False otherwise
    """
    try:
        return float(num_str) > 0
    except ValueError:
        return False


def validate_non_empty(text: str) -> bool:
    """
    Validate that input is not empty.
    
    Args:
        text: String to validate
        
    Returns:
        True if input is not empty, False otherwise
    """
    return len(text.strip()) > 0
