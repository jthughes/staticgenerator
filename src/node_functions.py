from textnode import *
from htmlnode import *
from parentnode import *
from leafnode import *

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

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        search_string = node.text
        breaks = search_string.count(delimiter)
        fragments = search_string.split(delimiter)
        index = 0
        
        # Need at least two breaks to have a valid section 
        while breaks >= 2:
            # If doesn't start with a delimiter, have a normal section first
            # If it does, split will give an empty string for fragments[0],
            # so will need to clean either way
            if not search_string.startswith(delimiter, index):
                new_nodes.append(TextNode(fragments[0], TextType.NORMAL))
            index += len(fragments[0])
            fragments.pop(0)
            index += len(delimiter)

            new_nodes.append(TextNode(fragments[0], text_type))
            index += len(fragments[0]) + len(delimiter)
            fragments.pop(0)
            breaks -= 2
        # Insufficient remaining breaks to have properly tagged segement
        new_nodes.append(TextNode(search_string[index:], TextType.NORMAL)) 
    return new_nodes

import re

def extract_markdown_images(text: str) -> list[tuple]:
    search = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(search, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple]:
    search = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(search, text)
    return matches