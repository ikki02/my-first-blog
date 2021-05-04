import shutil

import pandas as pd
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, BackgroundTasks
from fastapi.responses import PlainTextResponse

from ml_api import schemas, file_utils
from ml_api.ml import MLAPI


fake_secret_token = "coneofsilence"
ml = MLAPI()
app = FastAPI()


@app.get("/", status_code=200, response_class=PlainTextResponse)
async def read_root(x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    return "ML PREDICTION API\n"


@app.post("/api/v1/predict/batch/", status_code=200, response_model=schemas.Filepath)
async def batch_prediction(background_tasks: BackgroundTasks, csv_file: UploadFile = File(...), x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    with open("/tmp/" + csv_file.filename, "wb") as buffer:
        shutil.copyfileobj(csv_file.file, buffer)
    df = pd.read_csv("/tmp/" + csv_file.filename, sep=",")

    if not file_utils.check_csv(df):
        await file_utils.cleanup("/tmp/" + csv_file.filename, df) # raiseエラーする場合、backgroud_tasksが動かない説
        raise HTTPException(status_code=400, detail="Invalid test data")
    local_save_path = file_utils.get_filepath()
    background_tasks.add_task(file_utils.save_csv, df, local_save_path)
    background_tasks.add_task(ml.batch_predict, local_save_path)
    background_tasks.add_task(file_utils.cleanup, "/tmp/" + csv_file.filename, df)
    return {"filepath": local_save_path.split('/')[-1]}


@app.get('/api/v1/load', status_code=200, response_model=schemas.Output)
async def load(filename: str, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if not file_utils.check_outputs(filename):
        raise HTTPException(status_code=404, detail="the result of prediction does not exist")
    preds = await file_utils.load_outputs(filename)
    return {"prediction": preds}


@app.post("/api/v1/predict/online/", status_code=200, response_model=schemas.Output)
async def online_prediction(data: schemas.Input, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    data_dict = data.dict().get("data")
    data = [{
        "item_id": data["item_id"]
        , "sold_price": data["sold_price"]
        , "diff_price": data["diff_price"]
        , "capital_area": data["capital_area"]
        , "status": data["status"]
        , "size": data["size"]
        , "listing_at_spring": data["listing_at_spring"]} for data in data_dict]
    df = pd.DataFrame(data)
    pred = ml.online_predict(df.to_numpy())
    df['target_label_pred'] = pred
    pred = df.to_dict(orient='records')
    return {"prediction": pred}


@app.post("/api/v1/train/", status_code=200, response_class=PlainTextResponse)
async def train(background_tasks: BackgroundTasks, csv_file: UploadFile = File(...), x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    with open("/tmp/" + csv_file.filename, "wb") as buffer:
        shutil.copyfileobj(csv_file.file, buffer)
    df = pd.read_csv("/tmp/" + csv_file.filename, sep=",")

    background_tasks.add_task(ml.train, df)
    background_tasks.add_task(file_utils.cleanup, "/tmp/" + csv_file.filename, df)
    return "ML Training Started using data {}".format(csv_file.filename)
