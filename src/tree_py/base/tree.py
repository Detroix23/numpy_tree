"""
TREE
tree.py
"""
import numpy
import numpy.typing
from typing import Optional

import base.iterables as iterables

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

        combinations: list[tuple[str, ...]] = iterables.headers_combinations(self.headers, level)

        tree: list[str] = list()
        indent: str
        last_x: bool

        for headers in combinations:
            last_x = (
                iterables.last_no_blank(headers) == self.headers[-1] 
                or iterables.last_no_blank(headers) not in self.headers
            )

            indent = " " * (indent_size * iterables.length_no_blank(headers))
            
            tree.append(f"{indent}{branch_last if last_x else branch}{iterables.last_no_blank(headers)}: {self.get(*headers)}\n")

        return "".join(tree)



def main() -> None:
    print("## TREE.")
    print("cf. `exemples.py`")

if __name__ == "__main__":
    main()
    
    