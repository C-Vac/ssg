# htmlnode.py
from textnode import TextNode, TextType

class HTMLNode:
    """
    Represents an HTML node in a document.

    Attributes:
        tag (str): The HTML tag for the node (e.g., 'div', 'span').
        value (str): The text content of the node.
        children (list): A list of child HTMLNode objects.
        props (dict): A dictionary of HTML attributes and their values.
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Initializes an HTMLNode instance.

        Args:
            tag (str, optional): The HTML tag for the node. Defaults to None.
            value (str, optional): The text content of the node. Defaults to None.
            children (list, optional): A list of child HTMLNode objects. Defaults to None.
            props (dict, optional): A dictionary of HTML attributes and their values. Defaults to None.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        Converts the HTMLNode and its children into an HTML string.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError

    def props_to_html(self):
        """
        Converts the node's properties to an HTML string.

        Returns:
            str: A string of HTML attributes.
        """
        props_string = ""
        if self.props:
            for key, value in self.props.items():
                props_string = props_string + f' {key}="{value}"'
        return props_string

    def __repr__(self):
        """
        Returns a string representation of the HTMLNode.

        Returns:
            str: A string representation of the HTMLNode.
        """
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    @staticmethod
    def text_node_to_html_node(text_node):
        """
        Converts a TextNode object to an HTMLNode object.

        Args:
            text_node (TextNode): The TextNode to convert.

        Returns:
            HTMLNode: The corresponding HTMLNode.

        Raises:
            TypeError: If the input is not a TextNode.
            Exception: If the TextNode's text type is not supported.
        """
        if isinstance(text_node, TextNode):
            match text_node.text_type:
                case TextType.TEXT:
                    return LeafNode(text_node.text)
                case TextType.BOLD:
                    return LeafNode(text_node.text, tag="b")
                case TextType.ITALIC:
                    return LeafNode(text_node.text, tag="i")
                case TextType.CODE:
                    return LeafNode(text_node.text, tag="code")
                case TextType.LINK:
                    return LeafNode(
                        text_node.text, tag="a", props={"href": text_node.url}
                    )
                case TextType.IMAGE:
                    return LeafNode(
                        value="",
                        tag="img",
                        props={"src": text_node.url, "alt": text_node.text},
                    )
                case _:
                    raise Exception("Text type not supported!")
        raise TypeError("That is NOT a TextNode!")


class LeafNode(HTMLNode):
    """
    Represents a leaf HTML node with no children.

    Attributes:
        tag (str): The HTML tag for the node (e.g., 'div', 'span').
        value (str): The text content of the node.
        props (dict): A dictionary of HTML attributes and their values.
    """
    def __init__(self, value, tag=None, props=None):
        """
        Initializes a LeafNode instance.

        Args:
            value (str): The text content of the node.
            tag (str, optional): The HTML tag for the node. Defaults to None.
            props (dict, optional): A dictionary of HTML attributes and their values. Defaults to None.
        """
        super().__init__(tag, value, None, props)

    def to_html(self):
        """
        Converts the LeafNode to an HTML string.

        Returns:
            str: The HTML string representation of the LeafNode.

        Raises:
            ValueError: If the LeafNode has no value.
        """
        if self.value == None:
            raise ValueError(f"Leaf node has no value: {self}")
        if not self.tag:
            return self.value

        props_str = ""
        if self.props:
            for key, val in self.props.items():
                props_str = props_str + f' {key}="{val}"'
        if self.tag == "img":
            return f"<{self.tag}{props_str}>"
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    """
    Represents a parent HTML node with children.

    Attributes:
        tag (str): The HTML tag for the node (e.g., 'div', 'ul').
        children (list): A list of child nodes.
        props (dict): A dictionary of HTML attributes and their values.
    """
    def __init__(self, children, tag=None, props=None):
        """
        Initializes a ParentNode instance.

        Args:
            children (list): A list of child nodes.
            tag (str, optional): The HTML tag for the node. Defaults to None.
            props (dict, optional): A dictionary of HTML attributes and their values. Defaults to None.
        """
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        """
        Converts the ParentNode and its children to an HTML string.

        Returns:
            str: The HTML string representation of the ParentNode and its children.

        Raises:
            ValueError: If the ParentNode has no tag or no children.
        """
        if not self.tag:
            raise ValueError("Parent node has no tag!")
        if not self.children:
            raise ValueError("Parent node has no children!")

        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()

        props_str = ""
        if self.props:
            for key, val in self.props.items():
                props_str = props_str + f' {key}="{val}"'
        return f"<{self.tag}{props_str}>{inner_html}</{self.tag}>"
