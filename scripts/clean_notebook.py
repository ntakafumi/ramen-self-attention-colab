#!/usr/bin/env python3
"""Colabが付加した公開不要情報をNotebookから取り除く。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "ramen_attention_colab.ipynb"

COLAB_MIME_TYPES = {
    "application/vnd.google.colaboratory.intrinsic+json",
    "application/vnd.jupyter.widget-view+json",
}
COLAB_HTML_MARKERS = (
    "colab-df-container",
    "google.colab.",
    "convertToInteractive",
)


def as_text(value) -> str:
    """Notebookの文字列または文字列配列を検査用の一文字列にする。"""
    if isinstance(value, list):
        return "".join(str(item) for item in value)
    return str(value)


def clean_output(output: dict) -> dict | None:
    """計算結果を残し、Colab専用表現と再現不能な表示だけを除く。"""
    if output.get("output_type") in {"display_data", "execute_result"}:
        # nbformatの仕様上、この二形式には空でもmetadataが必要。
        output["metadata"] = {}
    else:
        output.pop("metadata", None)

    data = output.get("data")
    if isinstance(data, dict):
        for mime_type in COLAB_MIME_TYPES:
            data.pop(mime_type, None)

        html = data.get("text/html")
        if html is not None and any(marker in as_text(html) for marker in COLAB_HTML_MARKERS):
            data.pop("text/html", None)

        plain = data.get("text/plain")
        if plain is not None and as_text(plain).startswith("<pandas.io.formats.style.Styler at 0x"):
            data.pop("text/plain", None)

        if not data:
            return None

    return output


def main() -> None:
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))

    notebook["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3",
        },
    }

    for cell in notebook.get("cells", []):
        cell["metadata"] = {}

        if cell.get("cell_type") == "markdown":
            source = as_text(cell.get("source", []))
            if source.startswith("## 著作権と利用条件") and "リポジトリ独自の文章とコード" not in source:
                source = source.replace(
                    "このNotebookの説明文と実験コードは、この教材のために新規に作成したものです。  \n",
                    "このNotebookの説明文と実験コードは、この教材のために新規に作成したものです。  \n"
                    "リポジトリ独自の文章とコードには、同梱の `LICENSE` に示す "
                    "`All Rights Reserved` の条件が適用されます。  \n",
                )
                cell["source"] = source.splitlines(keepends=True)
            elif source.startswith("## 著作権と利用条件"):
                source = source.replace(
                    "- [PyTorch](https://github.com/pytorch/pytorch)：BSD-3-Clause。",
                    "- [PyTorch](https://github.com/pytorch/pytorch)：本体はBSD-3-Clause。"
                    "配布パッケージには別ライセンスの第三者成果物も含まれます。",
                )
                source = source.replace(
                    "リポジトリ独自の文章とコードには、同梱の `LICENSE` に示す "
                    "`All Rights Reserved` の条件が適用されます。  ",
                    "リポジトリ独自の文章とコードには、同梱の `LICENSE` に示す "
                    "`All Rights Reserved` と限定的な教育利用許諾が適用されます。  ",
                )
                cell["source"] = source.splitlines(keepends=True)
            continue

        if cell.get("cell_type") != "code":
            continue

        source = as_text(cell.get("source", []))
        if "%pip " in source:
            # パッケージ取得時の進捗表示は環境依存で、教材の計算結果ではない。
            cell["outputs"] = []
            continue

        cleaned_outputs = []
        for output in cell.get("outputs", []):
            cleaned = clean_output(output)
            if cleaned is not None:
                cleaned_outputs.append(cleaned)
        cell["outputs"] = cleaned_outputs

    NOTEBOOK_PATH.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
