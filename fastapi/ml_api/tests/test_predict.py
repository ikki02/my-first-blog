import json
import os
import sys
BASE_DIR = os.getenv("BASE_DIR", "/deploy")
sys.path.append(BASE_DIR)

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


def test_is_model():
    MODEL_NAME = "LogisticRegression.sav"
    MODEL_PATH = os.path.join(BASE_DIR, f"ml_api/data/train/models/{MODEL_NAME}")
    assert os.path.isfile(MODEL_PATH)


def test_is_testdata(csv_path="ml_api/data/test/test.csv"):
    assert os.path.isfile(csv_path)


def test_post_batch_prediction():
    csv_path = "ml_api/data/test/test.csv"
    test_is_testdata(csv_path=csv_path)
    test_csv = {"csv_file": ("test.csv", open(BASE_DIR+'/'+csv_path, "rb"))}
    response = client.post("/api/v1/predict/batch/", headers={"X-Token": "coneofsilence"}, files=test_csv)
    assert response.status_code == 200


def test_post_batch_prediction_error():
    csv_path = "ml_api/data/test/test_error.csv"
    test_is_testdata(csv_path=csv_path)
    test_csv = {"csv_file": ("test.csv", open(BASE_DIR+'/'+csv_path, "rb"))}
    response = client.post("/api/v1/predict/batch/", headers={"X-Token": "coneofsilence"}, files=test_csv)
    print(response.status_code)
    assert response.status_code == 400


def test_is_no_garbage():
    assert not os.path.isfile("/tmp/test.csv")
    assert not os.path.isfile("/tmp/test_error.csv")


def test_get_predicted_data():
    response = client.get("/api/v1/load/", headers={"X-Token": "coneofsilence"}, params={"filename": "sample_for_test.csv"})
    assert response.status_code == 200


def test_post_online_prediction():
    # オンライン推論の動作確認（型確認もfastAPIで同時に行っている）
    with open(BASE_DIR+"/ml_api/event.json", "r") as rf:
        test_data_dict = json.load(rf)
        test_data = json.dumps(test_data_dict)
    response = client.post("/api/v1/predict/online/", headers={"X-Token": "coneofsilence"}, data=test_data)
    assert response.status_code == 200


def test_post_online_prediction_expected():
    with open(BASE_DIR+"/ml_api/event.json", "r") as rf:
        test_data_dict = json.load(rf)
        test_data = json.dumps(test_data_dict)
    response = client.post("/api/v1/predict/online/", headers={"X-Token": "coneofsilence"}, data=test_data)
    expected = '{"prediction":[{"item_id":6000,"sold_price":1006,"diff_price":0,"capital_area":0,"status":2,"size":4,"listing_at_spring":1,"target_label_pred":0.0},{"item_id":5532,"sold_price":1149,"diff_price":-2,"capital_area":0,"status":0,"size":3,"listing_at_spring":1,"target_label_pred":0.0}]}'
    assert response.text == expected
