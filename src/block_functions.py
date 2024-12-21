from nodes import *
from inline_functions import text_to_textnodes

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), markdown.split('\n\n'))))
    return blocks

def block_to_block_type(markdown_block: str) -> str:
    def is_heading(markdown_block: str) -> bool:
        index = 0
        while index < len(markdown_block) and markdown_block[index] == '#':
            index += 1
        if (0 < index <= 6 
            and index + 1 < len(markdown_block)
            and markdown_block[index] == " "):
            return True
        return False
    
    def is_code(markdown_block: str) -> bool:
        if len(markdown_block) < 7 or markdown_block[:3] != '```' or markdown_block[-3:] != '```':
            return False
        return True

    def is_quote(markdown_block: str) -> bool:
        lines = markdown_block.splitlines()
        for line in lines:
            if line.find(">") != 0:
                return False
        return True
    
    def is_unordered_list(markdown_block: str) -> bool:
        lines = markdown_block.splitlines()
        for line in lines:
            if line.find("* ") != 0 and line.find("- ") != 0:
                return False
        return True

    def is_ordered_list(markdown_block: str) -> bool:
        lines = markdown_block.splitlines()
        i = 1
        for line in lines:
            if line.find(f"{i}. ") != 0:
                return False
            i += 1
        return True
    
    if markdown_block is None or len(markdown_block) == 0:
        return None
    if is_heading(markdown_block):
        return "heading"
    if is_code(markdown_block):
        return "code"
    if is_quote(markdown_block):
        return "quote"
    if is_unordered_list(markdown_block):
        return "unordered_list"
    if is_ordered_list(markdown_block):
        return "ordered_list"
    return "paragraph"

def markdown_to_html_node(markdown: str) -> HTMLNode:
    def text_to_children(text: str) -> list[HTMLNode]:
        children = []
        nodes = text_to_textnodes(text)
        for node in nodes:
            children.append(text_node_to_html_node(node))
        return children

    def to_heading(block: str) -> HTMLNode:
        level = block.find(" ")
        node = ParentNode(f"h{level}", text_to_children(block[level + 1:]))
        return node
    
    def to_code(block: str) -> HTMLNode:
        node = ParentNode("pre",[ParentNode("code", text_to_children(block[3:-3]))])
        return node

    def to_quote(block: str) -> HTMLNode:
        lines = block.splitlines()
        formatted = list(map(lambda x : x[1:], lines))
        node = ParentNode("blockquote", text_to_children(formatted))
        return node

    def to_unordered_list(block: str) -> HTMLNode:
        lines = block.splitlines()
        formatted = list(map(lambda x : ParentNode("li", text_to_children(x[2:])), lines))
        node = ParentNode("ul", formatted)
        return node

    def to_ordered_list(block: str) -> HTMLNode:
        lines = block.splitlines()
        formatted = list(map(lambda x : ParentNode("li", text_to_children(x[2:])), lines))
        node = ParentNode("ol", formatted)
        return node

    def to_paragraph(block: str) -> HTMLNode:
        node = ParentNode("p", text_to_children(block))
        return node

    parent = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        node_type = block_to_block_type(block)
        node = None
        match node_type:
            case "heading":
                node = to_heading(block)
            case "code":
                node = to_code(block)
            case "quote":
                node = to_quote(block)
            case "unordered_list":
                node = to_unordered_list(block)
            case "ordered_list":
                node = to_ordered_list(block)
            case "paragraph":
                node = to_paragraph(block)
            case _:
                continue
        parent.children.append(node)
    return parent
