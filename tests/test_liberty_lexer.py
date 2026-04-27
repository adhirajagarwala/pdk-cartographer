import pytest

from pdk_cartographer.liberty.lexer import LibertyLexError, TokenKind, tokenize


def test_tokenize_identifiers_strings_numbers_and_punctuation() -> None:
    tokens = tokenize('cell(TINY_INV_X1) { area : 1.40; function : "!A"; }')

    assert [token.kind for token in tokens] == [
        TokenKind.IDENTIFIER,
        TokenKind.LPAREN,
        TokenKind.IDENTIFIER,
        TokenKind.RPAREN,
        TokenKind.LBRACE,
        TokenKind.IDENTIFIER,
        TokenKind.COLON,
        TokenKind.NUMBER,
        TokenKind.SEMICOLON,
        TokenKind.IDENTIFIER,
        TokenKind.COLON,
        TokenKind.STRING,
        TokenKind.SEMICOLON,
        TokenKind.RBRACE,
        TokenKind.EOF,
    ]
    assert tokens[0].value == "cell"
    assert tokens[7].value == "1.40"
    assert tokens[11].value == "!A"


def test_tokenize_ignores_whitespace_and_line_comments() -> None:
    tokens = tokenize(
        """
        // synthetic comment
        library(example) {
        }
        """
    )

    assert [token.value for token in tokens[:-1]] == [
        "library",
        "(",
        "example",
        ")",
        "{",
        "}",
    ]


def test_tokenize_ignores_block_comments_and_tracks_locations() -> None:
    tokens = tokenize("/* synthetic\nfixture */\ncell(A) {}")

    assert tokens[0].kind == TokenKind.IDENTIFIER
    assert tokens[0].value == "cell"
    assert tokens[0].line == 3
    assert tokens[0].column == 1


def test_tokenize_numbers_include_negative_and_exponent_forms() -> None:
    tokens = tokenize("cell(NUM_X1) { area : -1.25e-3; }")

    assert [token.value for token in tokens if token.kind == TokenKind.NUMBER] == [
        "-1.25e-3"
    ]


def test_unterminated_block_comment_reports_location() -> None:
    with pytest.raises(LibertyLexError) as exc_info:
        tokenize("library(bad) { /* unterminated")

    assert "unterminated block comment" in str(exc_info.value)
    assert exc_info.value.diagnostic.line == 1
    assert exc_info.value.diagnostic.column is not None
