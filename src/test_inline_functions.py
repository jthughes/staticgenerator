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

    def test_nested(self):
        message = "Hi **there how *are* you?**"
        input = TextNode(message, TextType.NORMAL)
        output1 = split_nodes_delimiter([input], "**", TextType.BOLD)
        output2 = split_nodes_delimiter(output1, "*", TextType.ITALIC)
        self.assertEqual(len(output2), 2)
        self.assertEqual(str(output2[0]), "TextNode(Hi , normal, None)")
        self.assertEqual(str(output2[1]), "TextNode(there how *are* you?, bold, None)")

    def test_nested_2(self):
        message = "Hi *there how **are** you?*"
        input = TextNode(message, TextType.NORMAL)
        output1 = split_nodes_delimiter([input], "**", TextType.BOLD)
        output2 = split_nodes_delimiter(output1, "*", TextType.ITALIC)
        self.assertEqual(len(output2), 3)
        self.assertEqual(str(output2[0]), "TextNode(Hi *there how , normal, None)")
        self.assertEqual(str(output2[1]), "TextNode(are, bold, None)")
        self.assertEqual(str(output2[2]), "TextNode( you?*, normal, None)")


class TestExtractMarkdownImages(unittest.TestCase):
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

    def test_extract_markdown_images_no_alt(self):
        text = "Test ![](boot.jpg)"
        output = extract_markdown_images(text)
        self.assertEqual(len(output), 1)
        self.assertTupleEqual(output[0], ('', 'boot.jpg'))
    
    def test_extract_markdown_images_no_src(self):
        text = "Test ![alt]()"
        output = extract_markdown_images(text)
        self.assertEqual(len(output), 0)
    
    def test_extract_markdown_images_empty(self):
        text = "Test ![]()"
        output = extract_markdown_images(text)
        self.assertEqual(len(output), 0)

    def test_extrac_markdown_images_nested(self):
        text = "This ![![image](https://i.imgur.com/aKaOqIh.gif)](a.b)"
        output = extract_markdown_images(text)
        self.assertEqual(len(output), 1)
        self.assertTupleEqual(output[0], ('![image', 'https://i.imgur.com/aKaOqIh.gif'))

    def test_extrac_markdown_images_nested_2(self):
        text = "This [![image](https://i.imgur.com/aKaOqIh.gif)]"
        output = extract_markdown_images(text)
        self.assertEqual(len(output), 1)
        self.assertTupleEqual(output[0], ('image', 'https://i.imgur.com/aKaOqIh.gif'))


class TestSplitNodesImage(unittest.TestCase):
    def test_split_simple_image(self):
        node = TextNode("![Image](cat.png)", TextType.NORMAL)
        output = split_nodes_image([node])
        self.assertEqual(len(output), 1)
        self.assertEqual(str(output[0]), "TextNode(Image, image, cat.png)")

    def test_split_simple_image_1(self):
        node = TextNode("Test ![Image](cat.png)", TextType.NORMAL)
        output = split_nodes_image([node])
        self.assertEqual(len(output), 2)
        self.assertEqual(str(output[0]), "TextNode(Test , normal, None)")
        self.assertEqual(str(output[1]), "TextNode(Image, image, cat.png)")

    def test_split_simple_image_2(self):
        node = TextNode("Test ![Image](cat.png) image ![img2](dog.png)![img3](fish.png)blah", TextType.NORMAL)
        output = split_nodes_image([node])
        self.assertEqual(len(output), 6)
        self.assertEqual(str(output[0]), "TextNode(Test , normal, None)")
        self.assertEqual(str(output[1]), "TextNode(Image, image, cat.png)")
        self.assertEqual(str(output[2]), "TextNode( image , normal, None)")
        self.assertEqual(str(output[3]), "TextNode(img2, image, dog.png)")
        self.assertEqual(str(output[4]), "TextNode(img3, image, fish.png)")
        self.assertEqual(str(output[5]), "TextNode(blah, normal, None)")

    def test_split_image_wrong_type(self):
        node = TextNode("Test", TextType.BOLD)
        output = split_nodes_image([node])
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], node)

    def test_split_image_with_link(self):
        node = TextNode("[hi](google.com)", TextType.NORMAL)
        output = split_nodes_image([node])
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], node)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        output = extract_markdown_links(text)
        self.assertEqual(len(output), 2)
        self.assertTupleEqual(output[0], ('to boot dev', 'https://www.boot.dev'))
        self.assertTupleEqual(output[1], ('to youtube', 'https://www.youtube.com/@bootdotdev'))

    def test_extract_markdown_links_not_links(self):
        text = "This has an ![image](https://i.imgur.com/aKaOqIh.gif) and a [link](https://www.boot.dev)"
        output = extract_markdown_links(text)
        self.assertEqual(len(output), 1)
        self.assertTupleEqual(output[0], ('link', 'https://www.boot.dev'))

    def test_extract_markdown_links_no_alt(self):
        text = "Test [](boot.jpg)"
        output = extract_markdown_links(text)
        self.assertEqual(len(output), 0)
    
    def test_extract_markdown_links_no_src(self):
        text = "Test [alt]()"
        output = extract_markdown_links(text)
        self.assertEqual(len(output), 0)
    
    def test_extract_markdown_links_empty(self):
        text = "Test []()"
        output = extract_markdown_links(text)
        self.assertEqual(len(output), 0)

    def test_extrac_markdown_links_nested(self):
        text = "This [[link](https://i.imgur.com/aKaOqIh.gif)](a.b)"
        output = extract_markdown_links(text)
        self.assertEqual(len(output), 1)
        self.assertTupleEqual(output[0], ('[link', 'https://i.imgur.com/aKaOqIh.gif'))

    def test_extrac_markdown_links_nested_2(self):
        text = "This [[link](https://i.imgur.com/aKaOqIh.gif)]"
        output = extract_markdown_links(text)
        self.assertEqual(len(output), 1)
        self.assertTupleEqual(output[0], ('[link', 'https://i.imgur.com/aKaOqIh.gif'))


