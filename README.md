# @74th の 技術書典用ビルドツール

@74th が技術書典用の本を作る時に使っているツールの共有です。
人に使ってもらうためにリソースを整えたものではありませんが、どんな感じに使っているかどうか解ると思います。

以前は Re:View を使っていましたが、ここ 3 冊はこれを使っています。

また、使用しているコンテンツは [VS Code Ninja Guide](https://74th.booth.pm/items/1973166) ですが、このコンテンツに含まれる全ての本文がこの中に含まれているわけではありません。

## なぜこれを使っているか

- Markdown ベースで入稿データを作りたい。
- Markdown だと表現力が足りない部分を、HTML で補完したい。
- Re:View だと表現力が足りない部分を、LaTeX で補完するのは辛かったから。

## 主に使っているツール

- [markdown-pdf-cli](https://github.com/74th/markdown-pdf-cli) : [VS Code の Markdown を PDF に変換するツール](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf) が、絵文字や PlantUML に対応していて、素敵なので Markdown から HTML にする部分に使っています。
- [Vivlio Style](https://vivliostyle.org/) : CSS 組版。A5 サイズに組版する、目次ページを作る、
- Chrome Browser : Vivlio Style HTML -> PDF
- macOS Preview : PDF への文字の埋め込み

## 必要なもの

- Python 3.6 以降
- Node.js
- Chrome Browser
- macOS

## 環境の準備

```
# タスクランナー Invoke のインストール
pip install invoke

# NPM のツールのインストール
npm install -g yarn
yarn
```

## 原稿のフォルダ

- [Markdown 原稿のサンプル](https://github.com/74th/techbook-builder/blame/master/article/1.file.md)

## 入稿ファイルのビルド

- `inv build`
  - markdown-pdf-cli を使って、 HTML の生成
- `inv open-vivliostyle`
  - Vivlio Style のダウンロードと、http-server の実行
- Chrome で右ページを開く http://127.0.0.1:8000/vivliostyle-viewer/vivliostyle-viewer.html#b=http://127.0.0.1:8000/contents.html&renderAllPages=true&userStyle=data:,/*%3Cviewer%3E*/%0A@page%20%7B%20size:%20A5;%20%7D%0A/*%3C/viewer%3E*/
  - Vivlio Style を開き、生成された HTML へのレンダリング指示、A5 サイズなどの指定が URL に入っている
- Chrome で Ctrl+P を押して、PDF として印刷
- PDF を macOS の Preview で開き、export PDF で PDF を PDF として出力
  - フォントの埋め込み
- macOS の Preview で、annotation でテキストの追加ができるので、ページ番号の入っていないページに、ページ境界にページ番号を書き込む（[ノンブルの追加](http://www.nikko-pc.com/offset/faq/off-faq.html#3-1)）

## 細かい設定など

- markdown-pdf-cli の設定 [settings.yaml](./settings.yaml)
  - https://github.com/yzane/vscode-markdown-pdf#options の設定を CLI では YAML に落としている
- タスク [tasks.py](./tasks.py)
  - chapters に章番号と、マークダウンファイルの対応表が書かれている。0 となっているものは、章番号をふらないもの。
  - `# xxxx`が`<h1>xxxx</h1>`と h1 タグになるので、章の見出しと判断し、少番号の付与と、HTML のタイトル（Vivlio Style ではヘッダータイトルに使われる）に追加。
  - `## xxxx`が`<h2>xxxx</h2>`と h2 タグになるので、節の見出しと判断し、節番号`3.2`を付与。
  - h1、h2 タグで収集したデータを使って、[目次ページ ./contents.html](./contents.html)を作成。
  - というような体裁のがちゃがちゃを、HTML を XML ファイルとみなして、Python でやっています。

## 諦めていること、今やっていないこと

- 節見出しのヘッダーへの追加。Vivlio Style では現状ファイルを分けなければ見出しを変えられないため。
- ePub の生成。
