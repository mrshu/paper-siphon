"""Candidate backends that run in isolated environments (dependency conflicts
with docling and each other). Each shells out to its own uv-managed venv.

Invocations were corrected against upstream mid-2026 docs (via codex review):
a backend whose environment cannot be built or whose conversion fails is
reported unavailable (with reason) and skipped — never silently dropped.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
VENVS = BENCH / ".venvs"
SCRATCH = BENCH / "outputs" / "_scratch"
CONVERT_TIMEOUT = int(os.environ.get("BENCH_CONVERT_TIMEOUT", "1800"))


def _venv_python(name: str) -> Path:
    return VENVS / name / "bin" / "python"


def uv_venv(name: str, python: str = "3.13") -> Path:
    vdir = VENVS / name
    if not (vdir / "bin" / "python").exists():
        VENVS.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["uv", "venv", "--python", python, str(vdir)],
            check=True, capture_output=True, text=True,
        )
    return vdir


def uv_pip(vdir: Path, *specs: str, index_url: str | None = None) -> None:
    cmd = ["uv", "pip", "install", "--python", str(vdir / "bin" / "python")]
    if index_url:
        cmd += ["--index-url", index_url]
    cmd += list(specs)
    subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=3600)


def has_import(vdir: Path, module: str) -> bool:
    r = subprocess.run(
        [str(vdir / "bin" / "python"), "-c", f"import {module}"],
        capture_output=True, text=True,
    )
    return r.returncode == 0


def _find_md(root: Path) -> str:
    mds = sorted(root.rglob("*.md"), key=lambda p: -p.stat().st_size)
    if not mds:
        raise FileNotFoundError(f"no markdown produced under {root}")
    return mds[0].read_text()


def _scratch(name: str) -> Path:
    d = SCRATCH / name
    d.mkdir(parents=True, exist_ok=True)
    return d


class _SubprocessBackend:
    name = "override"
    modules: tuple[str, ...] = ()

    def is_available(self) -> tuple[bool, str]:
        if shutil.which("uv") is None:
            return False, "uv not on PATH"
        vdir = VENVS / self.name
        if not (vdir / "bin" / "python").exists():
            return True, "env not built yet (built on first convert)"
        for m in self.modules:
            if not has_import(vdir, m):
                return False, f"module {m} missing in env"
        return True, ""

    def _run(self, cmd: list[str], env_extra: dict | None = None) -> None:
        env = dict(os.environ)
        if env_extra:
            env.update(env_extra)
        subprocess.run(
            cmd, check=True, capture_output=True, text=True,
            timeout=CONVERT_TIMEOUT, env=env,
        )


class Marker(_SubprocessBackend):
    name = "marker"
    modules = ("marker",)

    def ensure(self) -> Path:
        vdir = uv_venv(self.name)
        if not has_import(vdir, "marker"):
            uv_pip(vdir, "marker-pdf")
        return vdir

    def convert(self, pdf_path: Path) -> str:
        vdir = self.ensure()
        out = _scratch(self.name)
        self._run(
            [
                str(vdir / "bin" / "marker_single"), str(pdf_path),
                "--output_dir", str(out),
                "--output_format", "markdown",
                "--disable_image_extraction",
            ],
            env_extra={"TORCH_DEVICE": "mps", "PYTORCH_ENABLE_MPS_FALLBACK": "1"},
        )
        stem = pdf_path.stem
        md = out / stem / f"{stem}.md"
        return md.read_text() if md.exists() else _find_md(out / stem if (out / stem).exists() else out)


class Chandra(_SubprocessBackend):
    name = "chandra"
    modules = ("chandra",)

    def ensure(self) -> Path:
        vdir = uv_venv(self.name)
        if not has_import(vdir, "chandra"):
            uv_pip(vdir, "chandra-ocr[hf]")
        return vdir

    def convert(self, pdf_path: Path) -> str:
        vdir = self.ensure()
        out = _scratch(self.name) / pdf_path.stem
        out.mkdir(parents=True, exist_ok=True)
        self._run(
            [
                str(vdir / "bin" / "chandra"), str(pdf_path), str(out),
                "--method", "hf",
            ],
            env_extra={"PYTORCH_ENABLE_MPS_FALLBACK": "1"},
        )
        return _find_md(out)


class MinerU(_SubprocessBackend):
    name = "mineru"
    modules = ("mineru",)

    def ensure(self) -> Path:
        vdir = uv_venv(self.name)
        if not has_import(vdir, "mineru"):
            uv_pip(vdir, "mineru[core]")
        return vdir

    def convert(self, pdf_path: Path) -> str:
        vdir = self.ensure()
        out = _scratch(self.name)
        # Default backend first; MinerU picks pipeline vs vlm per install.
        self._run(
            [str(vdir / "bin" / "mineru"), "-p", str(pdf_path), "-o", str(out)],
            env_extra={"PYTORCH_ENABLE_MPS_FALLBACK": "1"},
        )
        return _find_md(out)


class _MlxServerBackend(_SubprocessBackend):
    """Base for document VLMs served via mlx-vlm's OpenAI-compatible server,
    driven directly per page image (full page → Markdown). This is the
    direct-server path — it does NOT include any model's bespoke two-stage
    layout SDK, so it is a lower bound on a model's full-pipeline quality.
    Recorded transparently in the report. Subclasses set MODEL/PORT/name.
    """
    modules = ("mlx_vlm",)
    MODEL = "override"
    PORT = 8123
    _server = None  # each subclass overrides with its own class attribute

    OCR_PROMPT = (
        "Convert this document page image to clean GitHub-flavored Markdown. "
        "Preserve headings, paragraphs, lists, tables (as Markdown or HTML), and "
        "mathematics (as LaTeX, inline $..$ or display $$..$$). Output ONLY the "
        "Markdown for the page content; no commentary, no code fences around the whole page."
    )

    def ensure(self) -> Path:
        vdir = uv_venv("glm_ocr_mlx", python="3.12")  # shared mlx-vlm env
        if not has_import(vdir, "mlx_vlm"):
            uv_pip(vdir, "mlx-vlm>=0.3.11")
        return vdir

    def _start_server(self, vdir: Path) -> None:
        import atexit
        import time
        import urllib.request

        cls = type(self)
        if cls._server and cls._server.poll() is None:
            return
        log_path = BENCH / "outputs" / "_scratch" / f"{self.name}_server.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        fh = open(log_path, "w")
        cls._server = subprocess.Popen(
            [str(vdir / "bin" / "python"), "-m", "mlx_vlm.server",
             "--model", self.MODEL, "--port", str(self.PORT),
             "--trust-remote-code", "--log-level", "WARNING"],
            stdout=fh, stderr=subprocess.STDOUT,
        )
        atexit.register(self.stop)
        deadline = time.time() + 1800  # first-run model download can be slow
        url = f"http://localhost:{self.PORT}/v1/models"
        while time.time() < deadline:
            if cls._server.poll() is not None:
                raise RuntimeError(f"mlx_vlm.server exited early; see {log_path}")
            try:
                urllib.request.urlopen(url, timeout=3)
                return
            except Exception:
                time.sleep(3)
        raise RuntimeError("mlx_vlm.server did not become ready within 1800s")

    @classmethod
    def stop(cls) -> None:
        if cls._server and cls._server.poll() is None:
            cls._server.terminate()
            try:
                cls._server.wait(timeout=20)
            except Exception:
                cls._server.kill()

    def _ocr_page(self, img_path: Path) -> str:
        import base64
        import json
        import urllib.request

        b64 = base64.b64encode(img_path.read_bytes()).decode()
        payload = {
            "model": self.MODEL,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": self.OCR_PROMPT},
                    {"type": "image_url",
                     "image_url": {"url": f"data:image/png;base64,{b64}"}},
                ],
            }],
            "max_tokens": 4096,
            "temperature": 0.0,
        }
        req = urllib.request.Request(
            f"http://localhost:{self.PORT}/v1/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=CONVERT_TIMEOUT) as resp:
            obj = json.loads(resp.read())
        return obj["choices"][0]["message"]["content"]

    def convert(self, pdf_path: Path) -> str:
        from lib import render_all_pages

        vdir = self.ensure()
        self._start_server(vdir)
        img_dir = _scratch(self.name) / pdf_path.stem
        pages = render_all_pages(pdf_path, img_dir, dpi=150, cap=30)
        return "\n\n".join(self._ocr_page(img).strip() for img in pages)


class GlmOcrMlx(_MlxServerBackend):
    name = "glm_ocr_mlx"
    MODEL = "mlx-community/GLM-OCR-bf16"
    PORT = 8123
    _server = None


class OlmOcr2Mlx(_MlxServerBackend):
    """olmOCR-2-7B (Qwen2.5-VL-7B fine-tune, Apache-2.0), 4-bit MLX quant.

    Uses the IN-PROCESS mlx_vlm.generate runner (not the server): mlx_vlm.server
    runs inference in worker threads, which crashes on Qwen2.5-VL with
    'RuntimeError: There is no Stream(gpu, N) in current thread'. The runner
    loads the model once (per PDF) on the main thread and generates per page.
    """
    name = "olmocr2_mlx"
    MODEL = "mlx-community/olmOCR-2-7B-1025-4bit"
    PORT = 8124
    _server = None

    def convert(self, pdf_path: Path) -> str:
        from lib import render_all_pages

        vdir = self.ensure()
        img_dir = _scratch(self.name) / pdf_path.stem
        pages = render_all_pages(pdf_path, img_dir, dpi=150, cap=30)
        runner = Path(__file__).resolve().parent / "mlx_generate_runner.py"
        proc = subprocess.run(
            [str(vdir / "bin" / "python"), str(runner), self.MODEL,
             *[str(p) for p in pages]],
            capture_output=True, text=True, timeout=CONVERT_TIMEOUT,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"mlx_generate_runner failed: {proc.stderr[-500:]}")
        parts = [p.strip() for p in proc.stdout.split("<<<PAGE_DELIM>>>") if p.strip()]
        if not parts:
            raise RuntimeError("mlx_generate_runner produced no output")
        return "\n\n".join(parts)


class LightOnOcrMlx(_MlxServerBackend):
    """LightOnOCR-1B (small 1B end-to-end OCR VLM), 4-bit MLX quant."""
    name = "lightonocr_mlx"
    MODEL = "mlx-community/LightOnOCR-1B-1025-4bit"
    PORT = 8125
    _server = None


class PaddleOcrVl(_SubprocessBackend):
    name = "paddleocr_vl"
    modules = ("paddleocr",)

    def ensure(self) -> Path:
        vdir = uv_venv(self.name)
        if not has_import(vdir, "paddle"):
            uv_pip(
                vdir, "paddlepaddle==3.2.1",
                index_url="https://www.paddlepaddle.org.cn/packages/stable/cpu/",
            )
        if not has_import(vdir, "paddleocr"):
            uv_pip(vdir, "paddleocr[doc-parser]")
        return vdir

    def convert(self, pdf_path: Path) -> str:
        vdir = self.ensure()
        out = _scratch(self.name) / pdf_path.stem
        out.mkdir(parents=True, exist_ok=True)
        self._run(
            [
                str(vdir / "bin" / "paddleocr"), "doc_parser",
                "--input", str(pdf_path),
                "--save_path", str(out),
            ]
        )
        return _find_md(out)
