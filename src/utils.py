# utils.py

import re
import os
import shutil
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode


def extract_title(markdown: str):
    lines = markdown.splitlines()
    heading = lines[0]
    if heading.startswith("# "):
        return heading.strip("#").strip()
    raise Exception("!-- Failed: MD file must begin with h1.")


def publish_static_content():
    public_root = "public"
    static_root = "static"

    print(f"\n---Publishing contents of '{static_root}' to '{public_root}'.---\n")

    def copy_directory(static_dir):
        nonlocal public_root
        files_copied = 0

        def copy_file(files, public_dir):
            """
            Copies one file to a target directory recursively from a list of files.

            Args:
                files (list): Strings of file paths of files to copy
                public_dir (str): The directory where files will be copied to
            """
            nonlocal files_copied
            nonlocal static_dir

            if len(files) < 1:
                print(f"\t> Copied {files_copied} files to {public_dir}.")
                return

            filename = files.pop()
            # Extract the relative path within the static directory
            file_path = os.path.join(static_dir, filename)
            relative_path = os.path.relpath(file_path, static_root)
            new_path = os.path.join(public_root, relative_path)

            # Copy the file to the new location
            shutil.copy(file_path, new_path)
            print(f"\t\t+ Copied {file_path} to {new_path}.")

            files_copied += 1
            copy_file(files, public_dir)  # Repeats until the list of files is empty

        print(f"> Copying files in '{static_dir}'.")

        public_dir = ""  # Root directory
        if not static_dir == static_root:
            relative_path = os.path.relpath(static_dir, static_root)
            public_dir = os.path.join(public_root, relative_path)
            # Create directory in public matching static path
            if not os.path.exists(public_dir):
                os.mkdir(public_dir)
                print(f"\t\t+ Created dir '{public_dir}'.")

        # Build list of files in the current directory
        file_paths = []
        with os.scandir(static_dir) as contents:
            for file in contents:
                if file.is_file():
                    file_paths.append(file.name)
                elif file.is_dir():
                    copy_directory(file.path)

        # Start copying
        copy_file(file_paths, public_dir)

    if not os.path.exists(static_root):
        raise FileNotFoundError(f"!-- No directory found at '{static_root}'!")
    if os.path.exists(public_root):
        for filename in os.listdir(public_root):
            filepath = os.path.join(public_root, filename)
            try:
                if os.path.isfile(filepath) or os.path.islink(filepath):
                    os.unlink(filepath)
                elif os.path.isdir(filepath):
                    shutil.rmtree(filepath)
            except Exception as e:
                print(f"Failed to delete {filepath}. Reason: {e}")
        print("- Emptied '/public' directory.")

    copy_directory(static_root)
    print("\n--- Done. Pages are ready to serve. ---\n")


def generate_static_content():
    """
    Reads the contents of the 'content' directory, then creates directories and generates html files in 'static' for each markdown file found in each subdirectory and in the root of 'content'.
    """
    with os.scandir("content") as files:
        for dir_entry in files:
            target_path = ""
            html_path = ""

            # Process root index.md file
            if dir_entry.is_file() and dir_entry.name.endswith(".md"):
                target_path = "content/index.md"
                html_path = "static/index.html"

            # Process content file in subdir
            elif not dir_entry.is_file():
                with os.scandir(dir_entry.path) as pages:
                    page_paths = []
                    for entry in pages:
                        page_paths.append(entry.path)
                    if not len(page_paths) == 1:
                        print(
                            f"!-- Must be exactly one file per subdirectory in 'content/': "
                            + dir_entry.path
                        )
                        break
                    md_file = page_paths[0]
                    if not md_file.endswith(".md"):
                        print("!-- Content must be a '.md' file: " + md_file)
                        break

                    target_path = md_file
                    relative_path = os.path.relpath(md_file, "content")
                    # eg. "page_directory/page_content.md"
                    head, tail = os.path.split(relative_path)
                    # eg. ("page_directory/", "page_content.md")

                    # NOTE: This names all docs as "index.html"
                    html_path = os.path.join("static/", head, "index.html")
                    # For custom named html documents:
                    # html_path = os.path.join("static/", head, tail.strip(".md") + ".html")
                    # eg. "static/page_directory/page_content.html"
                    new_dir = os.path.dirname(html_path)

                    # Make sure directory exists
                    if not os.path.exists(new_dir):
                        os.mkdir(new_dir)

            if target_path == "":
                print(
                    "!!! Something went wrong while getting the target path to convert the MD file to HTML. (This should literally never happen.)"
                )
            html = generate_html_document(target_path)

            # Create new html file or overwrite the existing file
            with open(html_path, "w") as html_file:
                html_file.write(html)


