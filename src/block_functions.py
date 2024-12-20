
def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), markdown.split('\n\n'))))
    return blocks
