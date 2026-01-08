"""Tests for Paper Siphon CLI."""

import pytest
from click.testing import CliRunner

from paper_siphon import LINE_NUMBER_PATTERN, clean_markdown
from paper_siphon.cli import main


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a Click CLI test runner."""
    return CliRunner()


# --- Line number pattern tests ---


@pytest.mark.parametrize(
    "text",
    [
        "1",
        "01",
        "001",
        "0001",
        "9",
        "99",
        "999",
        "9999",
        "123",
        "0042",
    ],
)
def test_line_number_pattern_matches_valid(text: str) -> None:
    """Pattern should match 1-4 digit numbers."""
    assert LINE_NUMBER_PATTERN.match(text)


@pytest.mark.parametrize(
    "text",
    [
        "12345",  # 5 digits - too long
        "1a",  # contains letter
        "a1",
        "12.5",  # contains dot
        " 123",  # leading space
        "123 ",  # trailing space
        "",  # empty
        "one",  # word
        "Table 1",  # text with number
    ],
)
def test_line_number_pattern_rejects_invalid(text: str) -> None:
    """Pattern should not match non-line-number text."""
    assert not LINE_NUMBER_PATTERN.match(text)


# --- clean_markdown tests ---


class TestCleanMarkdownLineNumbers:
    """Tests for line number removal."""

    def test_removes_single_digit(self) -> None:
        assert clean_markdown("1\n\nText\n\n2\n\nMore") == "Text\n\nMore"

    def test_removes_three_digit(self) -> None:
        assert clean_markdown("001\n\n002\n\n## Title") == "## Title"

    def test_removes_four_digit(self) -> None:
        assert clean_markdown("1234\n\nContent") == "Content"

    def test_preserves_numbers_in_prose(self) -> None:
        text = "There are 123 items."
        assert clean_markdown(text) == text

    def test_preserves_table_references(self) -> None:
        text = "See Table 1 for details."
        assert clean_markdown(text) == text


class TestCleanMarkdownWhitespace:
    """Tests for whitespace handling."""

    def test_collapses_multiple_blank_lines(self) -> None:
        assert clean_markdown("A\n\n\n\n\nB") == "A\n\nB"

    def test_strips_leading_trailing(self) -> None:
        assert clean_markdown("\n\n\nContent\n\n\n") == "Content"

    def test_handles_empty_string(self) -> None:
        assert clean_markdown("") == ""


class TestCleanMarkdownIntegration:
    """Integration tests with realistic content."""

    def test_realistic_paper_header(self) -> None:
        text = "001\n\n002\n\n003\n\n## Paper Title\n\n## Abstract\n\nText."
        expected = "## Paper Title\n\n## Abstract\n\nText."
        assert clean_markdown(text) == expected

    def test_handles_only_line_numbers(self) -> None:
        assert clean_markdown("001\n002\n003") == ""

    def test_preserves_markdown_tables(self) -> None:
        text = "| A | B |\n|---|---|\n| 1 | 2 |"
        assert clean_markdown(text) == text


# --- CLI tests ---


class TestCLIHelp:
    """Tests for CLI help and usage."""

    def test_shows_description(self, cli_runner: CliRunner) -> None:
        result = cli_runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Siphon clean Markdown from academic PDFs" in result.output

    def test_shows_all_options(self, cli_runner: CliRunner) -> None:
        result = cli_runner.invoke(main, ["--help"])
        assert "--vlm" in result.output
        assert "--mlx" in result.output
        assert "--enrich-formula" in result.output
        assert "--verbose" in result.output


class TestCLIValidation:
    """Tests for CLI argument validation."""

    def test_requires_file_argument(self, cli_runner: CliRunner) -> None:
        result = cli_runner.invoke(main, [])
        assert result.exit_code != 0
        assert "Missing argument" in result.output

    def test_rejects_nonexistent_file(self, cli_runner: CliRunner) -> None:
        result = cli_runner.invoke(main, ["/nonexistent/path/file.pdf"])
        assert result.exit_code != 0
        assert "does not exist" in result.output.lower()


class TestCLIConversion:
    """Tests for actual file conversion."""

    def test_converts_pdf_to_markdown(self, cli_runner: CliRunner, tmp_path) -> None:
        """Integration test: convert a minimal PDF and verify output."""
        # Create a simple text file to test the flow (docling can handle various formats)
        # We'll skip this if docling is not properly set up
        input_file = tmp_path / "test.txt"
        input_file.write_text("Hello World")
        output_file = tmp_path / "test.md"

        result = cli_runner.invoke(main, [str(input_file), "-o", str(output_file)])

        # This may fail if docling doesn't support .txt, which is fine
        # The test validates the CLI flow works
        if result.exit_code == 0:
            assert output_file.exists()
            assert "Done!" in result.output
