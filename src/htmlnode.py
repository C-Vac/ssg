from textnode import TextNode, TextType

class HTMLNode():
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
  
  def to_html(self):
    raise NotImplementedError
  
  def props_to_html(self):
    props_string = ""
    if self.props:
      for key, value in self.props.items():
        props_string = props_string + f' {key}="{value}"'
    return props_string

  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

  @staticmethod
  def text_node_to_html_node(text_node):
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
          return LeafNode(text_node.text, tag="a", props={"href": text_node.url})
        case TextType.IMAGE:
          return LeafNode(value="", tag="img", props={"src": text_node.url, "alt": text_node.text})
        case _:
          raise Exception("Text type not supported!")
    raise TypeError("That is NOT a TextNode!")

class LeafNode(HTMLNode):
  def __init__(self, value, tag=None, props=None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if not self.value:
      raise ValueError("Leaf node has no value!")
    if not self.tag:
      return self.value
    
    props_str = ""
    if self.props:
      for key, val in self.props.items():
        props_str = props_str + f' {key}="{val}"'
    return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
  def __init__(self, children, tag=None, props=None):
    super().__init__(tag=tag, children=children, props=props)

  def to_html(self):
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