def generate_html_document(md_file):
    """
    Converts a Markdown file to an HTML document string using a template.

    Args:
        markdown_file (str): The path to the Markdown file.

    Returns:
        html: String containing full HTML text.
    """

    template_path = "template.html"
    template = ""

    try:
        print(f"> Creating HTML doc from '{md_file}' and template: {template_path}")

        with open(template_path, "r") as f:
            template = f.read()

        with open(md_file, "r") as f:
            md_text = f.read()

        lines = md_text.splitlines()
        page_title = extract_title(lines[0])
        content_text = "\n".join(lines)

        html_node = markdown_to_html_node(content_text)

        head, tail = os.path.split(md_file)
        stylename = tail[:-3]

        base_path = ""
        if head == "content":
            base_path = ""
        else:
            base_path = os.path.relpath(head, "content") + "/"

        content = html_node.to_html()
        html = fill_template(page_title, content, base_path, stylename, template)

        print(f"\t+ Success.")
        return html

    except Exception as e:
        print(f"!-- Error converting Markdown to HTML: {e}")


def fill_template(title, content, base, style, template: str):
    filled = template.replace("{{ Title }}", title)
    filled = filled.replace("{{ Content }}", content)
    filled = filled.replace("{{ Base }}", base)
    filled = filled.replace("{{ Style }}", style)
    return filled


def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)  # we have the blocks
    html_nodes = []

    for block in blocks:  # Process each block into an HTMLNode
        node = block_to_html_node(block)
        html_nodes.append(node)

    # Assemble the Master Node
    doc_node = ParentNode(children=html_nodes, tag="div")
    return doc_node


def block_to_html_node(block: str):

    def text_to_children(text: str):
        """
        Creates HTMLNodes from markdown text.

        Args:
            text (str): The text to process.

        Returns:
            list: A list of LeafNode objects representing the HTML text.
        """
        text_nodes = TextNode.from_markdown(text)
        children = []
        for node in text_nodes:
            children.append(HTMLNode.text_node_to_html_node(node))
        return children

    def extract_heading(heading_block: str):
        """
        Removes markdown heading from the string and returns the HTML tag and the heading text.

        Args:
            text (str):

        Raises:
            Exception: If input text is not a proper md heading.

        Returns:
            tuple (str, str): Heading level and the heading text.
        """
        level = 0
        for char in heading_block:
            if char == "#":
                level += 1
            elif char == " " and level <= 6:
                children = text_to_children(heading_block[level + 1 :])
                heading_tag = f"h{level}"
                return ParentNode(tag=heading_tag, children=children)
            else:
                raise Exception(f"Malformed heading: {heading_block}")

    def extract_code(code_block: str):
        pattern = r"```([a-z]*)\n(.*?)```"  # Capture code language and code
        match = re.match(pattern, code_block, re.DOTALL)
        if match:
            code_language = match.group(1)  # Extract the code language
            code_text = match.group(2)  # Extract the code
            code_node = ParentNode(
                tag="pre",
                children=[
                    LeafNode(
                        tag="code", value=code_text, props={"class": code_language}
                    )
                ],
            )
            return code_node
        else:
            raise Exception(f"Malformed code block: {code_block}")

    def extract_quote(quote_block: str):
        lines = quote_block.split("\n")
        new_lines = []
        new_block = ""
        if len(lines) == 1:
            new_block = quote_block[2:]
        else:
            for line in lines:
                new_lines.append(line[2:])
            new_block = "\n".join(new_lines)

        children = text_to_children(new_block)
        paragraph_node = ParentNode(tag="p", children=children)
        # return ParentNode(tag="blockquote", children=[paragraph_node])
        return ParentNode(tag="blockquote", children=children)

    def extract_unordered_list(ul_block: str):
        lines = ul_block.split("\n")
        line_nodes = []
        for item in lines:
            new_item = item[2:].strip()
            item_parts_nodes = text_to_children(new_item)
            line_nodes.append(ParentNode(tag="li", children=item_parts_nodes))
        return ParentNode(tag="ul", children=line_nodes)

    def extract_ordered_list(ol_block: str):
        lines = ol_block.split("\n")
        line_nodes = []
        for item in lines:
            new_item = item.split(".", 1)[1].strip()
            item_parts_nodes = text_to_children(new_item)
            line_nodes.append(ParentNode(tag="li", children=item_parts_nodes))
        return ParentNode(tag="ol", children=line_nodes)

    match block_to_block_type(block):
        case "heading":
            return extract_heading(block)
        case "code":
            return extract_code(block)
        case "quote":
            return extract_quote(block)
        case "unordered_list":
            return extract_unordered_list(block)
        case "ordered_list":
            return extract_ordered_list(block)
        case "paragraph":
            return ParentNode(tag="p", children=text_to_children(block))
        case _:
            raise Exception(
                f"Markdown format could not be identified for block: {block}"
            )


