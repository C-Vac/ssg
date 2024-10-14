class HTMLNode():
  def __init__(self=None, tag=None, value=None, children=None, props=None):
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
