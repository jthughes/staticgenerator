import unittest

from textnode import TextNode, TextType


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



if __name__ == "__main__":
    unittest.main()