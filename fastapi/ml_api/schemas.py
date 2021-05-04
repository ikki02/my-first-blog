from pydantic import BaseModel
from typing import List

# request
class Record(BaseModel):
    item_id: int
    sold_price: int
    diff_price: int
    capital_area: int
    status: int
    size: int
    listing_at_spring: int

class Input(BaseModel):
    data: List[Record]

# response
class Filepath(BaseModel):
    filepath: str

class Prediction(Record):
    target_label_pred: float

class Output(BaseModel):
    prediction: List[Prediction]
