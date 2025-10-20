"""
TREE
iterables.py
"""

def last_no_blank(t: tuple[str, ...], origin: str = "Ω") -> str:
    """
    Return last element of tuple `t`, skiping blanks.
    """
    last: str = ""
    index: int = len(t) - 1
    while not last and index >= 0:
        if t[index]:
            last = t[index]
        index -= 1

    if not last:
        last = origin

    return last

def length_no_blank(t: tuple[str, ...]) -> int:
    """
    Count non-`None` element in a tuple `t`.
    """
    length: int = 0
    for element in t:
        if element:
            length += 1

    return length

def headers_combinations(headers: tuple[str, ...], level: int) -> list[tuple[str, ...]]:
    """
    Get all headers combinations.
    Also add the `CURRENT` constant, but only when it ends with it.
    """
    if level <= 1:
        return [(header, ) for header in headers]
    
    combinations: list[tuple[str, ...]] = list()
    
    for h1 in headers:
        for h2 in headers_combinations(headers, level - 1):
            t: tuple[str, ...] = (h1,) + h2
            if end_or_no_blank(t):
                combinations.append(t)

    return combinations

def end_or_no_blank(t: tuple[str, ...]) -> bool:
    """
    Return True if `t` only ends or has no blanks.
    False if blanks at the start, or in the middle.
    """
    index: int = len(t) - 1
    solid: bool = False
    valid: bool = True
    while valid and index >= 0:
        if t[index]:
            solid = True
        if solid and not t[index]:
            valid = False
        index -= 1

    return valid
