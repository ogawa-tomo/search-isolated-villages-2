# 秘境集落探索ツール

## 概要
下記URLで公開している秘境集落探索ツールのソースコードです。  
<https://search-isolated-villages-2.herokuapp.com/>  
秘境集落を探索し、秘境度を人口分布データをもとに評価して地域別にランキングで出力します。  
集落のほか、下記の秘境施設も探索できます。
* 秘境郵便局
* 秘境小学校
* 秘境駅
* 秘境廃駅
* 秘境道の駅
* 秘境ニュータウン
* 秘境研究機関

## 主な利用データ
* E-statの国勢調査GISデータ<https://www.e-stat.go.jp/>
* 国土数値情報ダウンロードサービス<http://nlftp.mlit.go.jp/ksj/>
* R774@まとめ屋さんの訪問先まとめマップデータ<http://umap.openstreetmap.fr/ja/map/r774_368811#5/36.297/139.680>

## ローカル環境での実行方法
1. 本リポジトリをクローン
2. requirements.txtに記述したpython実行環境を用意
3. webif.pyを実行
4. localhost:5000にアクセス

## データの整備方法
本リポジトリはローカル環境で実行可能なよう整備されたデータが既に用意されているが、データを1から整備するには次の手順で行う。  
### 1. 生データの用意
* 郵便局データの用意
  1. 国土数値情報ダウンロードサービス<http://nlftp.mlit.go.jp/ksj/>より、郵便局を選択
  2. 全国を選択してダウンロード
  3. ダウンロードしたファイルを`raw_data/post_office_shp`ディレクトリに格納
* 小学校データの用意
  1. 国土数値情報ダウンロードサービス<http://nlftp.mlit.go.jp/ksj/>より、学校を選択
  2. 全国を選択してダウンロード
  3. ダウンロードしたファイルを`raw_data/elementary_school_shp`ディレクトリに格納
* 駅データの用意
  1. 国土数値情報ダウンロードサービス<http://nlftp.mlit.go.jp/ksj/>より、鉄道を選択
  2. 全国を選択してダウンロード
  3. ダウンロードしたファイルを`raw_data/station_shp`ディレクトリに格納  
* 廃駅データの用意
  1. 国土数値情報ダウンロードサービス<http://nlftp.mlit.go.jp/ksj/>より、鉄道時系列を選択
  2. 全国を選択してダウンロード
  3. ダウンロードしたファイルを`raw_data/abandoned_station_shp`ディレクトリに格納  
* 道の駅データの用意
  1. 国土数値情報ダウンロードサービス<http://nlftp.mlit.go.jp/ksj/>より、道の駅を選択
  2. 全国を選択してダウンロード
  3. ダウンロードしたファイルを`raw_data/michinoeki_shp`ディレクトリに格納
* ニュータウンデータの用意
  1. 国土数値情報ダウンロードサービス<http://nlftp.mlit.go.jp/ksj/>より、ニュータウンを選択
  2. 全て選択してダウンロード
  3. ダウンロードしたファイルを`raw_data/new_town_shp`ディレクトリに格納
* 研究機関データの用意
  1. 国土数値情報ダウンロードサービス<http://nlftp.mlit.go.jp/ksj/>より、研究機関を選択
  2. 全国を選択してダウンロード
  3. ダウンロードしたファイルを`raw_data/research_institute_shp`ディレクトリに格納
* R774@まとめ屋さんの訪問先まとめマップデータの用意
  1. <http://umap.openstreetmap.fr/ja/map/r774_368811#5/36.297/139.680>にアクセス
  2. 画面左のメニューより「サイトへのマップ埋め込みと共有」を洗濯
  3. geojson形式でデータをダウンロードし、`raw_data/r774_geojson`ディレクトリに格納

※その他に必要なメッシュ人口データ・メッシュ境界データ・小地域データは次の工程で自動的にダウンロードされる

### 2. データ生成
make_input.batを実行する  
※4,5時間くらいかかる  
※pypy実行環境が必要  
※inputディレクトリ下にcsvファイルが生成されていればOK


## 参考：メッシュ境界データ、人口データ、小地域データについて
* メッシュ境界データ
  * E-statホームページ（<https://www.e-stat.go.jp/>）の「統計GIS」→統計データダウンロード→境界データ→5次メッシュ→世界測地系緯度経度・Shape形式
* メッシュ人口データ
  * E-statホームページ（<https://www.e-stat.go.jp/>）の「統計GIS」→統計データダウンロード→統計データ→国勢調査→2015年→5次メッシュ→人口等基本集計に関する事項
* 小地域データ
  * E-statホームページ（<https://www.e-stat.go.jp/>）の「統計GIS」→統計データダウンロード→境界データ→小地域→国勢調査→2015年→小地域→世界測地系緯度経度・Shape形式


## 参考：pypyの環境構築例（Windowsの場合）
要するに公式<http://pypy.org/download.html>からダウンロードし、解凍したものを好きな場所に置き、Pathを通せばいい  
参考：<https://stackoverflow.com/questions/9893317/how-to-use-pypy-on-windows>  
32bit版でよい  
インストールしたのはpypy3なので、実行するには以下のようにする  
`pypy3 [pythonファイル名]`  
pypy3へのpipのインストール  
	`pypy3 -m ensurepip`  
	参考：<http://doc.pypy.org/en/latest/install.html>  
pipを用いたpypyへのtqdmのインストール  
	`pypy3 -m pip install tqdm`  
	参考：<https://gist.github.com/tos-kamiya/9ba8f26885fb459b704b>  
	

