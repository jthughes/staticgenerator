import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode(tag="p", value="Test", props={"style":"color=green"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Test")
        self.assertEqual(node.children, None)
        self.assertDictEqual(node.props, {"style": "color=green"})

    def test_empty(self):
        node = LeafNode("This is raw text")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "This is raw text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_not_equal(self):
        node = LeafNode(tag="p", value="Test", props={"style":"color=green"})
        node2 = LeafNode(tag="h1", value="Test", props={"style":"color=green"})
        self.assertNotEqual(node, node2)

    def test_props(self):
        node = LeafNode(tag="p", value="Test", props={"style":"color=green"})
        expected = f" style=\"color=green\""
        actual = node.props_to_html()
        self.assertEqual(expected,  actual)
    
    def test_props_none(self):
        node = LeafNode(tag="p", value="Test")
        expected = ""
        actual = node.props_to_html()
        self.assertEqual(expected, actual)

    def test_to_html_simple(self):
        node = LeafNode(tag="p", value="This is a test")
        self.assertEqual(node.to_html(), "<p>This is a test</p>")

    def test_to_html_complex(self):
        node = LeafNode(tag="h1", value="My heading", props={"href": "localhost"})
        self.assertEqual(node.to_html(), "<h1 href=\"localhost\">My heading</h1>")

if __name__ == "__main__":
    unittest.main()