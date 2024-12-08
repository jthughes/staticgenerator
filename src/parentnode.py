from enum import Enum

from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag, None, children, props)


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag set")
        if self.children == None:
            raise ValueError("No children set")
        if len(self.children) == 0:
            raise ValueError("Empty children list")
        inner_html = ""
        for tag in self.children:
            inner_html += tag.to_html()
        return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"