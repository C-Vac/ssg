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
        result = TextNode.split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(result, nodes)

    def test_split_nodes_delimiter_empty_input(self):
        result = TextNode.split_nodes_delimiter([], "*", TextType.ITALIC)
        self.assertEqual(result, [])

    def test_extract_markdown_images_basic(self):
        text = "This is an image: ![Alt text](https://example.com/image.jpg)"
        expected = [("Alt text", "https://example.com/image.jpg")]
        self.assertEqual(TextNode._extract_markdown_images(text), expected)

    def test_extract_markdown_images_multiple(self):
        text = "Image 1: ![Alt 1](url1), Image 2: ![Alt 2](url2)"
        expected = [("Alt 1", "url1"), ("Alt 2", "url2")]
        self.assertEqual(TextNode._extract_markdown_images(text), expected)

    def test_extract_markdown_images_no_images(self):
        text = "This text has no images."
        expected = []
        self.assertEqual(TextNode._extract_markdown_images(text), expected)

    def test_extract_markdown_images_empty_text(self):
        text = ""
        expected = []
        self.assertEqual(TextNode._extract_markdown_images(text), expected)

    def test_extract_markdown_links_basic(self):
        text = "This is a link: [Link text](https://example.com)"
        expected = [("Link text", "https://example.com")]
        self.assertEqual(TextNode._extract_markdown_links(text), expected)

    def test_extract_markdown_links_multiple(self):
        text = "Link 1: [Text 1](url1), Link 2: [Text 2](url2)"
        expected = [("Text 1", "url1"), ("Text 2", "url2")]
        self.assertEqual(TextNode._extract_markdown_links(text), expected)

    def test_extract_markdown_links_no_links(self):
        text = "This text has no links."
        expected = []
        self.assertEqual(TextNode._extract_markdown_links(text), expected)

    def test_extract_markdown_links_empty_text(self):
        text = ""
        expected = []
        self.assertEqual(TextNode._extract_markdown_links(text), expected)

    def test_extract_markdown_links_exclude_images(self):
        text = "Link: [Text](url), Image: ![Alt](img_url)"
        expected = [("Text", "url")]  # Should not include the image
        self.assertEqual(TextNode._extract_markdown_links(text), expected)

    def test_split_nodes_images_and_links_basic_image(self):
        nodes = [TextNode("This is an image: ![Alt text](https://example.com/image.jpg)", TextType.TEXT)]
        result = TextNode.split_nodes_images_and_links(nodes)
        expected = [
            TextNode("This is an image: ", TextType.TEXT),
            TextNode("Alt text", TextType.IMAGE, url="https://example.com/image.jpg")  # Updated expected result
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_images_and_links_basic_link(self):
        nodes = [TextNode("This is a link: [Link text](https://example.com)", TextType.TEXT)]
        result = TextNode.split_nodes_images_and_links(nodes)
        expected = [
            TextNode("This is a link: ", TextType.TEXT),
            TextNode("Link text", TextType.LINK, url="https://example.com")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_images_and_links_multiple_images_and_links(self):
        nodes = [TextNode("Image: ![Alt 1](url1), Link: [Text 1](url2), Image: ![Alt 2](url3)", TextType.TEXT)]
        result = TextNode.split_nodes_images_and_links(nodes)
        expected = [
            TextNode("Image: ", TextType.TEXT),
            TextNode("Alt 1", TextType.IMAGE, url="url1"),  # Updated expected result
            TextNode(", Link: ", TextType.TEXT),
            TextNode("Text 1", TextType.LINK, url="url2"),
            TextNode(", Image: ", TextType.TEXT),
            TextNode("Alt 2", TextType.IMAGE, url="url3")  # Updated expected result
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_images_and_links_no_images_or_links(self):
        nodes = [TextNode("This text has no images or links.", TextType.TEXT)]
        result = TextNode.split_nodes_images_and_links(nodes)
        expected = [TextNode("This text has no images or links.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_images_and_links_empty_text(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = TextNode.split_nodes_images_and_links(nodes)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_images_and_links_non_text_node(self):
        nodes = [TextNode("Some text", TextType.BOLD)]
        result = TextNode.split_nodes_images_and_links(nodes)
        expected = [TextNode("Some text", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_from_markdown_basic(self):
        text = "This is *italic* and **bold** text."
        result = TextNode.from_markdown(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_from_markdown_with_image(self):
        text = "This is an image: ![Alt text](image.jpg)"
        result = TextNode.from_markdown(text)
        expected = [
            TextNode("This is an image: ", TextType.TEXT),
            TextNode("Alt text", TextType.IMAGE, url="image.jpg")
        ]
        self.assertEqual(result, expected)

    def test_from_markdown_with_link(self):
        text = "This is a link: [Link text](link.com)"
        result = TextNode.from_markdown(text)
        expected = [
            TextNode("This is a link: ", TextType.TEXT),
            TextNode("Link text", TextType.LINK, url="link.com")
        ]
        self.assertEqual(result, expected)

    def test_from_markdown_with_code(self):
        text = "This is `code`."
        result = TextNode.from_markdown(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_from_markdown_complex(self):
        text = "This is *italic* and **bold** text with an image: ![Alt text](image.jpg) and a link: [Link text](link.com) and some `code`."
        result = TextNode.from_markdown(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with an image: ", TextType.TEXT),
            TextNode("Alt text", TextType.IMAGE, url="image.jpg"),
            TextNode(" and a link: ", TextType.TEXT),
            TextNode("Link text", TextType.LINK, url="link.com"),
            TextNode(" and some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
