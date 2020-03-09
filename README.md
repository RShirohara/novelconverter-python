# Novel Converter

## Description

Pythonを使用して、小説をフォーマット毎に整形して標準出力で出力します。

## Usage

```bash
$python3 NovelConv.py "form" [-p "path"] [-f "imput_form"]
```

* "form": フォーマット名
  * markdown    : markdown形式
  * pixiv       : [Pixiv](http://pixiv.net)小説形式
  * ddmarkdown  : [でんでんマークダウン](https://conv.denshochan.com/markdown)形式(一部対応)
* -p "path" : 入力ファイルのパス (指定が無い場合標準入力から)
* -f "imput_form" : 入力のフォーマット指定

## Install

[Github Release](https://github.com/RShirohara/NovelConvertor/releases)

## License

[The MIT License](./LICENSE)

## Author

[Ray Shirohara](https://github.com/RShirohara/)
