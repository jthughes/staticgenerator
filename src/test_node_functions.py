import unittest

from node_functions import *

class TestNodeFunctions(unittest.TestCase):
    def test_bold(self):
        text_node = TextNode("Test", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b", "Incorrect Tag")
        self.assertEqual(html_node.value, "Test", "Incorrect Value")
        self.assertEqual(html_node.children, None, "Incorrect Children")
        self.assertEqual(html_node.props, None, "Incorrect Props")
        self.assertEqual(html_node.to_html(), "<b>Test</b>", "Incorrect to_html() return")

    def test_link(self):
        text_node = TextNode("[Click me]", TextType.LINK, "boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "[Click me]")
        self.assertEqual(html_node.children, None)
        self.assertDictEqual(html_node.props, {"href": "boot.dev"})
        self.assertEqual(
            html_node.to_html(),
            "<a href=\"boot.dev\">[Click me]</a>")
    
    def test_image(self):
        text_node = TextNode("Cat", TextType.IMAGE, "/img/cat.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.children, None)
        self.assertDictEqual(html_node.props, {"src": "/img/cat.png", "alt": "Cat"})
        self.assertEqual(
            html_node.to_html(),
            "<img src=\"/img/cat.png\" alt=\"Cat\"></img>")

    def test_exception(self):
        
        text_node = TextNode("Broken", "None")    

        self.assertRaises(ValueError, text_node_to_html_node, text_node)
        try:
            text_node_to_html_node(text_node)
        except ValueError as e:
            self.assertEqual(str(e), "Unrecognised type")
            
    
    # def test_empty(self):
    #     node = HTMLNode()
    #     self.assertEqual(node.tag, None)
    #     self.assertEqual(node.value, None)
    #     self.assertEqual(node.children, None)
    #     self.assertEqual(node.props, None)

    # def test_not_equal(self):
    #     node = HTMLNode("p", "Test", props={"style":"color:green"})
    #     node2 = HTMLNode("h1", "Test", props={"style":"color:green"})
    #     self.assertNotEqual(node, node2)

    # def test_props(self):
    #     node = HTMLNode("p", "Test", props={"style":"color:green"})
    #     expected = f" style=\"color:green\""
    #     actual = node.props_to_html()
    #     self.assertEqual(expected,  actual)
    
    # def test_props_none(self):
    #     node = HTMLNode("p", "Test")
    #     expected = ""
    #     actual = node.props_to_html()
    #     self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()