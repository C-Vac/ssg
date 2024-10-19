# utils.py

import re
import os
import shutil
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode

def publish_static_content():
    public_root = "./public/"
    static_root = "./static"

    def copy_files(static_path):
        nonlocal public_root

        def copy_file(files):
            nonlocal log_string
            files_copied = 0

            if len(files) < 1:
                log_string = f"Finished copying {files_copied} files to /public."
                return
            filepath = paths_list.pop()
            new_path = os.path.join(public_root, filepath)
            shutil.copy(filepath, new_path)
            print(f"Copied {filepath} to {new_path}.")
            files_copied += 1
            copy_file()

        paths_list = []
        with os.scandir(static_path) as contents:
            for file in contents:
                if file.is_file():
                    paths_list.append(file)
                elif file.is_dir():
                    dir_path = os.path.join(static_path, file)
                    print(f"Adding files in {dir_path} to be copied.")
                    copy_files(dir_path)
        log_string = ""
        copy_file()
        print(log_string)

    if not os.path.exists(static_root):
        os.mkdir(static_root)
    if not os.path.exists(public_root):
        shutil.rmtree(public_root)
        print("Deleted public dir and contents")
    os.mkdir(public_root)
    print("Created empty public directory")

    copy_files(static_root)

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
        return ParentNode(tag="blockquote", children=[paragraph_node])

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

def markdown_to_blocks(markdown):
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
            block = ""
        else:
            block += line.strip() + "\n"
    if block:
        blocks.append(block.strip())
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
