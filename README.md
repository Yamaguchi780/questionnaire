## 実行方法（初心者向け）

このツールは、回答 CSV（Google フォーム等）を読み込み、白紙のアンケート PDF に回答を書き込んで、全回答を 1 つの PDF にまとめて出力します。

---

### 1. 事前準備（Python の確認）

まず Python が入っているか確認します。

```bash
python3 --version
```

ない場合は Homebrew のダウンロード -> Python のダウンロードという手順を踏みましょう。
https://brew.sh/　から Homebrew をダウンロードしてください。

```bash
brew install python
```

### 2. パッケージのインストール

このプロジェクトでは PyPDF2, reportlab, pandas を使います。
PyPDF2 はバージョンによって挙動が変わるため、動作確認済みのバージョンを固定してインストールします。

```bash
pip3 install "PyPDF2==2.12.1" reportlab pandas
```

pip が見つからない場合は以下を試してください。(MacOS)

```bash
python3 -m pip install "PyPDF2==2.12.1" reportlab pandas
```

Windows の場合は Microsoft Store からインストールできるらしいです。

### 3. 入力ファイルを置く

年度ごとに input/<年度>/ フォルダを作り、その中に CSV と PDF を置きます。(名前は以下の例で統一してください)

```css
input/
  52回/
    回答.csv
    定期演奏会アンケート.pdf
  53回/
    回答.csv
    定期演奏会アンケート.pdf
```

### 4. 年度設定ファイルを用意する（ここを作れば動きます）

年度ごとにアンケート用紙（PDF）のレイアウトや設問数が違うため、  
**「どの設問を、PDF のどこに書くか」** を年度設定ファイルで指定します。

---

#### 4-1. `configs/` に年度ファイルを作る

新しい年度を作るときは、既存年度をコピーすると簡単です。設問が同じ（or 似てる）ものを選んでコピーしましょう。

```bash
cp configs/52回.py configs/53回.py
```

#### 4-2. テンプレ PDF を input におく。

入力 PDF は `input/<年度>/定期演奏会アンケート.pdf` に置きます。

#### 4-3. 設問の定義（`FIELDS`）を年度に合わせて編集する

`FIELDS` は「何をどこに書くか」を並べたリストです。  
設問が増えたら追加、減ったら削除するだけです。

主に使うのは次の 3 種類です。

- `TextDraw`：短い文字を 1 行で書く（例：名前）
- `CheckboxDraw`：選択肢にチェックを付ける（例：どこで知ったか）
- `BoxTextDraw`：自由記述を枠内に収める（自動縮小＆折り返し）

（例：自由記述欄を枠内に収める）

```python
BoxTextDraw(
    page_index=1,
    csv_key="all",
    x=68,
    y=515,
    box_width=346,
    box_height=80,
    max_font_size=12,
    min_font_size=3,
    line_spacing_ratio=1.2,
)
```

#### 4-4. CSV の列名（ヘッダー）と `csv_key` を一致させる

`csv_key` は **CSV の 1 行目（ヘッダー）** と一致している必要があります。  
合わない場合は、年度設定ファイル側の `csv_key` を CSV に合わせて変更してください。

（例：CSV ヘッダーに `name` があるなら）

```python
TextDraw(page_index=0, csv_key="name", x=260, y=205, font_size=12)
```

### 5. 実行する

年度を指定して run.py を実行します。

例：52 回を実行する場合

```bash
python3 run.py 52回
```

成功すると、出力先に PDF が作られます。

```bash
output/52回/まとめたアンケート.pdf
```
