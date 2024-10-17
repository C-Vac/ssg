import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_split_nodes_delimiter_basic(self):
        nodes = [TextNode("This is *italic* text", TextType.TEXT)]
        result = TextNode.split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_multiple_delimiters(self):
        nodes = [TextNode("This is *italic* and **bold** text", TextType.TEXT)]
        result = TextNode.split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        result = TextNode.split_nodes_delimiter(result, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_consecutive_delimiters(self):
        nodes = [TextNode("This is ***bold and italic*** text", TextType.TEXT)]
        result = TextNode.split_nodes_delimiter(nodes, "***", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold and italic", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_delimiter_at_beginning_and_end(self):
        nodes = [TextNode("*Italic at the beginning*", TextType.TEXT)]
        result = TextNode.split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("Italic at the beginning", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_multiple_nodes(self):
        nodes = [
            TextNode("This is *italic* text", TextType.TEXT),
            TextNode("This is **bold** text", TextType.TEXT)
        ]
        result = TextNode.split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        result = TextNode.split_nodes_delimiter(result, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_unmatched_delimiter(self):
        nodes = [TextNode("This is *unmatched text", TextType.TEXT)]
        with self.assertRaises(SyntaxError):
            TextNode.split_nodes_delimiter(nodes, "*", TextType.ITALIC)

    def test_split_nodes_delimiter_empty_input(self):
        result = TextNode.split_nodes_delimiter([], "*", TextType.ITALIC)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
