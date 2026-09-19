from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_node, TextType

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"


#raw markdown text to list of block strings
def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    split_blocks = [block.strip() for block in split_blocks if block.strip()]
    return split_blocks

def block_to_block_type(block_string):
    
    count = 0
    for char in block_string:
        if char == "#":
            count += 1
        else:
            break
    if count > 0 and count <=6 and block_string[count] == " ":
        return BlockType.HEADING
    elif block_string.startswith("```\n") and block_string.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in block_string.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in block_string.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i+1}. ") for i, line in enumerate(block_string.split("\n"))):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes
    

#markdown to html
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            level = len(block) - len(block.lstrip("#"))
            content = block[level:].strip()
            tag_string = f"h{level}"
            html_nodes.append(ParentNode(tag_string, text_to_children(content)))
        elif block_type == BlockType.CODE:
            code_content = block[3:-3].removeprefix("\n")
            text_node = TextNode(code_content, TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            html_nodes.append(ParentNode("pre", [html_node]))
        elif block_type == BlockType.QUOTE:
            quote_content = " ".join(line[1:].strip() for line in block.split("\n"))
            html_nodes.append(ParentNode("blockquote", text_to_children(quote_content)))
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = [line[2:].strip() for line in block.split("\n")]
            list_children = [ParentNode("li", text_to_children(item)) for item in list_items]
            html_nodes.append(ParentNode("ul", list_children))
        elif block_type == BlockType.ORDERED_LIST:
            list_items = [line.split(". ", 1)[1].strip() for line in block.split("\n")]
            list_children = [ParentNode("li", text_to_children(item)) for item in list_items]
            html_nodes.append(ParentNode("ol", list_children))
        else:
            content = " ".join(line.strip() for line in block.split("\n"))
            html_nodes.append(ParentNode("p", text_to_children(content)))
    return ParentNode("div", html_nodes)

            
            
        