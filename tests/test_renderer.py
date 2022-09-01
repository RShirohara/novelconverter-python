"""The test module of novelconverter.renderer."""

from dataclasses import dataclass, field
from pytest import fixture, raises

from novelconverter.renderer import NodeRenderer, RenderError, render
from novelconverter.tree import NovelNode, NovelParentNode, NovelTextNode


@dataclass
class Root(NovelParentNode):
    type: str = field(default="Root", init=False)
    raw: str
    children: tuple[NovelNode, ...]


@dataclass
class NestedList(NovelParentNode):
    type: str = field(default="NestedList", init=False)
    raw: str
    depth: int
    children: tuple[NovelNode, ...]


@dataclass
class Inline(NovelTextNode):
    type: str = field(default="Inline", init=False)
    raw: str
    value: str


def render_root(node: Root, renderers: dict[str, NodeRenderer[NovelNode]]) -> str:
    result: list[str] = []
    for child in node.children:
        if child.type in renderers.keys():
            result.append(renderers[child.type](child, renderers))
        else:
            result.append(child.raw)
    return "\n\n".join(result)


def render_nested_list(
    node: NestedList, renderers: dict[str, NodeRenderer[NovelNode]]
) -> str:
    result: list[str] = []
    for child in node.children:
        if child.type in renderers.keys():
            result.append(renderers[child.type](child, renderers))
        else:
            result.append(child.raw)
    return "\n".join(f"  {res}" for res in result)


def render_inline(node: Inline, renderers: dict[str, NodeRenderer[NovelNode]]) -> str:
    return node.value


@fixture
def document() -> Root:
    """NovelNode tree used by test."""

    return Root(
        raw="Raw string provided by Root.",
        children=(
            Inline(
                raw="Raw string provided by first inline node.",
                value="This is first inline node.",
            ),
            NestedList(
                raw="Raw string provided by NestedList.",
                depth=1,
                children=(
                    Inline(
                        raw="Raw string provided by first nested inline node.",
                        value="This is first nested inline node.",
                    ),
                    Inline(
                        raw="Raw string provided by second nested inline node.",
                        value="This is second nested inline node.",
                    ),
                    NestedList(
                        raw="Raw string provided by doubly nested NestedList.",
                        depth=2,
                        children=(
                            Inline(
                                raw="Raw string provided by doubly nested inline node.",
                                value="This is doubly nested inline node.",
                            ),
                        ),
                    ),
                ),
            ),
            Inline(
                raw="Raw string provided by last inline node.",
                value="This is last inline node.",
            ),
        ),
    )


class TestRender:
    """Test renderer.render"""

    def test_is_all_renderer_contains(self, document: Root) -> None:
        """If all Renderers corresponding to Node exist, render using Renderer."""

        renderers = {
            "Root": render_root,
            "NestedList": render_nested_list,
            "Inline": render_inline,
        }
        actual: str = """This is first inline node.

  This is first nested inline node.
  This is second nested inline node.
    This is doubly nested inline node.

This is last inline node."""

        assert render(document, renderers) == actual

    def test_is_root_renderer_not_contains(self, document: Root) -> None:
        """If Renderer corresponding to Root does not exist, raise RenderError."""

        renderers = {
            "NestedList": render_nested_list,
            "Inline": render_inline,
        }

        with raises(RenderError) as render_error:
            render(document, renderers)

        assert "\n".join(
            (
                "Renderer corresponding to Node does not exist",
                'node: Root, raw: "Raw string provided by Root."',
            )
        ) == str(render_error.value)

    def test_is_child_renderer_not_contains(self, document: Root) -> None:
        """If Renderer corresponding to Children does not exist, render using 'raw' values."""

        renderers = {
            "Root": render_root,
            "Inline": render_inline,
        }
        actual: str = """This is first inline node.

Raw string provided by NestedList.

This is last inline node."""

        assert render(document, renderers) == actual
