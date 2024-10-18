# test_utils.py

import unittest
from utils import *

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks_basic(self):
        markdown = "This is a block.\n\nThis is another block."
        expected = ["This is a block.", "This is another block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_multiple_empty_lines(self):
        markdown = "Block 1\n\n\nBlock 2\n\n\n\nBlock 3"
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_leading_and_trailing_empty_lines(self):
        markdown = "\n\nBlock 1\n\nBlock 2\n\n\n"
        expected = ["Block 1", "Block 2"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_no_empty_lines(self):
        markdown = "This is a single block."
        expected = ["This is a single block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_empty_string(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

class TestBlockToBlockType(unittest.TestCase):

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), "heading")
        self.assertEqual(block_to_block_type("## Heading"), "heading")
        self.assertEqual(block_to_block_type("### Heading"), "heading")

    def test_block_to_block_type_code(self):
        self.assertEqual(block_to_block_type("```\nCode block\n```"), "code")
        self.assertEqual(block_to_block_type("```python\nprint('Hello')\n```"), "code")

    def test_block_to_block_type_quote(self):
        self.assertEqual(block_to_block_type("> Quote"), "quote")
        self.assertEqual(block_to_block_type("> Quote 1\n> Quote 2"), "quote")

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), "unordered_list")
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2"), "unordered_list")

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2"), "ordered_list")
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), "ordered_list")

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph."), "paragraph")
        self.assertEqual(block_to_block_type("This is a paragraph.\nWith multiple lines."), "paragraph")

    def test_block_to_block_type_empty_block(self):
        self.assertEqual(block_to_block_type(""), "paragraph")

if __name__ == '__main__':
    unittest.main()
