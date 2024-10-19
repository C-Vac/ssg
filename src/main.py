import sys
import os
from utils import publish_static_content, generate_html_content
from contextlib import redirect_stdout

DEBUG_LOG_PATH = "debug_log.txt"

if __name__ == "__main__":
    print("--- START: main.py")

    with open(DEBUG_LOG_PATH, 'w') as f:
        with redirect_stdout(f):
            generate_html_content()
            publish_static_content()

    print("--- END: main.py exited successfully. Program execution log: " + DEBUG_LOG_PATH)
