from enum import Enum

class HTMLNode():
    
    def __init__(self, tag: str = None, value: str = None, 
                 children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        html = ""
        if self.props == None:
            return ""
        for attr in self.props:
            html += f" {attr}=\"{self.props[attr]}\""
        return html
