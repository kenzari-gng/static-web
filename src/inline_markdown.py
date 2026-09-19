from textnode import TextNode, TextType, text_node_to_html_node
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
    
        else:
            split_texts = node.text.split(delimiter)
            if len(split_texts) % 2 == 0:
                raise Exception("Invalid markdown syntax: unmatched delimiter")
            for i, text in enumerate(split_texts):
                if text == "":
                    continue
                if i%2 == 0:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text, text_type))
    return new_nodes
            
# This function extracts markdown image syntax from the text and returns a list of TextNode objects.
# The markdown image syntax is ![alt text](image_url)
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

#split image nodes and link nodes into text nodes
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = extract_markdown_images(node.text)
            if not matches:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for match in matches:
                    alt_text, image_url = match
                    image_markdown = f"![{alt_text}]({image_url})"
                    before, after = remaining_text.split(image_markdown, 1)
                    if before:
                        new_nodes.append(TextNode(before, TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
                    remaining_text = after
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = extract_markdown_links(node.text)
            if not matches:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for match in matches:
                    alt_text, link_url = match
                    link_markdown = f"[{alt_text}]({link_url})"
                    before, after = remaining_text.split(link_markdown, 1)
                    if before:
                        new_nodes.append(TextNode(before, TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.LINK, link_url))
                    remaining_text = after
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
    return new_nodes

#raw string of markdown text to list of TextNode objects       
def text_to_textnodes(text):
    text_node = [TextNode(text, TextType.TEXT)]
    text_node = split_nodes_delimiter(text_node, "**", TextType.BOLD)
    text_node = split_nodes_delimiter(text_node, "_", TextType.ITALIC)
    text_node = split_nodes_delimiter(text_node, "`", TextType.CODE)
    text_node = split_nodes_image(text_node)
    text_node = split_nodes_link(text_node)
    return text_node