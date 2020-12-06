#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from novelconverter.parser import build_inlineparser, build_blockparser


class TestInlineParser(unittest.TestCase):
    """Test class of novelconverter.inlineparser."""

    def setUp(self):
        self.inlineparser = build_inlineparser()

    # Add parser function

    # def test_run(self):
    #   source = ""
    #   result = ""
    #   self.assertEqual(result, self.inlineparser.run(source))


class TestBlockParser(unittest.TestCase):
    """Test class of novelconverter.blockparser."""

    def setUp(self):
        self.blockparser = build_blockparser()

    # Add parser function

    def test_para(self):
        source = 't1\nt2\nt3{"type": "hoge", "result": ["t4-1", "t4-2"]}t5'
        result = {
            "type": "para",
            "content": [
                "t1",
                "t2",
                [
                    "t3",
                    {"type": "hoge", "result": ["t4-1", "t4-2"]},
                    "t5"
                ],
            ]
        }
        self.assertEqual(result, self.blockparser.reg["para"](source))

    def test_run(self):
        source = 't1\nt2\nt3{"type": "hoge", "result": ["t4-1", "t4-2"]}t5\nt6'
        result = {
            "type": "para",
            "content": [
                "t1",
                "t2",
                [
                    "t3",
                    {"type": "hoge", "result": ["t4-1", "t4-2"]},
                    "t5",
                ],
                "t6"
            ]
        }
        self.assertEqual(result, self.blockparser.run(source))


if __name__ == "__main__":
    unittest.main()
