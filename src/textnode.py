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