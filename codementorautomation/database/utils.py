def title_to_snake(title_case: str) -> str:
    """Converts a title case string to snake case."""
    return ''.join(['_' + c.lower() if c.isupper() else c for c in title_case]).lstrip('_')
