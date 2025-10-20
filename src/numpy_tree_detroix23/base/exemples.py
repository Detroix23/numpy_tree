"""
TREE
exemples.py
"""

import numpy
import numpy.typing

from . import tree

def main() -> None:
    print("## EXEMPLES.")
    
    print("=> A1")

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
    t1: tree.Tree = tree.Tree.from_arrays(a1, h1)

    g: tuple[str, ...]

    print(t1)
    g = ("A", "C")
    print("-", g, t1.get_any(*g))
    g = ("A",)
    print("-", g, t1.get_any(*g))
    g = ("A", tree.CURRENT)
    print("-", g, t1.get(*g))
    g = (tree.CURRENT,)
    print("-", g, t1.get(*g))
    g = ("C", "A", tree.CURRENT)
    t1.update(34, *g)
    
    print()
    print("-", t1.arrays)
    
    print()
    print(t1.string_tree())
    

    print("=> A2")

    t2 = tree.Tree(("A", "B", "C"), 4)
    print("t2:")
    t2.update(123, "A", "A", "A", tree.CURRENT)
    print(t2)
    print(t2.string_tree())
    l1 = t2.get_any("A", "A", "A")
    print(l1)

if __name__ == "__main__":
    main()

