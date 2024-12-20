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

class TestBlockToBlockType(unittest.TestCase):
    def test_empty(self):
        output = block_to_block_type("")
        output1 = block_to_block_type(None)
        self.assertEqual(output, None)
        self.assertEqual(output1, None)

    def test_header(self):
        block = " Header"
        for i in range(6):
            block = f"#{block}"
            output = block_to_block_type(block)
            self.assertEqual(output, "heading")
    
    def test_header_no_space(self):
        block = "Header"
        for i in range(6):
            block = f"#{block}"
            output = block_to_block_type(block)
            self.assertEqual(output, "paragraph")
    
    def test_header_no_space_no_text(self):
        block = ""
        for i in range(6):
            block = f"#{block}"
            output = block_to_block_type(block)
            self.assertEqual(output, "paragraph")

    def test_header_no_text(self):
        block = "# "
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

    def test_header_level_7(self):
        block = "####### Header"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")
    
    def test_code(self):
        block = "```code```"
        output = block_to_block_type(block)
        self.assertEqual(output, "code")

    def test_code_1(self):
        block = "```code``"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

    def test_code_2(self):
        block = "``````code``"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")
    
    def test_code_3(self):
        block = "``````"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

    def test_code_4(self):
        block = "`````"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

    def test_quote_0(self):
        block = ">"
        output = block_to_block_type(block)
        self.assertEqual(output, "quote")

    def test_quote_1(self):
        block = ">\n>Hi"
        output = block_to_block_type(block)
        self.assertEqual(output, "quote")

    def test_quote_2(self):
        block = ">Hi\nHow are you?\n>Good thanks"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

    def test_unordered_0(self):
        block = "- list!"
        output = block_to_block_type(block)
        self.assertEqual(output, "unordered_list")

    def test_unordered_1(self):
        block = "* list!"
        output = block_to_block_type(block)
        self.assertEqual(output, "unordered_list")

    def test_unordered_2(self):
        block = "- list!\n* 2\n- 3"
        output = block_to_block_type(block)
        self.assertEqual(output, "unordered_list")

    def test_unordered_3(self):
        block = "- list!\n2. 2\n- 3"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

    def test_unordered_4(self):
        block = "-list!"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

    def test_unordered_5(self):
        block = "- list!\n2\n- 3"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")
    
    def test_ordered_0(self):
        block = "1. first"
        output = block_to_block_type(block)
        self.assertEqual(output, "ordered_list")

    def test_ordered_1(self):
        block = "1. first\n2. second\n3. third"
        output = block_to_block_type(block)
        self.assertEqual(output, "ordered_list")

    def test_ordered_2(self):
        block = "1. first\n2. second\n 3. third"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

    def test_ordered_3(self):
        block = " 1. first\n2. second\n3. third"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

    def test_ordered_4(self):
        block = ("1. first\n"
                "2. second\n"
                "3. third"
                "4. fourth"
                "5. fifth"
                "6. sixth"
                "7. seventh"
                "8. eight"
                "9. ninth"
                "10. tenth")
        output = block_to_block_type(block)
        self.assertEqual(output, "ordered_list")

    def test_ordered_5(self):
        block = "2. first\n3. second\n4. third"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

    def test_ordered_6(self):
        block = "0. first\n1. second\n2. third"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

    def test_ordered_7(self):
        block = "1. first\n1. second\n3. third"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

    def test_ordered_8(self):
        block = "1. first\nsecond\n2. third"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

    def test_ordered_9(self):
        block = "1. first\nsecond\n3. third"
        output = block_to_block_type(block)
        self.assertEqual(output, "paragraph")

if __name__ == "__main__":
    unittest.main()