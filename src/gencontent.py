from markdown_blocks import markdown_to_html_node 
from htmlnode import HTMLNode, LeafNode, ParentNode
import os


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in the markdown content.")


def generate_page(from_path, template_path, dest_path, basepath):
    #print message indicating the start of page generation
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")

    #read the markdown content from the source file
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    
    #read the template content from the template file
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    
    #markdown to html conversion
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    #get title from the markdown content
    title = extract_title(markdown_content)

    #replace the placeholder in the template with the generated HTML content and title
    final_content = template_content.replace("{{ Content }}", html_content).replace("{{ Title }}", title)

    final_content = final_content.replace('href="/', f'href="{basepath}')
    final_content = final_content.replace('src="/', f'src="{basepath}')

    dirname = os.path.dirname(dest_path)
    if dirname != "":
        os.makedirs(dirname, exist_ok=True)
    #write the final content to the destination file
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content = os.listdir(dir_path_content)
    for c in content:
        if os.path.isdir(os.path.join(dir_path_content, c)):
            next_source_dir = os.path.join(dir_path_content, c)
            next_dest_dir = os.path.join(dest_dir_path, c)
            os.makedirs(next_dest_dir, exist_ok=True)
            generate_pages_recursive(next_source_dir, template_path, next_dest_dir, basepath)
        elif os.path.isfile(os.path.join(dir_path_content, c)) and c.endswith(".md"):
            source_file = os.path.join(dir_path_content, c)
            html_name = c.replace(".md", ".html")
            dest_file = os.path.join(dest_dir_path, html_name)
            generate_page(source_file, template_path, dest_file, basepath)
