"""Run string processor before parsing and after rendering process."""


from typing import Callable

Processor = Callable[[str], str]
ProcessorContainer = dict[str, Processor]


def apply_processor(source: str, processors: ProcessorContainer) -> str:
    """Apply processors to string.

    Args:
        source (str): Source string.
        processors (ProcessorContainer): Name and processor pair.

    Returns:
        str: String with processor applied.
    """

    applied_str: str = source
    for value in processors.values():
        applied_str: str = value(applied_str)
    return applied_str
