
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