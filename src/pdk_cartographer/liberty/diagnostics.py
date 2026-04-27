"""Diagnostics for the fixture-first Liberty parser."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LibertyDiagnostic:
    """A small source diagnostic for malformed synthetic Liberty input."""

    message: str
    line: int | None = None
    column: int | None = None

    def format(self) -> str:
        """Return a human-readable diagnostic message."""

        if self.line is None or self.column is None:
            return self.message
        return f"{self.message} at line {self.line}, column {self.column}"


class LibertyError(ValueError):
    """Base class for Liberty lexer/parser errors."""

    def __init__(self, diagnostic: LibertyDiagnostic | str) -> None:
        if isinstance(diagnostic, str):
            diagnostic = LibertyDiagnostic(diagnostic)
        self.diagnostic = diagnostic
        super().__init__(diagnostic.format())


class LibertyLexError(LibertyError):
    """Raised when Liberty fixture text cannot be tokenized."""


class LibertyParseError(LibertyError):
    """Raised when fixture Liberty text cannot be parsed."""
