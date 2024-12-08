from enum import Enum

from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    
    def __init__(self, value: str, tag: str = None, 
                 children: list = None, props: dict = None):
        super().__init__(tag, value, children, props)


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        if self.value == None:
            raise ValueError("No value set")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"