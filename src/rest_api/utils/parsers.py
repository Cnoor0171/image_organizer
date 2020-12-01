"""Custom argument parser classes"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional

FilterType = List[str]
FieldKeyType = Optional[str]
FieldType = Dict[FieldKeyType, "_SubTree"]


@dataclass
class _SubTree:
    filters: Optional[FilterType] = None
    fields: Optional[FieldType] = None


class OptFields:
    """
    Parses optional fields specifiers

    Input string must be a comma seperated list of optional fields. Whitespace is ignored.
        eg: "thisField, thatField"

    Each optional field can have a list of filters attached to it, surrounded by "[ ]".
        eg: "thisField[1,2,3], thatField"

    Each optional field can have nested optional fields, surrounded by "{ }".
        eg: "thisField{nestedField}, thatField"

    Both filters and nested optional fields can be combined.
        eg: "thisField[1,2]{nestedField}, thatField"
    """

    LEXER = re.compile(r"\s*([,\{\}\[\]])\s*")
    IGNORED_TOKENS = (",", "")
    NESTING_TOKENS = {
        "[": "]",
        "{": "}",
    }

    def __init__(self, input_str=""):
        tokens = self.LEXER.split(input_str)
        self.fields = self._build_fields(tokens)

    def _build_fields(self, tokens: List[str]) -> FieldType:
        fields: FieldType = {}
        nested_tokens: List[str] = []
        curr_field = None
        start_sub_tree = 0
        for idx, token in enumerate(tokens):
            if token in self.IGNORED_TOKENS:
                continue
            elif token in self.NESTING_TOKENS.keys():
                if not nested_tokens:
                    start_sub_tree = idx
                nested_tokens.append(token)
            elif token in self.NESTING_TOKENS.values():
                if not nested_tokens:
                    pos = self._get_pos(tokens, start_sub_tree)
                    raise ValueError(f"Unbalanced nested token at position {pos}")
                popped = nested_tokens.pop()
                if token != self.NESTING_TOKENS[popped]:
                    pos = self._get_pos(tokens, start_sub_tree)
                    raise ValueError(f"Unbalanced nested token at position {pos}")
                if not nested_tokens:
                    if token == "]":
                        fields[curr_field].filters = self._build_filter(
                            tokens[start_sub_tree + 1 : idx]
                        )
                    elif token == "}":
                        fields[curr_field].fields = self._build_fields(
                            tokens[start_sub_tree + 1 : idx]
                        )
            elif not nested_tokens:
                curr_field = token
                fields[curr_field] = _SubTree()
        if nested_tokens:
            pos = self._get_pos(tokens, start_sub_tree)
            raise ValueError(f"Unbalanced nested token at position {pos}")
        return dict(fields)

    def _build_filter(self, tokens: List[str]):
        return [token for token in tokens if token not in self.IGNORED_TOKENS]

    def _get_pos(self, tokens: List[str], token_idx):
        position = 0
        for token in tokens[0:token_idx]:
            position += len(token)
        return position
