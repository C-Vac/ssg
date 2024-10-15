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
