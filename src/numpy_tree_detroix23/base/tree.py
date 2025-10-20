"""
TREE
tree.py
"""
import numpy
import numpy.typing
from typing import Optional, Final, Union

from . import iterables

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
        - ignore_item_type: bool; Used in `get` and `update` to not raise when the user sets headers
        that return an array.
        
    Exemple: Current = Crt
        
            Crt A   B
    Crt     1   2   3 
      A     4   5   6
      B     7   8   9
    """
    
    arrays: numpy.typing.NDArray[numpy.int64]
    headers: Final[tuple[str, ...]]
    depth: Final[int]
    ignore_item_type: bool

    def __init__(
        self,
        headers: tuple[str, ...],
        depth: int,
        *,
        default_zeros: bool = True,
    ) -> None:
        """
        Construct a new empty tree.
        """
        headers = (CURRENT,) + headers
        self.headers = headers
        self.depth = depth
        if default_zeros:
            self.arrays = self.zeros()
        self.ignore_item_type = False

    def __str__(self) -> str:
        """
        Return a formatted representation of the tree.
        """
        return f"""Tree(
    arrays=(
        size={self.arrays.size},
        ndim={self.arrays.ndim},
        shape={self.arrays.shape},
    ),
    headers={self.headers},
    depth={self.depth},
) """ 
    
    def __repr__(self) -> str:
        """
        Return a one-line almost compatible `exec` representation.
        """
        return f"Tree(arrays=(size={self.arrays.size}, ndim={self.arrays.ndim}, \
shape={self.arrays.shape}), headers={self.headers}, depth={self.depth})"
    
    def zeros(self) -> numpy.typing.NDArray[numpy.int64]:
        """
        Initialize `depth` 0-full arrays of equal size.
        Size is the length of the headers.
        """
        shape: tuple[int, ...] = tuple(
            len(self.headers) for _ in range(self.depth)
        )
        return numpy.zeros(shape, dtype=numpy.int64)

    @staticmethod
    def from_arrays(
        arrays: numpy.typing.NDArray[numpy.int64], 
        headers: tuple[str, ...],
    ) -> 'Tree':
        """
        Construct a new tree from a given existing array.
        """
        new = Tree(
            headers, 
            arrays.ndim,
            default_zeros=False,
        )
        new.arrays = arrays

        return new

    def map_headers(self, *headers: str) -> list[int]:
        """
        Return a `list[int]` of the index of the given headers.
        """
        indexes: list[int] = list()
        
        if len(headers) > self.arrays.ndim:
            raise IndexError(f"(X) - Too many headers: {len(headers)} {headers}. \n{self}")
        
        for header in headers:
            if header not in self.headers:
                raise KeyError(f"(X) - Header {header} not in the tree's headers ({self.headers})")
            
            indexes.append(self.headers.index(header))

        return indexes

    def get_any(self, *headers: str) -> Union[int, numpy.typing.NDArray[numpy.int64]]:
        """
        Return the value of the `Tree`, following the given `headers`.
        Can return both an `int`, or an array.
        """
        if not iterables.end_or_no_blank(headers):
            raise KeyError(f"(X) - Calls of `CURRENT` are allowed only in end of the headers. {headers}.")

        
        indexes: list[int] = self.map_headers(*complete_headers(headers, self.depth))

        return self.arrays[*indexes]
    
    def get(self, *headers: str) -> int:
        """
        Return the value of the `Tree`, following the given `headers`.
        Can return only an `int`, else raise an IndexError.
        """
        if not iterables.end_or_no_blank(headers):
            raise KeyError(f"(X) - Calls of `CURRENT` are allowed only in end of the headers. {headers}.")

        indexes: list[int] = self.map_headers(*complete_headers(headers, self.depth))
        
        if (not self.ignore_item_type) and isinstance(self.arrays[*indexes], numpy.ndarray):
                raise IndexError(f"\n(X) - Can't update a whole array; update an unique value. \
headers={headers}, indexes={indexes}, result={self.arrays[*indexes]} type={type(self.arrays[*indexes])}")

        return self.arrays[*indexes]

    def update(self, value: int, *headers: str) -> None:
        """
        Update to the `value` the position at `headers`.    \r
        Must be updating an `int` value.    \r
        Otherwise, if tring to update an array, raise an error. \r 
        """
        indexes: list[int] = self.map_headers(*headers)

        if (not self.ignore_item_type) and isinstance(self.arrays[*indexes], numpy.ndarray):
                raise IndexError(f"\n(X) - Can't update a whole array; update an unique value. \
headers={headers}, indexes={indexes}, result={self.arrays[*indexes]} type={type(self.arrays[*indexes])}")

        try:
            self.arrays[*indexes] = value

        except Exception as exception:
            print(f"\n(X.i) - tree.update: headers={headers}, indexes={indexes}.\n")
            raise exception

        return
    
    def update_any(self, value: int, *headers: str) -> None:
        """
        Update to the `value` the position at `headers`.    \r
        Can update both an `int` or an array without warning.
        """
        indexes: list[int] = self.map_headers(*headers)

        try:
            self.arrays[*indexes] = value

        except Exception as exception:
            print(f"\n(X.i) - tree.update: headers={headers}, indexes={indexes}.\n")
            raise exception

        return
    
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

        tree: list[str] = list()
        indent: str
        last_x: bool

        for headers in iterables.headers_combinations(self.headers, level):
            last_x = (
                iterables.last_no_blank(headers) == self.headers[-1] 
                or iterables.last_no_blank(headers) not in self.headers
            )

            indent = " " * (indent_size * iterables.length_no_blank(headers))
            
            tree.append(
                f"{indent}{branch_last if last_x else branch}{iterables.last_no_blank(headers)}: {self.get(*headers)}\n"
            )

        return "".join(tree)


def complete_headers(headers: tuple[str, ...], length: int) -> tuple[str, ...]:
    """
    If `headers` ends with `CURRENT`:
        - Return an updated tuple with `CURRENT` to reach the `length`.
    """
    completed: tuple[str, ...] = headers

    if headers[-1] == CURRENT:
        completed += tuple(CURRENT for _ in range(length - len(headers)))
    
    return completed

def main() -> None:
    print("## TREE.")
    print("cf. `exemples.py`")

if __name__ == "__main__":
    main()
    
    