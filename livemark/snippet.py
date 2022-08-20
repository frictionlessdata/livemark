from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List, Dict, Any

if TYPE_CHECKING:
    from .document import Document


# TODO:
# We can parse json/yaml in advance for snippet-processing plugins


class Snippet:
    """Livemark snippet

    Parameters:
        input: textual snippet for the snippet
        header: an array of the snippet's header

    """

    def __init__(self, input: str, *, header: List[str]):
        lang = ""
        type = ""
        props = {}

        # Infer lang
        if len(header) >= 1:
            lang = header[0].lower()

        # Infer type/props
        for index, item in enumerate(header[1:]):
            if index == 0 and "=" not in item:
                type = item
                continue
            parts = item.split("=")
            name = parts[0].lower()
            value = parts[1] if len(parts) == 2 else True
            props[name] = value

        # Set attributes
        self.__input = input
        self.__header = header
        self.__output = None
        self.__lang = lang
        self.__type = type
        self.__props = props

    def __setattr__(self, name, value):
        if name == "output":
            self.__output = value
        elif name == "input":
            self.__input = value
        elif name == "lang":
            self.__lang = value
        elif name == "type":
            self.__type = value
        else:  # default setter
            super().__setattr__(name, value)

    @property
    def input(self) -> str:
        """Snippet's input"""
        return self.__input

    @property
    def output(self) -> Optional[str]:
        """Snippet's output"""
        return self.__output

    @property
    def header(self) -> List[str]:
        """Snippet's header"""
        return self.__header

    @property
    def lang(self) -> str:
        """Snippet's lang"""
        return self.__lang

    @property
    def type(self) -> str:
        """Snippet's type

        Returns:
            str: type
        """
        return self.__type

    @property
    def props(self) -> Dict[str, Any]:
        """Snippet's props"""
        return self.__props

    # Process

    def process(self, document: Document) -> None:
        """Process snippet

        Parameters:
            document: document having this snippet
        """
        for plugin in document.plugins:
            plugin.process_snippet(self)
