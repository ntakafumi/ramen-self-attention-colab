#!/usr/bin/env python3
"""公開Notebookの構造、出力、メタデータを標準ライブラリだけで検査する。"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "ramen_attention_colab.ipynb"
REQUIRED_PUBLIC_FILES = [
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "CITATION.cff",
    ROOT / "CHANGELOG.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    ROOT / "THIRD_PARTY_NOTICES.md",
    ROOT / "LICENSES" / "Apache-2.0.txt",
    ROOT / "requirements.txt",
]

FORBIDDEN_METADATA_KEYS = {
    "base_uri",
    "colab",
    "displayName",
    "execution",
    "executionInfo",
    "outputId",
    "user",
    "userId",
    "widgets",
}
FORBIDDEN_TEXT = (
    "/Users/",
    "C:\\Users\\",
    "application/vnd.google.colaboratory.intrinsic+json",
    "application/vnd.jupyter.widget-view+json",
    "colab-df-container",
    "google.colab.",
)


def walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_PUBLIC_FILES if not path.is_file()]
    if missing:
        fail(f"公開用ファイルがありません: {', '.join(missing)}")

    raw = NOTEBOOK_PATH.read_text(encoding="utf-8")
    for text in FORBIDDEN_TEXT:
        if text in raw:
            fail(f"公開できない文字列がNotebookに含まれています: {text}")

    notebook = json.loads(raw)
    if notebook.get("nbformat") != 4:
        fail("nbformatが4ではありません")

    all_keys = set(walk_keys(notebook))
    bad_global_keys = all_keys & FORBIDDEN_METADATA_KEYS
    if bad_global_keys:
        fail(f"公開不要メタデータがあります: {sorted(bad_global_keys)}")

    code_cells = []
    error_outputs = []

    for index, cell in enumerate(notebook.get("cells", [])):
        cell_metadata_keys = set(walk_keys(cell.get("metadata", {})))
        bad_keys = cell_metadata_keys & FORBIDDEN_METADATA_KEYS
        if bad_keys:
            fail(f"セル{index}に公開不要メタデータがあります: {sorted(bad_keys)}")

        if cell.get("cell_type") != "code":
            continue

        code_cells.append(cell)
        for output in cell.get("outputs", []):
            output_metadata_keys = set(walk_keys(output.get("metadata", {})))
            bad_output_keys = output_metadata_keys & FORBIDDEN_METADATA_KEYS
            if bad_output_keys:
                fail(f"セル{index}の出力に公開不要メタデータがあります: {sorted(bad_output_keys)}")
            if output.get("output_type") == "error":
                error_outputs.append(index)

    if error_outputs:
        fail(f"エラー出力を含むコードセルがあります: {error_outputs}")

    execution_counts = [cell.get("execution_count") for cell in code_cells]
    expected_counts = list(range(1, len(code_cells) + 1))
    if execution_counts != expected_counts:
        fail("コードセルの実行番号が1からの連番ではありません")

    print(f"OK: {len(code_cells)} code cells")
    print("OK: no error outputs")
    print("OK: no private Colab metadata or local absolute paths")
    print("OK: required public files are present")


if __name__ == "__main__":
    main()
