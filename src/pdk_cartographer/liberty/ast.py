"""Generic AST nodes for the fixture-first Liberty subset parser."""

from __future__ import annotations

from dataclasses import dataclass, field

LibertyScalar = str | float
LibertyValue = LibertyScalar | tuple[LibertyScalar, ...]


@dataclass(frozen=True)
class SourceLocation:
    """A source location used in parser diagnostics and AST nodes."""

    line: int
    column: int


@dataclass(frozen=True)
class LibertyAttribute:
    """A Liberty attribute such as ``area : 1.40;`` or ``index_1("...");``."""

    name: str
    value: LibertyValue
    location: SourceLocation


@dataclass(frozen=True)
class LibertyGroup:
    """A generic Liberty group with arguments, attributes, and child groups."""

    name: str
    args: tuple[LibertyScalar, ...] = field(default_factory=tuple)
    attributes: dict[str, LibertyAttribute] = field(default_factory=dict)
    groups: tuple[LibertyGroup, ...] = field(default_factory=tuple)
    location: SourceLocation | None = None

    def first_arg_as_string(self) -> str | None:
        """Return the first group argument as text when present."""

        if not self.args:
            return None
        first_arg = self.args[0]
        if isinstance(first_arg, tuple):
            return " ".join(str(part) for part in first_arg)
        return str(first_arg)

    def child_groups(self, name: str) -> tuple[LibertyGroup, ...]:
        """Return direct child groups with the requested Liberty group name."""

        return tuple(group for group in self.groups if group.name == name)
