# Pythonで始める数理最適化勉強用のレポジトリ
「Pythonで始める数理最適化」の内容を勉強するためのレポジトリです。
 #### ipynbファイルをpyファイルに変換する方法
  - ターゲットディレクトリに移動します。
    ```bash
    cd ./ch03
    ```
  - 次のコマンドを入力し、そのディレクトリ内のipynbファイルをpythonファイルに変換します。
    ```bash
    jupyter nbconvert --to python *.ipynb
    ```
 #### テスト実行方法
  - 自作のライブラリを読み込んでテストを実行させるため、次のようなコマンドを入力してpytestを実行
    ```bash
    python -m pytest ./ch03/test_optimization_result.py 
    ```
 #### 参考URL
  - [対象本のGitHubレポジトリ](https://github.com/ohmsha/PyOptBook)
