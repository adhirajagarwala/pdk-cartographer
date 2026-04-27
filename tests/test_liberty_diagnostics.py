import pytest

from pdk_cartographer.liberty import LibertyDiagnostic, LibertyError
from pdk_cartographer.liberty.parser import LibertyParseError, parse_liberty_text


def test_diagnostic_formats_message_with_location() -> None:
    diagnostic = LibertyDiagnostic("expected token", line=7, column=11)

    assert diagnostic.format() == "expected token at line 7, column 11"


def test_base_error_exposes_diagnostic() -> None:
    error = LibertyError(LibertyDiagnostic("bad syntax", line=2, column=4))

    assert error.diagnostic.message == "bad syntax"
    assert str(error) == "bad syntax at line 2, column 4"


def test_malformed_input_reports_line_and_column() -> None:
    with pytest.raises(LibertyParseError) as exc_info:
        parse_liberty_text(
            """
            library(bad) {
              cell(BAD_X1) {
                area 1.0;
              }
            }
            """
        )

    message = str(exc_info.value)
    assert "expected ':' or '('" in message
    assert "line" in message
    assert "column" in message
    assert exc_info.value.diagnostic.line is not None


def test_missing_closing_brace_reports_unexpected_end() -> None:
    with pytest.raises(LibertyParseError) as exc_info:
        parse_liberty_text("library(bad) { cell(BAD_X1) { area : 1.0; }")

    assert "unexpected end of Liberty text" in str(exc_info.value)
    assert exc_info.value.diagnostic.column is not None
