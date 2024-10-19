import sys
import os
from utils import publish_static_content, generate_html_document
from contextlib import redirect_stdout

if __name__ == "__main__":
    print("--- START: main.py")

    with open('debug_log.txt', 'w') as f:
        with redirect_stdout(f):
            generate_html_document()
            # publish_static_content()

    print("--- END: main.py exited successfully.")
