"""The test module of novelconverter.processor"""

from novelconverter.processor import apply_processor


def convert_linebreaks(source: str) -> str:
    return source.replace("\r", "\n")


def convert_spaces(source: str) -> str:
    return source.replace("　", " ")


class TestApplyProcessor:
    """Test processor.apply_processor"""

    def test(self) -> None:
        source: str = "\rたとえばわたしは\rこの文章を書く。\n\r　これは 最後の　文字。"
        expected: str = "\nたとえばわたしは\nこの文章を書く。\n\n これは 最後の 文字。"

        processors = {"LineBreak": convert_linebreaks, "Space": convert_spaces}

        assert apply_processor(source, processors) == expected
