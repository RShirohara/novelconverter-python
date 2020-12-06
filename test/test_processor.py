#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from novelconverter.processor import build_postprocessor, build_preprocessor


class TestPreProcessor(unittest.TestCase):
    """Test class of novelconverter.preprocessor."""

    def setUp(self):
        self.processor = build_preprocessor()

    # Add processor function

    # def test_func(self):
    #   source = ""
    #   result = ""
    #   self.assertEqual(result, self.processor.reg[func_name](source))


class TestPostProcessor(unittest.TestCase):
    """Test class of novelconverter.postprocessor."""

    def setUp(self):
        self.processor = build_postprocessor()

    # Add processor function

    # def test_func(self):
    #   source = ""
    #   result = ""
    #   self.assertEqual(result, self.processor.reg[func_name](source))


if __name__ == "__main__":
    unittest.main()
