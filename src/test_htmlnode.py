import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
