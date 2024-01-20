import re

def strip_description_path(url):
    """Remove the /description or /submissions suffix from a leetcode.com url, if present.

    Args:
        url (str): The url to sanitise.

    Returns:
        str: The url without the suffix.
    """
    if url.startswith("https://leetcode.com/problems/"):
        return re.sub(r"/(description|submissions)/?$", "", url)
    else:
        return url
