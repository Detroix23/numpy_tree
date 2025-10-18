"""
TREE
__main__.py
Using numpy to make a regular tree.

─ Ω: 1
   ├─ A: 5
      ├─ A: 4
         ├─ A: 5
         ├─ B: 6
         └─ C: 7
      ├─ B: 7
         ├─ A: 8
         ├─ B: 9
         └─ C: 10
      └─ C: 10
   :
"""
from numpy_tree_detroix23.base import exemples


def main() -> None:
    print("# Tree")

    exemples.main()

if __name__ == "__main__":
    main()