class TestSplitNodesLink(unittest.TestCase):
    def test_split_simple_link(self):
        node = TextNode("[Link](boot.dev)", TextType.NORMAL)
        output = split_nodes_link([node])
        self.assertEqual(len(output), 1)
        self.assertEqual(str(output[0]), "TextNode(Link, link, boot.dev)")

    def test_split_simple_link_1(self):
        node = TextNode("Test [Link](boot.dev)", TextType.NORMAL)
        output = split_nodes_link([node])
        self.assertEqual(len(output), 2)
        self.assertEqual(str(output[0]), "TextNode(Test , normal, None)")
        self.assertEqual(str(output[1]), "TextNode(Link, link, boot.dev)")

    def test_split_simple_link_2(self):
        node = TextNode("Test [Link](boot.dev)[Link2](google.com)", TextType.NORMAL)
        output = split_nodes_link([node])
        self.assertEqual(len(output), 3)
        self.assertEqual(str(output[0]), "TextNode(Test , normal, None)")
        self.assertEqual(str(output[1]), "TextNode(Link, link, boot.dev)")
        self.assertEqual(str(output[2]), "TextNode(Link2, link, google.com)")

    def test_split_deceptive_link(self):
        node = TextNode("Test ![Link](boot.dev)[Link](boot.dev)![Link](boot.dev) Blah", TextType.NORMAL)
        output = split_nodes_link([node])
        self.assertEqual(len(output), 3)
        self.assertEqual(str(output[0]), "TextNode(Test ![Link](boot.dev), normal, None)")
        self.assertEqual(str(output[1]), "TextNode(Link, link, boot.dev)")
        self.assertEqual(str(output[2]), "TextNode(![Link](boot.dev) Blah, normal, None)")

    def test_split_link_empty(self):
        node = TextNode("Hey!", TextType.NORMAL)
        output = split_nodes_link([node])
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], node)

    def test_split_link_no_text(self):
        node = TextNode("Hey!", TextType.BOLD)
        output = split_nodes_link([node])
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], node)


class TestTextToTextNodes(unittest.TestCase):
    def test_boot_dev_example(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = text_to_textnodes(text)
        expected_output = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(output, expected_output)

    def test_format_in_code(self):
        text = "```*bold*```"
        output = text_to_textnodes(text)
        self.assertEqual(len(output), 1)
        self.assertEqual(str(output[0]), "TextNode(*bold*, code, None)")

    def test_code_blocks(self):
        text = "``blah```blah2```blah3`"
        output = text_to_textnodes(text)
        self.assertEqual(len(output), 3)
        self.assertEqual(str(output[0]), "TextNode(``blah, normal, None)")
        self.assertEqual(str(output[1]), "TextNode(blah2, code, None)")
        self.assertEqual(str(output[2]), "TextNode(blah3`, normal, None)")

    # This will need to change if supporting proper nesting in future
    def test_overlap(self):
        text = "*Hello [link*](boot.dev)"
        output = text_to_textnodes(text)
        self.assertEqual(len(output), 2)
        self.assertEqual(str(output[0]), "TextNode(*Hello , normal, None)")
        self.assertEqual(str(output[1]), "TextNode(link*, link, boot.dev)")


if __name__ == "__main__":
    unittest.main()