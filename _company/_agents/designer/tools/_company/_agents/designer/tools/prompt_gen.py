import os
import sys

# Forwarding wrapper for duplicated path execution
target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, target_dir)
from prompt_gen import generate_prompt

if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "IMF2화_자정의중앙 금융 금고"
    lens = sys.argv[2] if len(sys.argv) > 2 else "35mm"
    lighting = sys.argv[3] if len(sys.argv) > 3 else "야간_시네마틱"
    generate_prompt(title, lens, lighting)
