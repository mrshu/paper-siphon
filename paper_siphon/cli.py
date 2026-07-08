"""Paper Siphon - Extract clean Markdown from academic PDFs."""

import logging
import sys
import tempfile
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse

import click

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableFormerMode,
    TableStructureOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption

from paper_siphon.backends import vlm_backend_name, vlm_convert
from paper_siphon.cleaning import clean_markdown
from paper_siphon.quality import needs_escalation

logger = logging.getLogger(__name__)


def is_url(source: str) -> bool:
    """Check if source is a URL."""
    parsed = urlparse(source)
    return parsed.scheme in ("http", "https")


def to_markdown_filename(filename: str) -> Path:
    """Convert a filename to .md output path.

    Handles arXiv-style IDs like '1706.03762' where the dot is not a file extension.
    """
    path = Path(filename)
    suffix = path.suffix

    # If suffix looks like a number (e.g., .03762), it's not a real extension
    if suffix and suffix[1:].isdigit():
        return Path(filename + ".md")

    return path.with_suffix(".md")


@contextmanager
def resolve_source(source: str):
    """Resolve source to a local file path, downloading if URL.

    Yields (path, filename) where filename is used for default output naming.
    """
    if is_url(source):
        parsed = urlparse(source)
        filename = Path(parsed.path).name or "paper.pdf"
        click.echo(f"Downloading {source}")
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            urllib.request.urlretrieve(source, tmp_path)
            yield tmp_path, filename
        finally:
            tmp_path.unlink(missing_ok=True)
    else:
        path = Path(source)
        if not path.exists():
            raise click.ClickException(f"File not found: {source}")
        yield path, path.name


def create_standard_converter(enrich_formula: bool) -> DocumentConverter:
    """Create a converter using the standard PDF pipeline."""
    pipeline_options = PdfPipelineOptions(
        do_table_structure=True,
        table_structure_options=TableStructureOptions(mode=TableFormerMode.ACCURATE),
        do_formula_enrichment=enrich_formula,
    )
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
        }
    )


def convert_standard(file_path: Path, enrich_formula: bool) -> str:
    """Run the fast default Docling pipeline; return raw Markdown."""
    converter = create_standard_converter(enrich_formula=enrich_formula)
    result = converter.convert(file_path)
    return result.document.export_to_markdown()


@click.command()
@click.version_option(package_name="paper-siphon")
@click.argument("source", required=False)
@click.pass_context
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    help="Output file path. Defaults to input filename with .md extension.",
)
@click.option(
    "--vlm",
    is_flag=True,
    default=False,
    help="Use the VLM backend (GLM-OCR on Apple Silicon, marker elsewhere) — "
    "slower but much better on complex layouts, math, and bad encodings.",
)
@click.option(
    "--mlx/--no-mlx",
    default=True,
    help="Use MLX (GLM-OCR) on Apple Silicon for the VLM path. "
    "--no-mlx forces the marker backend even on a Mac.",
)
@click.option(
    "--escalate/--no-escalate",
    default=True,
    help="Auto-retry with the VLM backend when the default output looks "
    "garbled or drops equations (default: on).",
)
@click.option(
    "--enrich-formula",
    is_flag=True,
    default=False,
    help="Enable formula enrichment on the default pipeline (slow, runs on CPU).",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Enable verbose logging.",
)
def main(
    ctx: click.Context,
    source: str | None,
    output: Path | None,
    vlm: bool,
    mlx: bool,
    escalate: bool,
    enrich_formula: bool,
    verbose: bool,
) -> None:
    """Siphon clean Markdown from academic PDFs.

    SOURCE can be a local file path or a URL to a PDF.

    Extracts content from academic papers, automatically removing line numbers
    and cleaning up formatting artifacts.

    \b
    Examples:
        paper-siphon paper.pdf
        paper-siphon paper.pdf -o notes.md
        paper-siphon https://arxiv.org/pdf/1706.03762.pdf
        paper-siphon --vlm paper.pdf

    \b
    Tip: For arXiv papers, just change /abs/ to /pdf/ in the URL:
        https://arxiv.org/abs/1706.03762  ->  https://arxiv.org/pdf/1706.03762.pdf
    """
    if source is None:
        click.echo(ctx.get_help())
        return

    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    with resolve_source(source) as (file_path, filename):
        if output is None:
            output = to_markdown_filename(filename)

        click.echo(f"Converting {source} -> {output}")

        try:
            if vlm:
                click.echo(f"Using VLM backend: {vlm_backend_name(mlx)}")
                markdown = vlm_convert(file_path, use_mlx=mlx)
            else:
                click.echo("Using standard pipeline (accurate table mode)")
                markdown = convert_standard(file_path, enrich_formula=enrich_formula)

                if escalate:
                    should, reason = needs_escalation(markdown)
                    if should:
                        click.echo(
                            f"Default {reason}; re-running with "
                            f"{vlm_backend_name(mlx)}"
                        )
                        # Auto-escalation is best-effort: if the VLM backend
                        # can't run (no uv, download/network failure, timeout,
                        # crash), keep the usable standard output rather than
                        # discarding a conversion Docling already produced.
                        try:
                            markdown = vlm_convert(file_path, use_mlx=mlx)
                        except Exception as e:
                            click.echo(
                                f"VLM escalation failed ({e}); keeping the "
                                "standard-pipeline output",
                                err=True,
                            )
        except ImportError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
        except Exception as e:
            logger.exception("Conversion failed")
            click.echo(f"Error: Conversion failed - {e}", err=True)
            sys.exit(1)

        cleaned = clean_markdown(markdown)

        output.write_text(cleaned)
        click.echo(f"Done! Output saved to {output}")


if __name__ == "__main__":
    main()
