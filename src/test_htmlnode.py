import unittest

from htmlnode import HTMLNode, LeafNode

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

if __name__ == "__main__":
    unittest.main()
