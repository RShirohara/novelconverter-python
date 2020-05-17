# Novel Converter

## Description

Pythonを使用して、小説をフォーマット毎に整形して標準出力で出力します。

## Usage

```bash
$novelconv [-h] [-f FROM_FORMAT] [-o OUTPUT] [-i INPUT] to_format
```

- -h: helpを出力
- -f, --from_format: 入力テキストのフォーマット指定
- -o, --output: 出力パスの指定
- -i, --input: 入力パスの指定
- to_format: 出力テキストのフォーマット指定

## フォーマット一覧

- ddmarkdown: [でんでんマークダウン](https://conv.denshochan.com/markdown)形式
- markdown: Markdown形式
- pixiv: [Pixiv](http://pixiv.net/novel)小説の形式
- plain: 可能な限りメタ表記を消して出力

## Install

[Github Release](https://github.com/RShirohara/NovelConvertor/releases)

## License

[The MIT License](./LICENSE)

## Author

[Ray Shirohara](https://github.com/RShirohara/)