def markdown_to_blocks(markdown: str):
    """
    Splits a Markdown string into blocks based on empty lines.

    Args:
        markdown (str): The Markdown string to split.

    Returns:
        list: A list of strings, where each string represents a block of Markdown text.

    Examples:
        >>> markdown = "This is a block.\n\nThis is another block."
        >>> markdown_to_blocks(markdown)
        ['This is a block.', 'This is another block.']
    """
    blocks = []
    lines = markdown.split("\n")

    block = ""
    for line in lines:
        if line.strip("\n") == "":
            if block == "":
                continue
            blocks.append(block.strip())
            print(f"---DEBUG--- \n\tBlock: {block}")
            block = ""
        else:
            block += line.strip() + "\n"
    if block:
        blocks.append(block.rstrip())
    return blocks


def block_to_block_type(block: str):
    """
    Determines the type of a Markdown block.

    Args:
        block (str): The Markdown block to analyze.

    Returns:
        str: The type of the block, which can be one of the following:
            - "heading"
            - "code"
            - "quote"
            - "unordered_list"
            - "ordered_list"
            - "paragraph"

    Examples:
        >>> block_to_block_type("# Heading")
        'heading'
        >>> block_to_block_type("```\nCode block\n```")
        'code'
        >>> block_to_block_type("> Quote")
        'quote'
        >>> block_to_block_type("- Item 1\n- Item 2")
        'unordered_list'
        >>> block_to_block_type("1. Item 1\n2. Item 2")
        'ordered_list'
        >>> block_to_block_type("This is a paragraph.")
        'paragraph'
    """
    lines = block.splitlines()
    if len(lines) == 0:
        return "paragraph"
    if lines[0].startswith("#"):
        return "heading"
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return "code"
    if all(line.startswith(">") for line in lines):
        return "quote"
    if all(line.startswith(("* ", "- ", "+")) for line in lines):
        return "unordered_list"
    if all(line.startswith(str(i + 1) + ". ") for i, line in enumerate(lines)):
        return "ordered_list"
    return "paragraph"


def analyze_paths(filepath, dirpath):
    """Analyzes and prints various path manipulations.

    Args:
        filepath (str): The path to a file.
        dirpath (str): The path to a directory.
    """

    path_data = {
        "filepath": filepath,
        "dirpath": dirpath,
        "--FUNC--": "--RETURN--",
        "filename": os.path.basename(filepath),
        "split_str": filepath.split(os.sep),
        "split_os": os.path.split(filepath),
        "dirname": os.path.dirname(filepath),
        "relative_file": os.path.relpath(filepath, dirpath),
        "relative_dir": os.path.relpath(dirpath, filepath),
    }
    for key, value in path_data.items():
        print(f"{key}:\t{value}")
