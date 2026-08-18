# 「ラーメンが」の次は「好き」？ Attentionを計算してみよう

日本語BERTの学習済み単語Embeddingを入口にして、Scaled Dot-Product Attentionの計算を途中の数値まで確かめる初心者向け教材です。

中西崇文 [『ChatGPTはどのように動いているのか？』（翔泳社、2026年）](https://amzn.asia/d/09DZPTOy)から発展させた独立教材であり、書籍本文の転載ではありません。

対象は、日本の高校生を含む、Transformerを初めて学ぶ人です。

## Notebook

[ramen_attention_colab.ipynb](./ramen_attention_colab.ipynb)

Google Colabの無料版で、GPUを使わずに実行できます。

最初の実行では、約450 MBの日本語BERTのファイルをダウンロードします。

## この教材で行うこと

題材は、次の指定文です。

> 私がラーメンが[MASK]

候補は「好き」「寝る」「悩む」の三つです。

Notebookでは、次の順に計算します。

1. 「ラーメン」「餃子」「桜」をEmbeddingし、コサイン類似度を比べる。
2. 入力文と三候補をトークンへ分割する。
3. 公開済み日本語BERTの単語Embedding表から、各トークンの768次元ベクトルを得る。
4. 教材用の一層・一ヘッドのSelf-Attentionで、Query、Key、Valueを計算する。
5. QueryとKeyの内積を \(\sqrt{d_k}\) で割り、softmaxでAttention重みに変える。
6. Attention重みを使ってValueを混ぜ、文脈ベクトルを作る。
7. 文脈ベクトルと三候補のEmbeddingをコサイン類似度で比べる。
8. 小さな学習集合から \(W_Q, W_K, W_V\) を学習し、学習前後を比べる。
9. 未学習の「ラーメン」へ結果が移る手掛かりを、30学習語との類似度から調べる。
10. Attentionを均等に固定した対照模型とも比べる。

入力トークンと候補について、768個のEmbedding成分を省略せず表示します。

必要なら、各成分を列に分けたCSVも生成できます。

## 何が「本物」と共通し、何を省いたか

共通する中心計算は、次の式です。

$$
\operatorname{Attention}(Q,K,V)
=
\operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
$$

ただし、このNotebookが作るのは、固定した日本語BERTの単語Embedding表を入力に使う教材用の三分類模型です。

BERTの穴埋めモデルそのものでも、GPT系LLMの次トークン生成モデルでもありません。

次の要素を意図的に省いています。

- 多層化
- Multi-Head Attention
- 位置Embedding
- Feed Forward Network
- 残差接続
- Layer Normalization
- Dropout
- GPT系モデルの因果マスク
- 語彙全体から次トークンを選ぶ出力層
- BERT入力で通常加える`[CLS]`と`[SEP]`

また、「寝る」「悩む」のように複数トークンへ分かれる候補は、各トークンのEmbeddingを平均して一個の候補代表ベクトルにしています。

これは候補比較を見やすくするための単純化であり、複数トークンを順番に生成する確率ではありません。

入力トークンと候補のEmbeddingは、数値の尺度をそろえるため、長さ1へ正規化してから使います。

この正規化は教材上の追加処理であり、実際のBERTやGPTの標準処理ではありません。

出力専用の手作り行列 \(W_{\mathrm{OUT}}\) は置かず、候補Embeddingにも入力と同じ学習対象の \(W_V\) を使います。

これも計算経路を短く見せるための設計であり、実際のLLMの出力層と同じ構造ではありません。

## 保存済み実行結果

乱数シードを1に固定し、CPUで全25コードセルを通し実行した結果です。

| 観察項目 | 結果 |
|---|---:|
| ラーメンと餃子の単語Embedding類似度 | 0.3008 |
| ラーメンと桜の単語Embedding類似度 | 0.1082 |
| 学習前の一位 | 悩む（41.9%） |
| 学習後の一位 | 好き（68.7%） |
| 学習後に「ラーメン」へ向いたAttention | 39.1% |
| 学習30件の正解率 | 100.0% |
| 検証9件の正解率 | 100.0% |
| 均等Attention対照の検証正解率 | 100.0% |

この結果は、教材用に人手で選んだ30件の学習例と9件の検証例に対するものです。

一般的な日本語能力や、実際のLLMの性能を示す値ではありません。

とくに、Attentionを均等に固定した対照模型も100%になりました。

したがって、この実験から「Attention重みが予測の唯一の原因である」「Attentionを見れば模型の判断理由が分かる」とは結論できません。

この教材で直接観察できるのは、QとKの内積から重みが生まれ、その重みでVが混ざる計算過程です。

学習データに「ラーメン」は含めていません。

保存済み結果では、「ラーメン」に近い学習語の上位5件が、カレー、寿司、餃子、珈琲、ケーキとなりました。

事前学習済みEmbeddingに含まれる近さと、30件から学んだ行列が組み合わさって、「好き」が一位になります。

ただし、最終結果は単純な最近傍検索ではなく、入力文全体をAttentionへ通した後の三候補比較です。

## 書籍との対応ページ

Notebook内では、次の紙面ページを対応箇所として示しています。

- 34〜38ページ：ベクトル化する理由。
- 52〜60ページ：内積とコサイン類似度。
- 120〜132ページ：誤差から行列を更新する学習。
- 147〜154ページ：Embeddingと768次元ベクトルの類似度。
- 186〜193ページ：Transformer全体の流れ。
- 194〜203ページ：Q、K、VとSelf-Attentionの計算。

書籍本文PDFは著作権保護されたローカル参照資料であり、この公開リポジトリには収録しません。

## Google Colabでの実行方法

1. [ramen_attention_colab.ipynb](./ramen_attention_colab.ipynb)を開く。
2. ファイルをダウンロードし、[Google Colab](https://colab.research.google.com/)へアップロードする。
3. 「ランタイム」→「すべてのセルを実行」を選ぶ。

新しいColabランタイムでの実行を推奨します。

無償利用枠の計算資源や制限は変動するため、最新情報は [Google Colab FAQ](https://research.google.com/colaboratory/faq.html)を確認してください。

## 主な実行環境

Notebook内で、次のパッケージ版を指定しています。

- Transformers 5.15.0
- huggingface-hub 1.24.0
- fugashi 1.5.1
- unidic-lite 1.0.8
- PyTorch 2.5以上、3未満

ローカル環境で試す場合の依存関係は、[requirements.txt](./requirements.txt)にも記載しています。

ハードウェアやPyTorchの版によって、小数点以下の値がわずかに変わる可能性があります。

## ファイル

- `ramen_attention_colab.ipynb`：教材本体と保存済みの実行結果。
- `README.md`：教材の目的、範囲、実行方法、注意点。
- `requirements.txt`：ローカル実行用の主な依存関係。
- `LICENSE`：このリポジトリ独自の文章とコードの利用条件。
- `CITATION.cff`：研究、授業、記事で参照するときの書誌情報。
- `CHANGELOG.md`：公開版の変更履歴。
- `CONTRIBUTING.md`：不具合報告と提案の方針。
- `SECURITY.md`：脆弱性を見つけた場合の連絡方針。
- `THIRD_PARTY_NOTICES.md`：利用する外部モデルとライブラリの情報。
- `LICENSES/Apache-2.0.txt`：第三者成果物に適用されるApache License 2.0の写し。
- `scripts/clean_notebook.py`：Colab固有の公開不要情報を除去する補助スクリプト。
- `scripts/validate_notebook.py`：Notebookの実行状態と公開安全性を検査するスクリプト。
- `.github/workflows/validate-notebook.yml`：pushとpull requestで検査を実行するGitHub Actions。
- `.gitignore`：一時ファイル、任意生成CSV、執筆用の内部メモを公開対象から外す設定。

## 著作権と第三者成果物

Notebookの説明文と実験コードは、この教材のために作成したものです。

モデル本体はリポジトリへ収録せず、実行時に [tohoku-nlp/bert-base-japanese-v3](https://huggingface.co/tohoku-nlp/bert-base-japanese-v3)から取得します。

モデルと各ライブラリには、それぞれのライセンスが適用されます。

詳細は [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md)を参照してください。

## このリポジトリ固有のライセンス

Copyright (c) 2026 Takafumi Nakanishi（中西 崇文）。

このリポジトリ独自の文章、コード、Notebook構成、表などには、[LICENSE](./LICENSE)に示す`All Rights Reserved`と限定的な教育利用許諾を適用します。

個人学習または非営利授業では、条件を守る限り、Notebookのダウンロード、実行、私的改変、同じ授業の履修者への無償配布ができます。

販売、商用利用、公衆への再配布、改変版の一般公開、別の出版物への収録には、著作権者の事前許諾が必要です。

この許諾は、MIT LicenseやApache License 2.0などのオープンソースライセンスではありません。

第三者のモデル、ライブラリ、論文には、それぞれの権利者が定めた別のライセンスが適用されます。

将来、教材の再利用を広く許可する場合は、著者が公開方針を決めたうえで、MIT LicenseやApache License 2.0などへ明示的に変更する必要があります。

## 公開前の検査

Colabで再実行した後は、リポジトリのルートで次の二つを順に実行します。

```bash
python3 scripts/clean_notebook.py
python3 scripts/validate_notebook.py
```

一つ目は、Colabがセルへ付加した利用者情報、実行時刻、内部ID、Colab専用のDataFrame表示を除去します。

二つ目は、全コードセルの実行番号、エラー出力、ローカル絶対パス、Colab固有メタデータ、公開に必要なファイルを検査します。

GitHubへpushした場合は、GitHub Actionsでも同じ検査を自動実行します。

## 参考文献

- Ashish Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), 2017.
- Jacob Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805), 2018.
- Sarthak Jain and Byron C. Wallace, [Attention is not Explanation](https://arxiv.org/abs/1902.10186), 2019.
- 中西崇文『ChatGPTはどのように動いているのか？』翔泳社、2026年。
