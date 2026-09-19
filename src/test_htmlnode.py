import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" target="_blank"')

    def test_no_props(self):
        node = HTMLNode(tag="p", value="Hello, world!", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_tags(self):
        node1 = HTMLNode(tag="div", value="Firebolt!", props=None)
        node2 = HTMLNode(tag="p", value="Firebolt!", props=None)
        self.assertNotEqual(node1.tag, node2.tag)

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_props(self):
        node = LeafNode(tag="a", value="Click here", props={"href": "https://www.boot.dev", "target": "_blank"})
        expected_html = '<a href="https://www.boot.dev" target="_blank">Click here</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_without_props(self):
        node = LeafNode(tag="p", value="Hello, world!", props=None)
        expected_html = '<p>Hello, world!</p>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_no_tag(self):
        node = LeafNode(tag=None, value="Just text", props=None)
        expected_html = 'Just text'
        self.assertEqual(node.to_html(), expected_html)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        expected_html = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), expected_html)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child1 = LeafNode(tag="p", value="Child 1", props=None)
        child2 = LeafNode(tag="p", value="Child 2", props=None)
        parent_node = ParentNode(tag="div", children=[child1, child2], props={"class": "container"})
        expected_html = '<div class="container"><p>Child 1</p><p>Child 2</p></div>'
        self.assertEqual(parent_node.to_html(), expected_html)

    def test_to_html_no_children(self):
        parent_node = ParentNode(tag="div", children=[], props={"class": "container"})
        expected_html = '<div class="container"></div>'
        self.assertEqual(parent_node.to_html(), expected_html)

    def test_to_html_no_tag(self):
        child1 = LeafNode(tag="p", value="Child 1", props=None)
        parent_node = ParentNode(tag=None, children=[child1], props={"class": "container"})
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_children_error(self):
        parent_node = ParentNode(tag="div", children=None, props={"class": "container"})
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_one_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )