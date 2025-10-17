"""
TREE
tree.py
"""
import numpy
import numpy.typing
from typing import Optional

# Special header to take the actual branch value, and not the next branch.
CURRENT: str = ""

class Tree:
    """
    Define a Tree using numpy.
    Arguments:
        - arrays: numpy.NDarray(dtype=int); Used to store data in numpy arrays.
        - headers: list[Optional[str]]; Give named keys for the index-only numpy arrays.
        `CURRENT` in the list allow to get value of branch that are not in the extremites.
        Don't forget to create value for all branch, and not only the last ones.
    
    Exemple: Current = Crt
        
            Crt A   B
    Crt     1   2   3 
      A     4   5   6
      B     7   8   9
    """
    
    arrays: numpy.typing.NDArray[numpy.int64]
    headers: tuple[str, ...]
    
    def __init__(self, arrays: numpy.typing.NDArray[numpy.int64], headers: tuple[str, ...]) -> None:
        """
        Construct the tree.
        """
        self.arrays = arrays
        headers = (CURRENT,) + headers
        self.headers = headers
    
    def __str__(self) -> str:
        return f"""Tree(
    arrays=(
        size={self.arrays.size}
        ndim={self.arrays.ndim}
        shape={self.arrays.shape}
    ) 
    headers={self.headers}
) """ 
    
    def __repr__(self) -> str:
        return f"Tree(arrays=(size={self.arrays.size} ndim={self.arrays.ndim} \
shape={self.arrays.shape}) headers={self.headers})"
        
    def get(self, *headers: str) -> int:
        """
        Return the value of the three following the given headers.
        """
        indexes: list[int] = list()
        
        if len(headers) > self.arrays.ndim:
            raise IndexError(f"(X) - Too many headers: {len(headers)} {headers}. \n{self}")
        
        for header in headers:
            if header not in self.headers:
                raise KeyError(f"(X) - Header {header} not in the tree's headers ({self.headers})")
            
            indexes.append(self.headers.index(header))
            
        return self.arrays[*indexes]
    
    def update(self, value: int, *headers: str) -> None:
        """
        Update to the `value` the position at `headers`.
        """
        indexes: list[int] = list()
        
        if len(headers) > self.arrays.ndim:
            raise IndexError(f"(X) - Too many headers: {len(headers)} {headers}. \n{self}")
        
        for header in headers:
            if header not in self.headers:
                raise KeyError(f"(X) - Header {header} not in the tree's headers ({self.headers})")
            
            indexes.append(self.headers.index(header))
        
        # print(f"dtype {self.dtype} {repr(self.dtype)} {type(self.dtype)} {self.dtype.__class__}")
               
        try:
            if self.arrays[*indexes].dtype != numpy.int64:
                raise IndexError(f"(X) - Can't update a whole array; update an unique value. \
headers={headers}, result={self.arrays[*indexes]} type={type(self.arrays[*indexes])}")
         
            self.arrays[*indexes] = value

        except Exception as exception:
            print(f"(X) - tree.update: headers={headers}, indexes={indexes}.")
            raise exception
    
    
    def string_tree(
        self, 
        level_in: Optional[int] = None, 
        indent_size: int = 3,
        branch: str = "├─ ",
        vertical: str = "│ ",
        branch_last: str = "└─ ",
    ) -> str:
        """
        Return the string of the tree branch to a certain `level`.
        `None` (default) means all.
        """
        level: int
        if level_in is None:
            level = self.arrays.ndim
        else:
            level = level_in

        combinations: list[tuple[str, ...]] = headers_combinations(self.headers, level)

        tree: list[str] = list()
        indent: str
        last_x: bool

        for headers in combinations:
            last_x = last_no_blank(headers) == self.headers[-1] or last_no_blank(headers) not in self.headers

            indent = " " * (indent_size * length_no_blank(headers))
            
            tree.append(f"{indent}{branch_last if last_x else branch}{last_no_blank(headers)}: {self.get(*headers)}\n")

        return "".join(tree)
    
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


def main() -> None:
    print("# Tree")
    print("## TREE")
    
    a1: numpy.typing.NDArray[numpy.int64] = numpy.array([[
            [1, 2, 3, 4],
            [4, 5, 6, 7],
            [7, 8, 9, 10],
            [10, 11, 12, 13],
        ], [
            [5, 2, 3, 4],
            [4, 5, 6, 7],
            [7, 8, 9, 10],
            [10, 11, 12, 13],
        ], [
            [7, 2, 3, 4],
            [4, 5, 6, 7],
            [7, 8, 9, 10],
            [10, 11, 12, 13],
        ], [
            [7, 2, 3, 4],
            [4, 5, 6, 7],
            [7, 8, 9, 10],
            [10, 11, 12, 13],
        ],
    ], dtype=numpy.int64)
            
    h1: tuple[str, ...] = ("A", "B", "C")
    t1 = Tree(a1, h1)

    g: tuple[str, ...]

    print(t1)
    g = ("A", "C")
    print("-", g, t1.get(*g))
    g = ("A",)
    print("-", g, t1.get(*g))
    g = ("A", CURRENT)
    print("-", g, t1.get(*g))
    g = (CURRENT,)
    print("-", g, t1.get(*g))
    g = ("C", "A")
    t1.update(34, *g)
    
    print()
    print("-", t1.arrays)
    
    
    print()
    print(t1.string_tree())
    
    
if __name__ == "__main__":
    main()
    
    