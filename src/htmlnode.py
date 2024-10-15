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
    if self.value == None:
      raise ValueError("Leaf node has no value!")
    if self.tag == None:
      return self.value
    
    props_str = ""
    if self.props != None:
      for key, val in self.props.items():
        props_str = props_str + f' {key}="{val}"'
    return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
