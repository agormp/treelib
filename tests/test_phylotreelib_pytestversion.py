import phylotreelib as pt
import pytest
import random

###################################################################################################
###################################################################################################

# Tests for loose functions

###################################################################################################
###################################################################################################

class Test_remove_comments:

    def test_balanced(self):
        text = 'Hello [comment] World!\n[newline]'
        assert pt.remove_comments(text) == 'Hello  World!\n'

    def test_unbalanced(self):
        text = 'Hello [comment World!\n[newline'
        with pytest.raises(pt.TreeError):
            pt.remove_comments(text)

    def test_nested_comments(self):
        text = 'Hello [outer [inner] comment] World!'
        assert pt.remove_comments(text) == 'Hello  World!'

###################################################################################################
###################################################################################################

# Tests for Interner class

###################################################################################################
###################################################################################################

# How to do this? Probably need to instantiate relevant classes and add items to interner
# and then check that different items point to same object in memory, but how?

###################################################################################################
###################################################################################################

# Tests for Branchstruct class

###################################################################################################
###################################################################################################

class Test_init_Branchstruct:

    def test_attribute_assignment(self):
        mylength = 0.1543
        mylabel = "0.95"
        branch = pt.Branchstruct(length=mylength, label=mylabel)
        assert branch.length == mylength
        assert branch.label == mylabel

class Test_copy_Branchstruct:
    def test_copy(self):
        mylength = 0.1543
        mylabel = "0.9965"
        b1 = pt.Branchstruct(length=mylength, label=mylabel)
        b1.myatt1 = "howdy"
        b1.myatt2 = 0.34984
        b1.myatt3 =  {1:1, 2:4, 3:9}
        b2 = b1.copy()
        assert b1.length == b2.length
        assert b1.label == b2.label
        assert b1.myatt1 == b2.myatt1
        assert b1.myatt2 == b2.myatt2
        assert b1.myatt3 == b2.myatt3
        assert b1.myatt3 is not b2.myatt3  # Deepcopy

###################################################################################################
###################################################################################################

# Tests for Topostruct class

###################################################################################################
###################################################################################################

class Test_create_Topostruct:

    def test_attributes(self):
        ts = pt.Topostruct()
        w = 0.345
        t = "(A,(B,(C,D)));"  # not actually a tree but fine for testing...
        f = 0.97
        x = "not supposed to be an attribute"
        # Note: main test here is to see if class accepts (only) attribues named in __slots__
        # Assertion is done implicitly: if exception is raised here then test fails
        ts.weight = w
        ts.tree = t
        ts.freq = f
        with pytest.raises(AttributeError):
            ts.notanatt = x

###################################################################################################
###################################################################################################

# Tests for Tree class

###################################################################################################
###################################################################################################

class Test_from_string:
    def test_parse_simplestring(self, treedata):
        treestring = treedata["simplestring"]
        assert isinstance(pt.Tree.from_string(treestring), pt.Tree)

    def test_parse_blanks(self, treedata):
        treestring = treedata["string_with_blanks"]
        assert isinstance(pt.Tree.from_string(treestring), pt.Tree)

    def test_parse_newline(self, treedata):
        treestring = treedata["string_with_newlines"]
        assert isinstance(pt.Tree.from_string(treestring), pt.Tree)

    def test_parse_label(self, treedata):
        treestring = treedata["string_with_label"]
        assert isinstance(pt.Tree.from_string(treestring), pt.Tree)

    def test_parse_complexstring(self, treedata):
        treestring = treedata["complexstring"]
        assert isinstance(pt.Tree.from_string(treestring), pt.Tree)

    def test_parse_spuriousnewlines(self, treedata):
        treestring = treedata["string_with_weird_newlines"]
        assert isinstance(pt.Tree.from_string(treestring), pt.Tree)

    def test_return_correct(self, treedata):
        treestring = treedata["string_with_label"]
        mytree = pt.Tree.from_string(treestring)
        expected_leaves = {"KL0F07689", "KW081_13", "SBC669_26", "YAL016W"}
        expected_intnodes = {0, 1}
        expected_nodes = expected_leaves | expected_intnodes

        assert mytree.leaves == expected_leaves
        assert mytree.intnodes == expected_intnodes
        assert mytree.nodes == expected_nodes
        assert mytree.children(0) == {1, "KL0F07689", "KW081_13"}
        assert mytree.children(1) == {"SBC669_26", "YAL016W"}


