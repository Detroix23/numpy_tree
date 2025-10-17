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
import base.exemples


def main() -> None:
    print("# Tree")

    base.exemples.main()

if __name__ == "__main__":
    main()
