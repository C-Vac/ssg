import sys
import os
from utils import markdown_to_html_node, publish_static_content, generate_html_document
from contextlib import redirect_stdout

if __name__ == "__main__":
    print("--- START: main.py")

    # with os.scandir("content") as files:
        
    #     for f in files:
    #         html = ""
    #         rootdir = os.path.relpath(f.path, "content")
    #         print("root dir for file:" + rootdir)
    #         if f.is_file() and f.name.endswith(".md"):
    #             html = generate_html_document(f.name)
    #             new_path = 
    #             with open(f.name, "w") as f:
    #                 f.write(html)
    #         elif not f.is_file():


    with open('debug_log.txt', 'w') as f:
        with redirect_stdout(f):
            publish_static_content()

    print("--- END: main.py exited successfully.")
