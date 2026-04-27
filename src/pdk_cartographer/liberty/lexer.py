"""Tokenization for the fixture-first Liberty subset parser.

This lexer is intentionally small. It recognizes the syntax needed by the
synthetic educational fixtures in this repository and preserves line/column
locations for parser diagnostics. It is not a full Liberty lexer.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from pdk_cartographer.liberty.diagnostics import LibertyDiagnostic, LibertyLexError


class TokenKind(StrEnum):
    """Token categories used by the handwritten Liberty parser."""

    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    EOF = "EOF"


@dataclass(frozen=True)
class Token:
    """A Liberty token with source location."""

    kind: TokenKind
    value: str
    line: int
    column: int


_PUNCTUATION = {
    "(": TokenKind.LPAREN,
    ")": TokenKind.RPAREN,
    "{": TokenKind.LBRACE,
    "}": TokenKind.RBRACE,
    ":": TokenKind.COLON,
    ";": TokenKind.SEMICOLON,
    ",": TokenKind.COMMA,
}


def tokenize(text: str) -> tuple[Token, ...]:
    """Tokenize Liberty fixture text."""

    lexer = _Lexer(text)
    return lexer.tokenize()


class _Lexer:
    def __init__(self, text: str) -> None:
        self._text = text
        self._pos = 0
        self._line = 1
        self._column = 1

    def tokenize(self) -> tuple[Token, ...]:
        tokens: list[Token] = []
        while not self._at_end():
            char = self._peek()
            if char.isspace():
                self._consume_whitespace()
            elif char == "/" and self._peek_next() == "/":
                self._consume_line_comment()
            elif char == "/" and self._peek_next() == "*":
                self._consume_block_comment()
            elif char == '"':
                tokens.append(self._consume_string())
            elif char in _PUNCTUATION:
                tokens.append(self._consume_punctuation())
            elif char == "-" or char.isdigit():
                tokens.append(self._consume_number())
            elif _is_identifier_start(char):
                tokens.append(self._consume_identifier())
            else:
                raise self._error(f"unexpected character {char!r}")

        tokens.append(Token(TokenKind.EOF, "", self._line, self._column))
        return tuple(tokens)

    def _consume_whitespace(self) -> None:
        while not self._at_end() and self._peek().isspace():
            self._advance()

    def _consume_line_comment(self) -> None:
        self._advance()
        self._advance()
        while not self._at_end() and self._peek() != "\n":
            self._advance()

    def _consume_block_comment(self) -> None:
        self._advance()
        self._advance()
        while not self._at_end():
            if self._peek() == "*" and self._peek_next() == "/":
                self._advance()
                self._advance()
                return
            self._advance()
        raise self._error("unterminated block comment")

    def _consume_string(self) -> Token:
        line = self._line
        column = self._column
        self._advance()
        chars: list[str] = []
        while not self._at_end():
            char = self._advance()
            if char == '"':
                return Token(TokenKind.STRING, "".join(chars), line, column)
            if char == "\\":
                if self._at_end():
                    raise self._error("unterminated string escape")
                chars.append(self._advance())
            else:
                chars.append(char)
        raise self._error("unterminated string")

    def _consume_punctuation(self) -> Token:
        line = self._line
        column = self._column
        char = self._advance()
        return Token(_PUNCTUATION[char], char, line, column)

    def _consume_number(self) -> Token:
        line = self._line
        column = self._column
        chars: list[str] = []
        if self._peek() == "-":
            chars.append(self._advance())
            if self._at_end() or not self._peek().isdigit():
                raise self._error("expected digit after '-'")

        while not self._at_end() and self._peek().isdigit():
            chars.append(self._advance())

        if not self._at_end() and self._peek() == ".":
            chars.append(self._advance())
            if self._at_end() or not self._peek().isdigit():
                raise self._error("expected digit after decimal point")
            while not self._at_end() and self._peek().isdigit():
                chars.append(self._advance())

        if not self._at_end() and self._peek() in {"e", "E"}:
            chars.append(self._advance())
            if not self._at_end() and self._peek() in {"+", "-"}:
                chars.append(self._advance())
            if self._at_end() or not self._peek().isdigit():
                raise self._error("expected exponent digits")
            while not self._at_end() and self._peek().isdigit():
                chars.append(self._advance())

        return Token(TokenKind.NUMBER, "".join(chars), line, column)

    def _consume_identifier(self) -> Token:
        line = self._line
        column = self._column
        chars = [self._advance()]
        while not self._at_end() and _is_identifier_part(self._peek()):
            chars.append(self._advance())
        return Token(TokenKind.IDENTIFIER, "".join(chars), line, column)

    def _advance(self) -> str:
        char = self._text[self._pos]
        self._pos += 1
        if char == "\n":
            self._line += 1
            self._column = 1
        else:
            self._column += 1
        return char

    def _peek(self) -> str:
        return self._text[self._pos]

    def _peek_next(self) -> str | None:
        next_pos = self._pos + 1
        if next_pos >= len(self._text):
            return None
        return self._text[next_pos]

    def _at_end(self) -> bool:
        return self._pos >= len(self._text)

    def _error(self, message: str) -> LibertyLexError:
        return LibertyLexError(
            LibertyDiagnostic(message, line=self._line, column=self._column)
        )


def _is_identifier_start(char: str) -> bool:
    return char.isalpha() or char == "_"


def _is_identifier_part(char: str) -> bool:
    return char.isalnum() or char in {"_", ".", "$", "-"}
