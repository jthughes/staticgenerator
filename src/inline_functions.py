from nodes import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
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
        remainder = search_string[index:]
        if (len(remainder) > 0):
            new_nodes.append(TextNode(remainder, TextType.NORMAL)) 
    return new_nodes

import re

def extract_markdown_images(text: str) -> list[tuple]:
    search = r"!\[([^\[\]]*)\]\(([^\(\)]+)\)"
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

    search = r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)"
    matches = re.findall(search, text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
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

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    pass