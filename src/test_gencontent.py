import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is a title\n\nThis is some content."
        title = extract_title(markdown)
        self.assertEqual(title, "This is a title")

    def test_extract_title_no_title(self):
        markdown = "This is some content without a title."
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_not_first_line(self):
        markdown = "This is some content.\n# This is a title"
        title = extract_title(markdown)
        self.assertEqual(title, "This is a title")

    def test_extract_title_h2(self):
        markdown = "## This is a subtitle\n\nThis is some content."
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_h1_with_spaces(self):
        markdown = "#  This is a title with spaces  \n\nThis is some content."
        title = extract_title(markdown)
        self.assertEqual(title, "This is a title with spaces")