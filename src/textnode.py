from enum import Enum
import re
  
class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode():

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            raise TypeError(f"Cannot compare TextNode to {type(other)} type object '{other}'!")
        return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    @classmethod
    def from_markdown(cls, text):
        """
        Creates a list of TextNode objects from a Markdown text string.

        Args:
            text (str): The Markdown text to parse.

        Returns:
            list: A list of TextNode objects representing the parsed Markdown text.
        """
        nodes = [TextNode(text, TextType.TEXT)]
        nodes = cls.split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        nodes = cls.split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = cls.split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = cls.split_nodes_images_and_links(nodes)
        return nodes

    @staticmethod
    def split_nodes_delimiter(old_nodes, delimiter: str, text_type: TextType):
        """
        Splits text nodes with a given delimiter into multiple text nodes with different types.

        The function now splits the text by the delimiter exactly as it is,
        distinguishing between different delimiters (e.g., "\*" vs "\*\*").

        It also handles the special case where the delimiter is "*" and the character
        immediately after is also "\*", treating it as a literal "\*\*" and not a delimiter.

        Additionally, it handles the case where the text begins with a delimiter,
        ensuring that the emphasized node is correctly labeled with the text_type.

        Args:
            old_nodes (list): A list of TextNode objects.
            delimiter (str): The delimiter to split the text by.
            text_type (TextType): The TextType to assign to the delimited text.

        Returns:
            list: A new list of TextNode objects with the split text.

        Raises:
            SyntaxError: If there are unmatched delimiters.

        Examples:
            >>> node1 = TextNode("This is *italic* and **bold** text", TextType.TEXT)
            >>> new_nodes = TextNode.split_nodes_delimiter([node1], "*", TextType.ITALIC)
            >>> new_nodes = TextNode.split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
            >>> print(new_nodes)
            [TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)]
        """
        new_nodes = []
        for node in old_nodes:
            if node.text_type == TextType.TEXT:
                parts = []
                text = ""
                delimiter_count = 0
                i = 0

                # Handle the case where the text begins with a delimiter
                if node.text.startswith(delimiter):
                    parts.append("")
                    delimiter_count += 1
                    i += len(delimiter)

                while i < len(node.text):
                    if delimiter == "*" and i < len(node.text) - 1 and node.text[i] == "*" and node.text[i + 1] == "*":  # Check for "**"
                        text += "**"  # Add "**" to the text part
                        i += 2  # Skip the "**"
                    elif node.text[i:i + len(delimiter)] == delimiter:
                        if text:
                            parts.append(text)
                        text = ""
                        delimiter_count += 1
                        i += len(delimiter)
                    else:
                        text += node.text[i]
                        i += 1
                parts.append(text)

                if delimiter_count % 2 != 0:
                    raise SyntaxError(f"Invalid Markdown syntax: unmatched delimiter '{delimiter}'")

                text_parts = parts[::2]
                code_parts = parts[1::2]
                for text, code in zip(text_parts, code_parts + [""]):
                    if text:
                        new_nodes.append(TextNode(text, TextType.TEXT))
                    if code:
                        new_nodes.append(TextNode(code.replace(delimiter, "", 1), text_type))

            else:
                new_nodes.append(node)

        return new_nodes

    @staticmethod
    def split_nodes_images_and_links(old_nodes):
        """
        Splits text nodes based on the presence of Markdown images or links.

        This function uses the helper methods `_extract_image_parts`, `_extract_link_parts`,
        and `_split_text_by_parts` to identify and split image and link nodes.

        Args:
            old_nodes (list): A list of TextNode objects.

        Returns:
            list: A new list of TextNode objects with split text nodes for images and links.
        """
        new_nodes = []
        for node in old_nodes:
            if node.text_type == TextType.TEXT:
                image_parts = TextNode._extract_image_parts(node.text)
                link_parts = TextNode._extract_link_parts(node.text)
                all_parts = image_parts + link_parts

                if all_parts:
                    new_nodes.extend(TextNode._split_text_by_parts(node.text, all_parts))
                else:
                    new_nodes.append(node)
            else:
                new_nodes.append(node)
        return new_nodes

    @staticmethod
    def _extract_image_parts(text):
        """
        Extracts image parts from a text string.
        """
        parts = []
        for alt_text, url in TextNode._extract_markdown_images(text):
            for match in re.finditer(re.escape(f"![{alt_text}]({url})"), text):
                start, end = match.span()
                # Add a marker to indicate it's an image part
                parts.append((start, end, alt_text, url, "image"))  
        return parts

    @staticmethod
    def _extract_link_parts(text):
        """
        Extracts link parts from a text string.
        """
        parts = []
        for link_text, url in TextNode._extract_markdown_links(text):
            for match in re.finditer(re.escape(f"[{link_text}]({url})"), text):
                start, end = match.span()
                # Add a marker to indicate it's a link part
                parts.append((start, end, link_text, url, "link"))  
        return parts

    @staticmethod
    def _split_text_by_parts(text, parts):
        """
        Splits a text string into parts based on the given parts list.
        """
        nodes = []
        last_end = 0
        for start, end, text_content, url, part_type in sorted(parts):  # Include part_type
            if text[last_end:start]:
                nodes.append(TextNode(text[last_end:start], TextType.TEXT))
            # Determine node type based on part_type
            node_type = TextType.IMAGE if part_type == "image" else TextType.LINK  
            nodes.append(TextNode(text_content, node_type, url=url))
            last_end = end
        if last_end < len(text):
            nodes.append(TextNode(text[last_end:], TextType.TEXT))
        return nodes

    @staticmethod
    def _extract_markdown_images(text):
        pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        matches = re.findall(pattern, text)
        return matches

    @staticmethod
    def _extract_markdown_links(text):
        pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
        matches = re.findall(pattern, text)
        return matches
