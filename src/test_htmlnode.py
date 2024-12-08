import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "Test", props={"style":"color:green"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Test")
        self.assertEqual(node.children, None)
        self.assertDictEqual(node.props, {"style": "color:green"})

    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_not_equal(self):
        node = HTMLNode("p", "Test", props={"style":"color:green"})
        node2 = HTMLNode("h1", "Test", props={"style":"color:green"})
        self.assertNotEqual(node, node2)

    def test_props(self):
        node = HTMLNode("p", "Test", props={"style":"color:green"})
        expected = f" style=\"color:green\""
        actual = node.props_to_html()
        self.assertEqual(expected,  actual)
    
    def test_props_none(self):
        node = HTMLNode("p", "Test")
        expected = ""
        actual = node.props_to_html()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()