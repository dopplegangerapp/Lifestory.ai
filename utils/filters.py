from datetime import datetime

def timestamp_to_date(timestamp):
    """Convert a Unix timestamp to a formatted date string."""
    if not timestamp:
        return "Unknown date"
    
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%B %d, %Y")
    except (ValueError, TypeError):
        return "Invalid date" 