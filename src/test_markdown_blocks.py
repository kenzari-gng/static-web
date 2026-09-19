import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, text_to_children, markdown_to_html_node

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
# Heading

This is a paragraph.

- list item
- another item
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            [
                "# Heading",
                "This is a paragraph.",
                "- list item\n- another item"
            ],
            blocks
        )
    
    #block to block type
    def test_valid_heading(self):
        block_string = "# Heading"
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_valid_code(self):
        block_string = "```\ncode block\n```"
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.CODE, block_type)

    def test_valid_quote(self):
        block_string = "> This is a quote\n> Another line of the quote"
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_valid_unordered_list(self):
        block_string = "- list item\n- another item"
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_valid_ordered_list(self):
        block_string = "1. list item\n2. another item"
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)
    
    def test_valid_paragraph(self):
        block_string = "This is a paragraph."
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_heading(self):
        block_string = "####### Invalid heading"
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
    
    def test_invalid_code(self):
        block_string = "```\ncode block"
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_quote(self):
        block_string = "> This is a quote\nAnother line of the quote"
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_invalid_unordered_list(self):
        block_string = "- list item\n* another item"
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
    
    def test_invalid_ordered_list(self):
        block_string = "1. list item\n3. another item"
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_valid_quote_with_multiple_lines(self):
        block_string = "> This is a quote\n>Another line of the quote\n> Yet another line"
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.QUOTE, block_type)
    
    def test_valid_unordered_list_with_multiple_lines(self):
        block_string = "- list item\n- another item\n- yet another item"
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_valid_ordered_list_with_multiple_lines(self):
        block_string = "1. list item\n2. another item\n3. yet another item"
        block_type = block_to_block_type(block_string)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

    #markdown to html
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_quote(self):
        md = """
> This is a quote
> with multiple lines
> one last line
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines one last line</blockquote></div>",
        )
    def test_unordered_list(self):
        md = """
- This is a list item
- This is another list item
- This is a third list item
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list item</li><li>This is another list item</li><li>This is a third list item</li></ul></div>",
        )