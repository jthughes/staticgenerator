import unittest

from block_functions import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_demo(self):
        markdown = (
            "# This is a heading\n"
            "\n"
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
            "\n"
            "* This is the first list item in a list block\n"
            "* This is a list item\n"
            "* This is another list item\n"
        )
        output = markdown_to_blocks(markdown)
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0], "# This is a heading")
        self.assertEqual(output[1], "This is a paragraph of text. It has some **bold** and *italic* words inside of it.")
        self.assertEqual(output[2], ("* This is the first list item in a list block\n"
                                    "* This is a list item\n"
                                    "* This is another list item"))
    
    def test_extra_spaces(self):
        markdown = (
            "# Heading\n"
            "\n"
            "\n"
            "body of text\n"
        )
        output = markdown_to_blocks(markdown)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], "# Heading")
        self.assertEqual(output[1], "body of text")

    def test_extra_spaces_2(self):
        markdown = (
            "# Heading\n"
            "\n"
            "\n"
            "\n"
            "body of text\n"
        )
        output = markdown_to_blocks(markdown)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], "# Heading")
        self.assertEqual(output[1], "body of text")

    def test_extra_spaces_3(self):
        markdown = (
            "# Heading\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "body of text\n"
        )
        output = markdown_to_blocks(markdown)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], "# Heading")
        self.assertEqual(output[1], "body of text")

    def test_extra_spaces_4(self):
        markdown = (
            "# Heading\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "body of text\n"
        )
        output = markdown_to_blocks(markdown)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], "# Heading")
        self.assertEqual(output[1], "body of text")

if __name__ == "__main__":
    unittest.main()