"""In-process MLX-VLM page→Markdown runner (main thread).

Avoids mlx_vlm.server's worker-thread GPU-stream crash on Qwen2.5-VL models
(RuntimeError: There is no Stream(gpu, N) in current thread). Loads the model
once, generates for each page image, prints each page's Markdown separated by a
delimiter. Run BY the mlx-vlm venv's python.

Usage: python mlx_generate_runner.py <model_id> <img1> <img2> ...
"""

import sys

DELIM = "<<<PAGE_DELIM>>>"
PROMPT = (
    "Convert this document page image to clean GitHub-flavored Markdown. "
    "Preserve headings, paragraphs, lists, tables (as Markdown or HTML), and "
    "mathematics (as LaTeX, inline $..$ or display $$..$$). Output ONLY the "
    "Markdown for the page content; no commentary."
)


def _text(result) -> str:
    # generate() may return a str or an object with .text
    if isinstance(result, str):
        return result
    for attr in ("text", "generation", "output"):
        if hasattr(result, attr):
            return str(getattr(result, attr))
    return str(result)


def main() -> None:
    model_id = sys.argv[1]
    images = sys.argv[2:]

    from mlx_vlm import generate, load
    from mlx_vlm.prompt_utils import apply_chat_template
    from mlx_vlm.utils import load_config

    model, processor = load(model_id)
    config = load_config(model_id)

    for img in images:
        formatted = apply_chat_template(processor, config, PROMPT, num_images=1)
        try:
            result = generate(
                model, processor, formatted, image=[img],
                max_tokens=4096, temperature=0.0, verbose=False,
            )
            page = _text(result).strip()
        except Exception as e:  # emit marker so the caller can see per-page failure
            page = f"<<<PAGE_ERROR>>> {type(e).__name__}: {e}"
        sys.stdout.write(DELIM + "\n" + page + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
