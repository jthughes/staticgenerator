from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (other.text == self.text 
            and other.text_type == self.text_type
            and other.url == self.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

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

class ParentNode(HTMLNode):
    
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag, None, children, props)


    # def __repr__(self):
    #     return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
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

class LeafNode(HTMLNode):
    
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)

    # def __repr__(self):
    #     return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        if self.value == None:
            raise ValueError("No value set")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Unrecognised type")
