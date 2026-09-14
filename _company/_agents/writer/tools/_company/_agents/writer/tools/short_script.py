import os
import sys

# Forwarding wrapper for duplicated path execution
target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, target_dir)
from short_script import generate_short_script

if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "IMF_전날밤의비밀"
    genre = sys.argv[2] if len(sys.argv) > 2 else "타임슬립/What If"
    generate_short_script(title, genre)
