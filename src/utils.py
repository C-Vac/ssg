# utils.py

from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType


def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)  # we have the blocks
    html_nodes = []

    for block in blocks: # Process the block into an HTMLNode
        node = block_to_html_node(block)
        html_nodes.append(node)

    doc_node = ParentNode(children=html_nodes, tag="div")
    return doc_node

def block_to_html_node(block):
    t = block_to_block_type(block)
    
    match t:
        case "heading":
            pass
        case "code":
            pass
        case "quote":
            pass
        case "unordered_list":
            pass
        case "ordered_list":
            pass
        case "paragraph":
            pass
        case _:
            raise Exception(f"Markdown format could not be identified for block: {block}")

    return HTMLNode()

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


def block_to_block_type(block):
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
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"
    if all(line.startswith(">") for line in lines):
        return "quote"
    if all(line.startswith(("* ", "- ")) for line in lines):
        return "unordered_list"
    if all(line.startswith(str(i + 1) + ". ") for i, line in enumerate(lines)):
        return "ordered_list"
    return "paragraph"
