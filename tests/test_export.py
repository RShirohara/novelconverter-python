# -*- coding: utf-8 -*-
# author: RShirohara

import unittest

import novelconverter


class TestExport(unittest.TestCase):
    def test_ddmarkdown(self):
        """Test method for ddmarkdown"""
        # Load data
        with open("tests/data/ddmarkdown/ddmarkdown.txt", "r") as _file:
            data = _file.read()

        with self.subTest("to_markdown"):
            # Load converted data
            with open("tests/data/ddmarkdown/to_markdown.txt", "r") as _file:
                _expected = _file.read()
            _actual = novelconverter.convert(
                data, "ddmarkdown", "markdown")
            self.assertEqual(_expected, _actual)

        with self.subTest("to_pixiv"):
            # Load converted data
            with open("tests/data/ddmarkdown/to_pixiv.txt", "r") as _file:
                _expected = _file.read()
            _actual = novelconverter.convert(
                data, "ddmarkdown", "pixiv")
            self.assertEqual(_expected, _actual)

        with self.subTest("to_plain"):
            # Load converted data
            with open("tests/data/ddmarkdown/to_plain.txt", "r") as _file:
                _expected = _file.read()
            _actual = novelconverter.convert(
                data, "ddmarkdown", "plain")
            self.assertEqual(_expected, _actual)

    def test_markdown(self):
        """Test method for markdown"""
        # Load data
        with open("tests/data/markdown/markdown.txt", "r") as _file:
            data = _file.read()

        with self.subTest("to_ddmarkdown"):
            # Load converted data
            with open("tests/data/markdown/to_ddmarkdown.txt", "r") as _file:
                _expected = _file.read()
            _actual = novelconverter.convert(
                data, "markdown", "markdown")
            self.assertEqual(_expected, _actual)

        with self.subTest("to_pixiv"):
            # Load converted data
            with open("tests/data/markdown/to_pixiv.txt", "r") as _file:
                _expected = _file.read()
            _actual = novelconverter.convert(
                data, "markdown", "pixiv")
            self.assertEqual(_expected, _actual)

        with self.subTest("to_plain"):
            # Load converted data
            with open("tests/data/markdown/to_plain.txt", "r") as _file:
                _expected = _file.read()
            _actual = novelconverter.convert(
                data, "markdown", "plain")
            self.assertEqual(_expected, _actual)

    def test_pixiv(self):
        """Test method for pixiv"""
        # Load data
        with open("tests/data/pixiv/pixiv.txt", "r") as _file:
            data = _file.read()

        with self.subTest("to_ddmarkdown"):
            # Load converted data
            with open("tests/data/pixiv/to_ddmarkdown.txt", "r") as _file:
                _expected = _file.read()
            _actual = novelconverter.convert(
                data, "pixiv", "markdown")
            self.assertEqual(_expected, _actual)

        with self.subTest("to_markdown"):
            # Load converted data
            with open("tests/data/pixiv/to_markdown.txt", "r") as _file:
                _expected = _file.read()
            _actual = novelconverter.convert(
                data, "pixiv", "markdown")
            self.assertEqual(_expected, _actual)

        with self.subTest("to_plain"):
            # Load converted data
            with open("tests/data/pixiv/to_plain.txt", "r") as _file:
                _expected = _file.read()
            _actual = novelconverter.convert(
                data, "pixiv", "plain")
            self.assertEqual(_expected, _actual)


if __name__ == "__main__":
    unittest.main()
