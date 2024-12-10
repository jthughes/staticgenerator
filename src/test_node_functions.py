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


    def test_split_nodes(self):
        message = "This is text with a **bolded phrase** in the middle"
        input = TextNode(message, TextType.NORMAL)
        output = split_nodes_delimiter([input], "**", TextType.BOLD)
        # print("")
        # print("Input:", input)
        # print("Output:",output)

    def test_split_nodes_long(self):
        message = "Hi *there* how *are you?* I *am *well *!!!"
        input = TextNode(message, TextType.NORMAL)
        output = split_nodes_delimiter([input], "*", TextType.ITALIC)
        # print("")
        # print("Input:", input)
        # print("Output:",output)
    
    def test_split_nodes_different(self):
        message = "**Bold**Normal``Code``*Italic***bold**"
        input = TextNode(message, TextType.NORMAL)
        output = split_nodes_delimiter([input], "**", TextType.BOLD)
        output2 = split_nodes_delimiter(output, "*", TextType.ITALIC)
        output3 = split_nodes_delimiter(output2, "``", TextType.CODE)
        # print("")
        # print("Input:", input)
        # print("Output:",output)
        # print("Output2:",output2)
        # print("Output3:",output3)


    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        print(extract_markdown_images(text))

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        print(extract_markdown_links(text))

if __name__ == "__main__":
    unittest.main()