from nodes import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        front = 0
        ignored = 0
        length = len(node.text)
        while front < length:
            start = node.text.find(delimiter, front + ignored)
            end = node.text.find(delimiter, start + len(delimiter))
            # If 0 or 1 found
            if (start == -1 or end == -1):
                new_nodes.append(TextNode(node.text[front:], TextType.NORMAL))
                break
            # If the delimiters bracket an empty string, ignore them.
            if end == start + len(delimiter):
                ignored += len(delimiter) * 2
                continue
            # We have a paired set of delimiters
            if (start > front):
                new_nodes.append(TextNode(node.text[front:start], TextType.NORMAL))
            new_nodes.append(TextNode(node.text[start + len(delimiter):end], text_type))               
            front = end + len(delimiter)
            ignored = 0
    return new_nodes

import re

def extract_markdown_images(text: str) -> list[tuple]:
    search = r"!\[([^\]]*)\]\(([^\(\)]+)\)"
    matches = re.findall(search, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple]:
    # Regex Breakdown (reference https://regexr.com/)
    # (?<!                  | Negative Lookbehind -> If this group matches, don't match rest of expression.
    #     !                 | If starts with !, this is an image, not link.
    # )                     |
    # \[                    | Match a literal [
    #     (                 | Start group #1 - if multiple groups in expression, return of findall is list of tuples with all groups
    #         [             | Start of a set of characters to match
    #             ^\[\]     | Matching rule: ^=Not, so match anything that isn't []. 
    #                  +    | + = match 1 or more times.
    # ])\]                  |  
    # \[                    |
    #     (                 | Start group #2
    #         [             |   
    #             ^\(\)+    |
    # ])\]                  |

    search = r"(?<!!)\[([^\]]+)\]\(([^\(\)]+)\)"
    matches = re.findall(search, text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        start_index = 0
        for i in range(len(images)):
            text, url = images[i]
            image_str = f"![{text}]({url})"
            index = node.text.find(image_str, start_index)
            if index > start_index:
                new_nodes.append(TextNode(node.text[start_index:index], TextType.NORMAL))
            new_nodes.append(TextNode(text, TextType.IMAGE, url))
            start_index = index + len(image_str)
        if start_index < len(node.text):
            new_nodes.append(TextNode(node.text[start_index:], TextType.NORMAL))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        images = extract_markdown_links(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        start_index = 0
        for i in range(len(images)):
            text, url = images[i]
            link_str = f"[{text}]({url})"
            index = node.text.find(link_str, start_index)
            # Need to ensure that we match against a link not an image
            while (index - 1 > 0 and node.text[index - 1] == "!"):
                index = node.text.find(link_str, index + 1)
            #
            if index > start_index:
                new_nodes.append(TextNode(node.text[start_index:index], TextType.NORMAL))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            start_index = index + len(link_str)
        if start_index < len(node.text):
            new_nodes.append(TextNode(node.text[start_index:], TextType.NORMAL))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextType.NORMAL)]

    nodes = split_nodes_delimiter(nodes, "```", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "``", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)

    return nodes