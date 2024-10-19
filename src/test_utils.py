# test_utils.py

import unittest
from utils import *
from htmlnode import *


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
        self.assertEqual(
            block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), "ordered_list"
        )

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph."), "paragraph")
        self.assertEqual(
            block_to_block_type("This is a paragraph.\nWith multiple lines."),
            "paragraph",
        )

    def test_block_to_block_type_empty_block(self):
        self.assertEqual(block_to_block_type(""), "paragraph")


class TestBlockToHTMLNode(unittest.TestCase):

    def test_heading(self):
        # Test cases for headings
        test_cases = [
            ("# Heading 1", "<h1>Heading 1</h1>"),
            ("## Heading 2", "<h2>Heading 2</h2>"),
            (
                "### Heading 3 with some `code` and **bold** text",
                "<h3>Heading 3 with some <code>code</code> and <b>bold</b> text</h3>",
            ),
            (
                "#### Heading 4 [with a link](https://www.google.com)",
                '<h4>Heading 4 <a href="https://www.google.com">with a link</a></h4>',
            ),
            (
                "##### Heading 5 ![and an image](https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png)",
                '<h5>Heading 5 <img src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png" alt="and an image"></h5>',
            ),
            (
                "###### Heading 6 *and some italic*",
                "<h6>Heading 6 <i>and some italic</i></h6>",
            ),
        ]
        for markdown, expected_html in test_cases:
            html_node = block_to_html_node(markdown)
            self.assertEqual(html_node.to_html(), expected_html)

    def test_code(self):
        # Test cases for code blocks
        test_cases = [
            (
                "```\nprint('Hello, world!')\n```",
                "<pre><code class=\"\">print('Hello, world!')\n</code></pre>",
            ),
            (
                "```python\nfor i in range(10):\n    print(i)\n```",
                '<pre><code class="python">for i in range(10):\n    print(i)\n</code></pre>',
            ),
            (
                "```\nThis code block\nhas multiple lines\nand some `backticks` inside.\n```",
                '<pre><code class="">This code block\nhas multiple lines\nand some `backticks` inside.\n</code></pre>',
            ),
            (
                "```\nA code block with\nno newlines at the\nbeginning or end```",
                '<pre><code class="">A code block with\nno newlines at the\nbeginning or end</code></pre>',
            ),
            (
                "```javascript\nfunction greet(name) {\n  console.log(`Hello, ${name}!`);\n}\n```",
                '<pre><code class="javascript">function greet(name) {\n  console.log(`Hello, ${name}!`);\n}\n</code></pre>',
            ),
        ]
        for markdown, expected_html in test_cases:
            html_node = block_to_html_node(markdown)
            self.assertEqual(html_node.to_html(), expected_html)

    def test_quote(self):
        # Test cases for quote blocks
        test_cases = [
            (
                "> This is a quote.",
                "<blockquote><p>This is a quote.</p></blockquote>",
            ),
            (
                "> This is a quote with\n> multiple lines.",
                "<blockquote><p>This is a quote with\nmultiple lines.</p></blockquote>",
            ),
            (
                "> This is a quote with\n> some **bold** and *italic* text.",
                "<blockquote><p>This is a quote with\nsome <b>bold</b> and <i>italic</i> text.</p></blockquote>",
            ),
            (
                "> This is a quote with\n> a [link](https://www.google.com).",
                '<blockquote><p>This is a quote with\na <a href="https://www.google.com">link</a>.</p></blockquote>',
            ),
            (
                "> This is a quote with\n> an ![image](https://www.example.com/image.jpg)",
                '<blockquote><p>This is a quote with\nan <img src="https://www.example.com/image.jpg" alt="image"></p></blockquote>',
            ),
        ]
        for markdown, expected_html in test_cases:
            html_node = block_to_html_node(markdown)
            self.assertEqual(html_node.to_html(), expected_html)

    def test_unordered_list(self):
        # Test cases for unordered lists
        test_cases = [
            ("- Item 1", "<ul><li>Item 1</li></ul>"),
            ("- Item 1\n- Item 2", "<ul><li>Item 1</li><li>Item 2</li></ul>"),
            (
                "- Item 1 with **bold** text\n- Item 2 with *italic* text",
                "<ul><li>Item 1 with <b>bold</b> text</li><li>Item 2 with <i>italic</i> text</li></ul>",
            ),
            (
                "- Item 1 with a [link](https://www.google.com)\n- Item 2 with an ![image](https://www.example.com/image.jpg)",
                '<ul><li>Item 1 with a <a href="https://www.google.com">link</a></li><li>Item 2 with an <img src="https://www.example.com/image.jpg" alt="image"></li></ul>',
            ),
        ]
        for markdown, expected_html in test_cases:
            html_node = block_to_html_node(markdown)
            self.assertEqual(html_node.to_html(), expected_html)

    def test_ordered_list(self):
        # Test cases for ordered lists
        test_cases = [
            ("1. Item 1", "<ul><li>Item 1</li></ul>"),
            ("1. Item 1\n2. Item 2", "<ul><li>Item 1</li><li>Item 2</li></ul>"),
            (
                "1. Item 1 with **bold** text\n2. Item 2 with *italic* text",
                "<ul><li>Item 1 with <b>bold</b> text</li><li>Item 2 with <i>italic</i> text</li></ul>",
            ),
            (
                "1. Item 1 with a [link](https://www.google.com)\n2. Item 2 with an ![image](https://www.example.com/image.jpg)",
                '<ul><li>Item 1 with a <a href="https://www.google.com">link</a></li><li>Item 2 with an <img src="https://www.example.com/image.jpg" alt="image"></li></ul>',
            ),
        ]
        for markdown, expected_html in test_cases:
            html_node = block_to_html_node(markdown)
            self.assertEqual(html_node.to_html(), expected_html)

    def test_paragraph(self):
        # Test cases for paragraphs
        test_cases = [
            ("This is a paragraph.", "<p>This is a paragraph.</p>"),
            (
                "This is a paragraph with\nmultiple lines.",
                "<p>This is a paragraph with\nmultiple lines.</p>",
            ),
            (
                "This is a paragraph with some **bold** and *italic* text.",
                "<p>This is a paragraph with some <b>bold</b> and <i>italic</i> text.</p>",
            ),
            (
                "This is a paragraph with a [link](https://www.google.com).",
                '<p>This is a paragraph with a <a href="https://www.google.com">link</a>.</p>',
            ),
            (
                "This is a paragraph with an ![image](https://www.example.com/image.jpg).",
                '<p>This is a paragraph with an <img src="https://www.example.com/image.jpg" alt="image">.</p>',
            ),
        ]
        for markdown, expected_html in test_cases:
            html_node = block_to_html_node(markdown)
            self.assertEqual(html_node.to_html(), expected_html)


class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_markdown_to_html_node_all_cases(self):
        # The Big Ass Test: Combining all Markdown elements
        markdown = """
# Heading 1 with **bold** and `inline code`

This is a paragraph with *italic* and [a link](https://www.google.com).

> This is a quote with an ![image](https://www.example.com/image.jpg).

- Item 1 in an unordered list
- Item 2 with some **bold** text

1. Item 1 in an ordered list
2. Item 2 with some *italic* text
"""
        expected_html = """
<div><h1>Heading 1 with <b>bold</b> and <code>inline code</code></h1>
<p>This is a paragraph with <i>italic</i> and <a href="https://www.google.com">a link</a>.</p>
<blockquote><p>This is a quote with an <img src="https://www.example.com/image.jpg" alt="image"></p></blockquote>
<ul><li>Item 1 in an unordered list</li>
<li>Item 2 with some <b>bold</b> text</li></ul>
<ul><li>Item 1 in an ordered list</li>
<li>Item 2 with some <i>italic</i> text</li></ul>
</div>
"""
        html_node = markdown_to_html_node(markdown)
        self.maxDiff = None
        self.assertEqual(html_node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()
