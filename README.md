# pyquest

Python + Streamlit で作られた、ローカル保存型のクイズアプリです。Pythonの基礎を50問収録しています。

## PLAY

https://pyquest-mhybpd8dgt6bjxhfs86fpy.streamlit.app

## 機能概要

- 問題に回答すると挑戦した問題数/正解数を保存
- `save.json`：累計スコアを保存・読み込み
- 50問解答した場合、リセットで再度成績をカウントできます
- 現時点ではローカルでの動作に最適化されています

##  起動方法

```bash
git clone https://github.com/your-username/quiz-app.git
cd quiz-app
streamlit run main.py
```
※ 起動しない場合
```
python -m streamlit run app.py
```

## 注意
※ Python 3.8+ 推奨

現在は1ユーザ用のローカル保存仕様です。複数人での利用や外部公開時のセーブデータの競合には対応しておりません。現時点の公開版を使用したい方は、セッションの重複にご注意の上ご利用ください。

## 開発者向け
addex.py は開発補助スクリプトのため、.gitignore に追加済

今後の予定：ユーザ管理・認証機能の追加、問題追加
