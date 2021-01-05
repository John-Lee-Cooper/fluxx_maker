""" Collection of string processing functions """


def safe_filename(string: str, special: str = "._") -> str:
    """ Return a safe verison of string for a file """

    string = string.strip().lower().replace(" ", "_")
    return "".join([c for c in string if c.isalnum() or c in special])
