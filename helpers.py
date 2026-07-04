"""
Utility helper functions
"""

import os
from datetime import datetime, timedelta
from typing import Tuple


def format_file_size(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def parse_duration(duration_str: str) -> int:
    """
    Parse duration string to seconds
    
    Args:
        duration_str: Duration string (e.g., "30m", "1h", "30s")
        
    Returns:
        Duration in seconds
    """
    try:
        if duration_str.endswith('s'):
            return int(duration_str[:-1])
        elif duration_str.endswith('m'):
            return int(duration_str[:-1]) * 60
        elif duration_str.endswith('h'):
            return int(duration_str[:-1]) * 3600
        else:
            return int(duration_str)
    except:
        return 3600  # Default 1 hour


def format_duration(seconds: int) -> str:
    """
    Format seconds to human-readable duration
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def format_datetime(dt: datetime) -> str:
    """
    Format datetime object to readable string
    
    Args:
        dt: Datetime object
        
    Returns:
        Formatted datetime string
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_next_run_time(hour: int, minute: int = 0) -> datetime:
    """
    Get next run time for a given hour and minute
    
    Args:
        hour: Hour (0-23)
        minute: Minute (0-59)
        
    Returns:
        Next datetime for the given time
    """
    now = datetime.now()
    next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    if next_run <= now:
        next_run += timedelta(days=1)
    
    return next_run


def ensure_directory(directory: str) -> bool:
    """
    Ensure directory exists, create if needed
    
    Args:
        directory: Directory path
        
    Returns:
        True if successful or already exists
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception:
        return False


def validate_channel_id(channel_id: str) -> bool:
    """
    Validate channel ID format
    
    Args:
        channel_id: Channel ID to validate
        
    Returns:
        True if valid
    """
    return bool(channel_id and isinstance(channel_id, str) and len(channel_id) > 0)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for filesystem compatibility
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename
