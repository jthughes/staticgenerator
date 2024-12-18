import unittest

from nodes import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal(self):
        node = TextNode("A", TextType.BOLD, "C")
        node1 = TextNode("A", TextType.BOLD)
        self.assertNotEqual(node, node1)
        node2 = TextNode("A", TextType.LINK, "C")
        self.assertNotEqual(node, node2)
        node3 = TextNode("B", TextType.BOLD, "C")
        self.assertNotEqual(node, node3)
        node4 = TextNode("D", TextType.IMAGE, "E")
        self.assertNotEqual(node, node4)

    def test_repr(self):
        node = TextNode("Hello there!", TextType.CODE)
        self.assertEqual(
            str(node),
            "TextNode(Hello there!, code, None)"
        )

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

    def test_to_html_exception(self):
        def test_raise(object, exception: Exception, function, exception_message):
            object.assertRaises(exception, function)
            try:
                function()
            except exception as e:
                object.assertEqual(str(e), exception_message)
        
        node = HTMLNode("p", "Test")
        test_raise(self, NotImplementedError, node.to_html, "")

class TestParentNode(unittest.TestCase):
    def test_single_child(self):
        leaf1 = LeafNode("b","Greetings!")

        node = ParentNode("p", children=[leaf1], props={"style":"color:green"})
        self.assertEqual(
            node.to_html(),
            "<p style=\"color:green\"><b>Greetings!</b></p>")
        self.assertEqual(
            str(node),
            "HTMLNode(p, None, [HTMLNode(b, Greetings!, None, None)], {'style': 'color:green'})"
        )

    def test_multiple_children(self):
        leaf1 = LeafNode("b","Greetings!")
        leaf2 = LeafNode(None, "How are you?")
        node = ParentNode("p", children=[leaf1, leaf2], props={"style":"color:green"})
        self.assertEqual(
            node.to_html(),
            "<p style=\"color:green\"><b>Greetings!</b>How are you?</p>")

    def test_nested_parents(self):
        leaf1 = LeafNode("h1", "Search")
        leaf2 = LeafNode("a", "here", {"href": "google.com"})
        leaf3 = LeafNode(None, "You can search the internet ")
        parent2 = ParentNode("p", [leaf3, leaf2])
        parent1 = ParentNode("body", [leaf1, parent2])
        self.assertEqual(
            parent1.to_html(),
            "<body><h1>Search</h1><p>You can search the internet <a href=\"google.com\">here</a></p></body>"
        )

    def test_exceptions(self):
        def test_raise(object, exception: Exception, function, exception_message):
            object.assertRaises(exception, function)
            try:
                function()
            except exception as e:
                object.assertEqual(str(e), exception_message)

        leaf = LeafNode("p", "Irrelevant")
        node = ParentNode(None, [leaf])
        test_raise(self, ValueError, node.to_html, "No tag set")
        node = ParentNode("h1", None) 
        test_raise(self, ValueError, node.to_html, "No children set")
        node = ParentNode("h2", [])
        test_raise(self, ValueError, node.to_html, "Empty children list")

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "Test", {"style":"color=green"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Test")
        self.assertEqual(node.children, None)
        self.assertDictEqual(node.props, {"style": "color=green"})

    def test_empty(self):
        node = LeafNode(None, "This is raw text")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "This is raw text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_not_equal(self):
        node = LeafNode("p", "Test", {"style":"color=green"})
        node2 = LeafNode("h1", "Test", {"style":"color=green"})
        self.assertNotEqual(node, node2)

    def test_props(self):
        node = LeafNode("p", "Test", {"style":"color=green"})
        expected = f" style=\"color=green\""
        actual = node.props_to_html()
        self.assertEqual(expected,  actual)
    
    def test_props_none(self):
        node = LeafNode("p", "Test")
        expected = ""
        actual = node.props_to_html()
        self.assertEqual(expected, actual)

    def test_to_html_simple(self):
        node = LeafNode("p", "This is a test")
        self.assertEqual(node.to_html(), "<p>This is a test</p>")

    def test_to_html_complex(self):
        node = LeafNode("h1", "My heading", {"href": "localhost"})
        self.assertEqual(node.to_html(), "<h1 href=\"localhost\">My heading</h1>")

    def test_raw_with_props(self):
        node = LeafNode(None, "What if I tag this?", {"size":"large"})
        self.assertEqual(node.to_html(), "What if I tag this?")

    def test_str(self):
        node = LeafNode("i", "aka em")
        self.assertEqual(str(node), "HTMLNode(i, aka em, None, None)")

    def test_exceptions(self):
        def test_raise(object, exception: Exception, function, exception_message):
            object.assertRaises(exception, function)
            try:
                function()
            except exception as e:
                object.assertEqual(str(e), exception_message)

        node = LeafNode("p", None)
        test_raise(self, ValueError, node.to_html, "No value set")

class TestTextoHTMLNodeFunction(unittest.TestCase):
    def test_normal(self):
        text_node = TextNode("Grey skys", TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Grey skys")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)
        self.assertEqual(
            html_node.to_html(),
            "Grey skys")
        
    def test_bold(self):
        text_node = TextNode("Test", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b", "Incorrect Tag")
        self.assertEqual(html_node.value, "Test", "Incorrect Value")
        self.assertEqual(html_node.children, None, "Incorrect Children")
        self.assertEqual(html_node.props, None, "Incorrect Props")
        self.assertEqual(html_node.to_html(), "<b>Test</b>", "Incorrect to_html() return")

    def test_italic(self):
        text_node = TextNode("aka em", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "aka em")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)
        self.assertEqual(
            html_node.to_html(),
            "<i>aka em</i>")

    def test_code(self):
        text_node = TextNode("print(\"Hello world!\")", TextType.CODE, "/img/cat.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print(\"Hello world!\")")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)
        self.assertEqual(
            html_node.to_html(),
            "<code>print(\"Hello world!\")</code>")

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



if __name__ == "__main__":
    unittest.main()