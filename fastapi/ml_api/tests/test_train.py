import json
import os
import sys
BASE_DIR = os.getenv("BASE_DIR", "/deploy")
sys.path.append(BASE_DIR)

import pandas as pd
from fastapi.testclient import TestClient

from ml_api.main import app

client = TestClient(app)


def test_get_root_good_token():
    response = client.get("/", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.text == "ML PREDICTION API\n"


def test_get_root_bad_token():
    response = client.get("/", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_is_traindata(csv_path="ml_api/data/train/train.csv"):
    assert os.path.isfile(csv_path)


def test_traindata_schema(csv_path="ml_api/data/train/train.csv"):
    expected = ['item_id', 'target_label', 'sold_price', 'diff_price', 'capital_area', 'status', 'size', 'listing_at_spring']
    assert pd.read_csv(csv_path).columns.tolist() == expected


def test_post_train():
    csv_path = "ml_api/data/train/train.csv"
    test_is_traindata(csv_path=csv_path)
    train_csv = {"csv_file": ("train.csv", open(BASE_DIR+'/'+csv_path, "rb"))}
    response = client.post("/api/v1/train/", headers={"X-Token": "coneofsilence"}, files=train_csv)
    assert response.status_code == 200


def test_model_score():
    '''訓練の精度のバリデーション（ベースラインより高いかどうか判定）（未着手）'''


def test_is_no_garbage():
    assert not os.path.isfile("/tmp/train.csv")
