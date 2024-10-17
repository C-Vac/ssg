from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

text = "This is *italic* and **bold** text with an image: ![Alt text](image.jpg) and a link: [Link text](link.com)"
nodes = TextNode.from_markdown(text)

for node in nodes:
  print(node)
