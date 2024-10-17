import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode("div")
        self.assertEqual(node.props_to_html(), "")  # No props should result in an empty string

    def test_props_to_html_single_prop(self):
        node = HTMLNode("div", props={"class": "container"})
        self.assertEqual(node.props_to_html(), ' class="container"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode("div", props={"class": "container", "id": "my-div"})
        # Order of props is not guaranteed, so check for both possible outputs
        try:
            self.assertEqual(node.props_to_html(), ' class="container" id="my-div"')
        except AssertionError:
            self.assertEqual(node.props_to_html(), ' id="my-div" class="container"')

    def test_repr(self):
        node = HTMLNode("div", "Hello", None, {"class": "container"})
        self.assertEqual(repr(node), "HTMLNode(div, Hello, None, {'class': 'container'})")

    def test_text_node_to_html_node_plain_text(self):
        text_node = TextNode("Hello", TextType.TEXT)
        html_node = HTMLNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello")

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Hello", TextType.BOLD)
        html_node = HTMLNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello")

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("Hello", TextType.ITALIC)
        html_node = HTMLNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Hello")

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("Hello", TextType.CODE)
        html_node = HTMLNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Hello")

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Hello", TextType.LINK, url="https://example.com")
        html_node = HTMLNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("Image", TextType.IMAGE, url="https://example.com/image.jpg")
        html_node = HTMLNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://example.com/image.jpg")
        self.assertEqual(html_node.props["alt"], "Image")

    def test_text_node_to_html_node_unsupported_type(self):
        text_node = TextNode("Hello", 420)
        with self.assertRaises(Exception):
            html_node = HTMLNode.text_node_to_html_node(text_node)

    def test_text_node_to_html_node_not_text_node(self):
        with self.assertRaises(TypeError):
            html_node = HTMLNode.text_node_to_html_node("Hello")


class TestLeafNode(unittest.TestCase):

    def test_to_html_no_tag(self):
        node = LeafNode("Hello")
        self.assertEqual(node.to_html(), "Hello")

    def test_to_html_with_tag(self):
        node = LeafNode("Hello", tag="p")
        self.assertEqual(node.to_html(), "<p>Hello</p>")

    def test_to_html_with_tag_and_props(self):
        node = LeafNode("Hello", tag="p", props={"class": "text-red"})
        self.assertEqual(node.to_html(), "<p class=\"text-red\">Hello</p>")

    def test_to_html_no_value_raises_error(self):
        node = LeafNode(None, tag="p")
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):

    def test_to_html_no_tag(self):
        node = ParentNode([LeafNode("Hello")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        node = ParentNode([], tag="div")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_simple(self):
        node = ParentNode([LeafNode("Hello")], tag="div")
        self.assertEqual(node.to_html(), "<div>Hello</div>")

    def test_to_html_with_props(self):
        node = ParentNode([LeafNode("Hello")], tag="div", props={"class": "container"})
        self.assertEqual(node.to_html(), "<div class=\"container\">Hello</div>")

    def test_to_html_multiple_children(self):
        node = ParentNode([LeafNode("Hello"), LeafNode("World")], tag="div")
        self.assertEqual(node.to_html(), "<div>HelloWorld</div>")

    def test_to_html_nested_parents(self):
        inner_node = ParentNode([LeafNode("Inner")], tag="span")
        outer_node = ParentNode([inner_node], tag="div")
        self.assertEqual(outer_node.to_html(), "<div><span>Inner</span></div>")

    def test_to_html_complex_nesting(self):
        leaf1 = LeafNode("One")
        leaf2 = LeafNode("Two")
        span1 = ParentNode([leaf1], tag="span")
        span2 = ParentNode([leaf2], tag="span", props={"class": "bold"})
        div = ParentNode([span1, span2], tag="div", props={"id": "content"})
        expected_html = "<div id=\"content\"><span>One</span><span class=\"bold\">Two</span></div>"
        self.assertEqual(div.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()
