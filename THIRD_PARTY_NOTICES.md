# Third-party notices

このリポジトリは、次の第三者成果物を実行時に利用します。

各成果物の著作権とライセンスは、それぞれの権利者に帰属します。

このファイルは、各ライセンス本文を置き換えるものではありません。

## 学習済みモデル

### tohoku-nlp/bert-base-japanese-v3

- 提供者：東北大学乾研究室
- 用途：Tokenizerと単語Embedding表
- 配布元：[Hugging Face model card](https://huggingface.co/tohoku-nlp/bert-base-japanese-v3)
- ライセンス：Apache License 2.0

Apache License 2.0の本文は、[LICENSES/Apache-2.0.txt](./LICENSES/Apache-2.0.txt)にも収録しています。

モデルの重みは、このリポジトリへ収録しません。

Notebookの実行時に配布元からダウンロードします。

## 主なライブラリ

- [Transformers](https://github.com/huggingface/transformers)：Apache License 2.0
- [huggingface_hub](https://github.com/huggingface/huggingface_hub)：Apache License 2.0
- [PyTorch](https://github.com/pytorch/pytorch)：本体はBSD-3-Clause。配布パッケージには、別ライセンスの第三者成果物も含まれます。
- [fugashi](https://github.com/polm/fugashi)：fugashi本体はMIT License。配布wheelに含まれるMeCabはBSD License。
- [unidic-lite](https://github.com/polm/unidic-lite)：パッケージのコードはMIT LicenseまたはWTFPL。収録されるUniDic 2.1.2はBSD License。
- [NumPy](https://github.com/numpy/numpy)：BSD-3-Clause
- [pandas](https://github.com/pandas-dev/pandas)：BSD-3-Clause

依存パッケージにも、それぞれのライセンスが適用されます。

このリポジトリは、これらのライブラリやモデル重みを同梱しません。

Notebookを実行すると、Pythonパッケージはパッケージ配布元から、モデルはHugging Faceから取得されます。

再配布する場合は、利用時点の各配布物に含まれるライセンスとNOTICEを確認してください。
