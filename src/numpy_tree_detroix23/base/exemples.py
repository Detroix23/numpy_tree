"""
TREE
exemples.py
"""

import numpy
import numpy.typing

import base.tree as tree

def main() -> None:
    print("## EXEMPLES.")
    
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
    t1 = tree.Tree(a1, h1)

    g: tuple[str, ...]

    print(t1)
    g = ("A", "C")
    print("-", g, t1.get(*g))
    g = ("A",)
    print("-", g, t1.get(*g))
    g = ("A", tree.CURRENT)
    print("-", g, t1.get(*g))
    g = (tree.CURRENT,)
    print("-", g, t1.get(*g))
    g = ("C", "A")
    t1.update(34, *g)
    
    print()
    print("-", t1.arrays)
    
    
    print()
    print(t1.string_tree())
    
if __name__ == "__main__":
    main()
