import unittest

from parentnode import ParentNode
from leafnode import LeafNode
    
class TestParentNode(unittest.TestCase):
    def test_single_child(self):
        leaf1 = LeafNode("b","Greetings!")

        node = ParentNode("p", children=[leaf1], props={"style":"color:green"})
        self.assertEqual(
            node.to_html(),
            "<p style=\"color:green\"><b>Greetings!</b></p>")

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


if __name__ == "__main__":
    unittest.main()