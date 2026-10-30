
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def main():
    while True:
        print("\n================================")
        print(" TOY HASH COLLISION STRUCTURE")
        print("================================")
        print("1. Run Simon's Algorithm")
        print("2. Run Classical Collision Search")
        print("3. Compare Both Methods")
        print("4. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            subprocess.run([
                sys.executable,
                str(BASE_DIR / "simon_algorithm.py")
            ])

        elif choice == "2":
            subprocess.run([
                sys.executable,
                str(BASE_DIR / "classical_search.py")
            ])

        elif choice == "3":
            print("\n================================")
            print("       METHOD COMPARISON")
            print("================================")

            print("\n1. Simon's Algorithm")
            print("- Demonstrates hidden-period recovery.")
            print("- Uses equations from measurement outcomes.")
            print("- Your current simon_algorithm.py is a")
            print("  classical demonstration of the logic.")

            print("\n2. Classical Collision Search")
            print("- Searches for matching hash values.")
            print("- Finds two inputs with the same hash.")
            print("- Checks whether their XOR matches")
            print("  the entered hidden period.")

            print("\n3. Key Difference")
            print("- Simon's algorithm uses quantum principles.")
            print("- Classical collision search checks inputs")
            print("  directly to find a collision.")

            print("\nNote: The Python menu simulations run")
            print("on a classical computer.")

        elif choice == "4":
            print("\nThank you for using the project!")
            break

        else:
            print("Invalid choice! Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
