import unicodedata
from typing import Dict, List, Any


def get_string_width(s: str) -> int:
    """
    Get the display width of a string, counting emoji and wide characters as 2 spaces.
    
    Args:
        s: String to measure
    
    Returns:
        Display width of the string
    """
    width = 0
    for c in s:
        # East Asian Width property for wide characters
        if unicodedata.east_asian_width(c) in ('F', 'W'):
            width += 2
        else:
            width += 1
    return width


def pad_to_width(s: str, width: int) -> str:
    """
    Pad a string to exact display width, considering emoji and wide character widths.
    
    Args:
        s: String to pad
        width: Desired final display width
    
    Returns:
        Padded string with proper centering
    """
    current_width = get_string_width(s)
    if current_width < width:
        padding = width - current_width
        left_pad = padding // 2
        right_pad = padding - left_pad
        return ' ' * left_pad + s + ' ' * right_pad
    return s


def format_address(addr: str, width: int = 36) -> str:
    """
    Format address to fixed width, centered.
    
    Args:
        addr: Address string to format
        width: Desired display width
        
    Returns:
        Centered and truncated address string
    """
    if len(addr) > width:
        half = width // 2 - 2
        return addr[:half] + "..." + addr[-half:]
    return pad_to_width(addr, width)


def format_address_with_name(addr: str, contacts: List[Dict[str, Any]], 
                            wallets: List[Dict[str, Any]], is_sender: bool = False, 
                            width: int = 50) -> str:
    """
    Format address with contact name or wallet nickname if available.
    For "Network Reward" transactions, uses a special label.
    
    Args:
        addr: Address to format
        contacts: List of contacts to look up names
        wallets: List of wallets to look up nicknames
        is_sender: Whether this address is a sender (for Network Reward handling)
        width: Desired display width
        
    Returns:
        Formatted address string with name/nickname if available
    """
    if addr == "Network Reward" or (is_sender and addr == "Network Reward"):
        return pad_to_width("🏆 Mining Reward", width)
    
    # Check if the address is in contacts
    for contact in contacts:
        if contact.get("address") == addr:
            name = f"{contact['first_name']} {contact['last_name']}"
            addr_display = f"{name} ({addr[:6]}...{addr[-6:]})"
            return pad_to_width(addr_display, width)
    
    # Check if the address is in wallets
    for wallet in wallets:
        if wallet.get("address") == addr:
            name = wallet.get("nickname", "My Wallet")
            addr_display = f"{name} ({addr[:6]}...{addr[-6:]})"
            return pad_to_width(addr_display, width)
    
    # If not found, just display the address
    return format_address(addr, width)


def format_amount(amount: float, width: int = 14) -> str:
    """
    Format amount to fixed width, centered.
    
    Args:
        amount: Amount to format
        width: Desired display width
        
    Returns:
        Centered and formatted amount string
    """
    return pad_to_width(f"{amount:.2f}", width)


def format_timestamp(ts: float, width: int = 21) -> str:
    """
    Format timestamp to fixed width, centered.
    
    Args:
        ts: Timestamp to format
        width: Desired display width
        
    Returns:
        Centered and formatted timestamp string
    """
    from datetime import datetime
    dt = datetime.fromtimestamp(ts)
    return pad_to_width(dt.strftime("%Y-%m-%d %H:%M:%S"), width)


def format_type(tx_type: str, width: int = 12) -> str:
    """
    Format transaction type, centered.
    
    Args:
        tx_type: Transaction type to format
        width: Desired display width
        
    Returns:
        Centered and formatted transaction type string
    """
    return pad_to_width(tx_type, width)


def format_hash(hash_value: str, width: int = 66) -> str:
    """
    Format hash to fixed width.
    
    Args:
        hash_value: Hash value to format
        width: Desired display width
        
    Returns:
        Truncated and formatted hash string
    """
    if len(hash_value) > width:
        half = width // 2 - 2
        return hash_value[:half] + "..." + hash_value[-half:]
    return hash_value
