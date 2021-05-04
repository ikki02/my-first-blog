# 推論API
APIの仕様書はhttp://0.0.0.0:80/docsまたはhttp://0.0.0.0:80/redocにて確認できる。
以下、機能の概要。

- バッチ推論  
test.csvをAPIにPOSTし、csvの各行に対して推論。推論結果をストレージに保存する。  
HTTPステータスコードはPOST後すぐに返し、推論結果は非同期で処理する。
- 推論データダウンロード  
予め保存された推論結果を読込、推論結果をJSON形式で返す。
- オンライン推論（おまけ）  
JSONデータをAPIにPOSTすることで、推論結果をJSON形式で返す。  
- 訓練（おまけ）  
train.csvをAPIにPOSTし、そのデータを用いて訓練後、モデルをストレージに保存する。  
HTTPステータスコードはPOST後すぐに返し、訓練は非同期で処理する。  
本APIでは、scikit-learnのStandardScaaler()とLogisticRegression()をパイプラインに、   
グリッドサーチと10分割の交差検証を実施してモデリングする。  
test_dataに対する精度は95%程度。  

※全てヘッダー認証必要.

# 環境
- MacOS BigSur 11.2
- Docker
- minikube v1.17.1
- kubectl Client v1.19.3
- kubectl Server v1.20.2
- Python 3.8.7
- pipenv (version 2020.11.15)
- FastAPI 0.63.0
- Pandas 1.2.2
- scikit-learn 0.24.1


# Installation
dockerイメージを用意する。

```
$ sh scripts/docker_build.sh 
```

コンテナを起動する。

```
$ sh scripts/docker_run.sh 
```

起動を確認する。

```
$ docker ps 
$ curl -X GET "http://0.0.0.0:80/" -H  "accept: text/plain" -H  "x-token: coneofsilence"
```

# Usage



## バッチ推論
@以下にアップロードしたいtest.csvのパスを任意に指定します。

```
curl -X POST "http://0.0.0.0:80/api/v1/predict/batch/" -H  "accept: application/json" -H  "x-token: coneofsilence" -H  "Content-Type: multipart/form-data" -F "csv_file=@ml_api/data/test/test.csv;type=text/csv"
```

## 推論データダウンロード

```
curl -X GET "http://0.0.0.0:80/api/v1/load?filename=sample_for_test.csv" -H  "accept: application/json" -H  "x-token: coneofsilence"
```

## オンライン予測（おまけ）

```
curl -X POST "http://0.0.0.0:80/api/v1/predict/online/" -H  "accept: application/json" -H  "Content-Type: application/json" -H  "x-token: coneofsilence" -d "{\"data\": [{\"item_id\": 6000,\"sold_price\": 1006,\"diff_price\": 0,\"capital_area\": 0,\"status\": 2,\"size\": 4,\"listing_at_spring\": 1},{\"item_id\": 5532,\"sold_price\": 1149,\"diff_price\": -2,\"capital_area\": 0,\"status\": 0,\"size\": 3,\"listing_at_spring\": 1}]}"
```

## 訓練（おまけ）
モデルは以下のようにして用意。

```
curl -X POST "http://0.0.0.0:80/api/v1/train/" -H  "accept: text/plain" -H  "x-token: coneofsilence" -H  "Content-Type: multipart/form-data" -F "csv_file=@ml_api/data/train/train.csv;type=text/csv"
```

マイクロサービス的に考えるなら訓練と推論は分けるケースも考えられるが、
今回の訓練APIは技術課題の範囲ではないこと、
インターフェースを統合し利便性をあげたかったこと、
を理由に一旦1つのAPIに統合することにした。

# Test

```
$ export BASE_DIR=$(pwd)
$ pytest
```
`ml_api/tests`以下に単体テストのスクリプトがあり、それを実行する。
また、入力と出力の型テストはFastAPI側で自動でしてくれるように実装。

ライブラリが手元のローカルマシンにない場合は、仮想環境を構築しその中で実行する。

```
$ pipenv install -r requirements.txt
$ pipenv shell
```
※ OSがMacOS BigSurの場合挙動が不安定なことがあったため、最悪コンテナ内で確認することも可能です。

```
$ docker run -it --rm myapi:v1 /bin/bash
$ pytest
```

# minikube
minikubeのデプロイ
```
$ sh scripts/minikube_deploy.sh
```
IPとポートが表示されるのでそれらの値に対して、上記curlコマンドを実行できる。

動作確認後のリソース削除
```
$ sh scripts/minikube_delete.sh
```

# Reference
FastAPIのめちゃくちゃ分かりやすいスライド
https://speakerdeck.com/amaotone/goodbye-flask-welcome-fastapi

FastAPI公式
https://fastapi.tiangolo.com
