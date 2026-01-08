"""Paper Siphon - Extract clean Markdown from academic PDFs."""

import logging
import platform
import sys
from pathlib import Path

import click

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableFormerMode,
    TableStructureOptions,
    VlmPipelineOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline

from paper_siphon.cleaning import clean_markdown

logger = logging.getLogger(__name__)

MLX_AVAILABLE = platform.system() == "Darwin" and platform.machine() == "arm64"


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


def create_vlm_converter(use_mlx: bool, enrich_formula: bool) -> DocumentConverter:
    """Create a converter using the VLM pipeline.

    Args:
        use_mlx: Use MLX acceleration (Apple Silicon only).
        enrich_formula: Enable formula enrichment.

    Raises:
        ImportError: If MLX is requested but mlx-vlm is not installed.
        RuntimeError: If MLX is requested on non-Apple Silicon hardware.
    """
    from docling.datamodel import vlm_model_specs

    if use_mlx:
        if not MLX_AVAILABLE:
            raise RuntimeError("MLX requires Apple Silicon (arm64 macOS)")
        try:
            vlm_options = vlm_model_specs.GRANITEDOCLING_MLX
        except AttributeError:
            raise ImportError(
                "mlx-vlm not installed. Install with: uv pip install mlx-vlm"
            )
    else:
        vlm_options = vlm_model_specs.GRANITEDOCLING_TRANSFORMERS

    pipeline_options = VlmPipelineOptions(
        vlm_options=vlm_options,
        do_formula_enrichment=enrich_formula,
    )
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=VlmPipeline, pipeline_options=pipeline_options
            ),
        }
    )


@click.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
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
    help="Use VLM pipeline (slower but better for complex layouts).",
)
@click.option(
    "--mlx/--no-mlx",
    default=True,
    help="Use MLX acceleration on Apple Silicon. Only applies with --vlm.",
)
@click.option(
    "--enrich-formula",
    is_flag=True,
    default=False,
    help="Enable formula enrichment (slow, runs on CPU).",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Enable verbose logging.",
)
def main(
    file: Path,
    output: Path | None,
    vlm: bool,
    mlx: bool,
    enrich_formula: bool,
    verbose: bool,
) -> None:
    """Siphon clean Markdown from academic PDFs.

    Extracts content from academic papers, automatically removing line numbers
    and cleaning up formatting artifacts.

    \b
    Examples:
        paper-siphon paper.pdf
        paper-siphon paper.pdf -o notes.md
        paper-siphon --vlm paper.pdf
        paper-siphon --enrich-formula paper.pdf
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    if output is None:
        output = file.with_suffix(".md")

    click.echo(f"Converting {file} -> {output}")

    try:
        if vlm:
            mode = "VLM + MLX" if mlx else "VLM + CPU"
            click.echo(f"Using {mode} pipeline")
            converter = create_vlm_converter(use_mlx=mlx, enrich_formula=enrich_formula)
        else:
            click.echo("Using standard pipeline (accurate table mode)")
            converter = create_standard_converter(enrich_formula=enrich_formula)

        result = converter.convert(file)
    except (ImportError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.exception("Conversion failed")
        click.echo(f"Error: Conversion failed - {e}", err=True)
        sys.exit(1)

    markdown = result.document.export_to_markdown()
    cleaned = clean_markdown(markdown)

    output.write_text(cleaned)
    click.echo(f"Done! Output saved to {output}")


if __name__ == "__main__":
    main()
