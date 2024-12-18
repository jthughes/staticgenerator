import unittest

from inline_functions import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes(self):
        message = "This is text with a **bolded phrase** in the middle"
        input = TextNode(message, TextType.NORMAL)
        output = split_nodes_delimiter([input], "**", TextType.BOLD)
        self.assertEqual(len(output), 3)
        self.assertEqual(str(output[0]), "TextNode(This is text with a , normal, None)")
        self.assertEqual(str(output[1]), "TextNode(bolded phrase, bold, None)")
        self.assertEqual(str(output[2]), "TextNode( in the middle, normal, None)")

    def test_split_nodes_long(self):
        message = "Hi *there* how *are you?* I *am *well *!!!"
        input = TextNode(message, TextType.NORMAL)
        output = split_nodes_delimiter([input], "*", TextType.ITALIC)
        self.assertEqual(len(output), 7)
        self.assertEqual(str(output[0]), "TextNode(Hi , normal, None)")
        self.assertEqual(str(output[1]), "TextNode(there, italic, None)")
        self.assertEqual(str(output[2]), "TextNode( how , normal, None)")
        self.assertEqual(str(output[3]), "TextNode(are you?, italic, None)")
        self.assertEqual(str(output[4]), "TextNode( I , normal, None)")
        self.assertEqual(str(output[5]), "TextNode(am , italic, None)")
        self.assertEqual(str(output[6]), "TextNode(well *!!!, normal, None)")

    def test_split_nodes_different(self):
        message = "**Bold**Normal``Code``*Italic***bold**"
        input = TextNode(message, TextType.NORMAL)
        output1 = split_nodes_delimiter([input], "**", TextType.BOLD)
        output2 = split_nodes_delimiter(output1, "*", TextType.ITALIC)
        output = split_nodes_delimiter(output2, "``", TextType.CODE)
        self.assertEqual(len(output), 5)
        self.assertEqual(str(output[0]), "TextNode(Bold, bold, None)")
        self.assertEqual(str(output[1]), "TextNode(Normal, normal, None)")
        self.assertEqual(str(output[2]), "TextNode(Code, code, None)")
        self.assertEqual(str(output[3]), "TextNode(*Italic, normal, None)")
        self.assertEqual(str(output[4]), "TextNode(*bold, bold, None)")

    def test_split_nodes_different_v2(self):
        message = "**Bold**Normal``Code``*Italic* **bold**"
        input = TextNode(message, TextType.NORMAL)
        output1 = split_nodes_delimiter([input], "**", TextType.BOLD)
        output2 = split_nodes_delimiter(output1, "*", TextType.ITALIC)
        output = split_nodes_delimiter(output2, "``", TextType.CODE)
        self.assertEqual(len(output), 6)
        self.assertEqual(str(output[0]), "TextNode(Bold, bold, None)")
        self.assertEqual(str(output[1]), "TextNode(Normal, normal, None)")
        self.assertEqual(str(output[2]), "TextNode(Code, code, None)")
        self.assertEqual(str(output[3]), "TextNode(Italic, italic, None)")
        self.assertEqual(str(output[4]), "TextNode( , normal, None)")
        self.assertEqual(str(output[5]), "TextNode(bold, bold, None)")


class TestSplitNodesImage(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        output = extract_markdown_images(text)
        self.assertEqual(len(output), 2)
        self.assertTupleEqual(output[0], ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'))
        self.assertTupleEqual(output[1], ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg'))

    def test_extract_markdown_images_not_links(self):
        text = "This has an ![image](https://i.imgur.com/aKaOqIh.gif) and a [link](https://www.boot.dev)"
        output = extract_markdown_images(text)
        self.assertEqual(len(output), 1)
        self.assertTupleEqual(output[0], ('image', 'https://i.imgur.com/aKaOqIh.gif'))
        


class TestSplitNodesLink(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        output = extract_markdown_links(text)
        self.assertEqual(len(output), 2)
        self.assertTupleEqual(output[0], ('to boot dev', 'https://www.boot.dev'))
        self.assertTupleEqual(output[1], ('to youtube', 'https://www.youtube.com/@bootdotdev'))

    def test_extract_markdown_links_not_images(self):
        text = "This has an ![image](https://i.imgur.com/aKaOqIh.gif) and a [link](https://www.boot.dev)"
        output = extract_markdown_links(text)
        self.assertEqual(len(output), 1)
        self.assertTupleEqual(output[0], ('link', 'https://www.boot.dev'))


if __name__ == "__main__":
    unittest.main()