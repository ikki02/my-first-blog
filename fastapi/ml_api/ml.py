import os
import pickle

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
# from google.cloud import storage

from ml_api import file_utils


class MLAPI:
    def __init__(self):
        self.BASE_DIR = os.getenv("BASE_DIR", "/deploy")
        self.MODEL_NAME = "LogisticRegression.sav"
        self.MODEL_PATH = os.path.join(self.BASE_DIR, f"ml_api/data/train/models/{self.MODEL_NAME}")
        try: 
            self.model = pickle.load(open(self.MODEL_PATH, "rb"))
        except:
            print('no model file')

    def preprocess(self, df):
        return df

    def train(self, df):
        y = df['target_label']
        X = df.loc[:, ['item_id', 'sold_price', 'diff_price', 'capital_area', 'status', 'size', 'listing_at_spring']]
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
        pipe = make_pipeline(StandardScaler(), LogisticRegression())
        param_grid = {'logisticregression__C': [0.001, 0.1, 10]}
        grid = GridSearchCV(pipe, param_grid, cv=10, verbose=1, n_jobs=-1)
        grid.fit(X_train, y_train)
        print(f'Best parameters:\n{grid.best_params_}')
        print(f'Best estimator:\n{grid.best_estimator_}')
        coefs = grid.best_estimator_.named_steps["logisticregression"].coef_[0]
        coef_dict = dict(zip(X.columns, coefs))
        print(f'Logistic regression coefficients:\n{coef_dict}')
        print(f'Test score: {grid.score(X_test, y_test):.2f}')
        model = 'ml_api/data/train/models/LogisticRegression.sav'
        pickle.dump(grid.best_estimator_, open(model, 'wb'))
        # 実運用ではGCSやS3にモデルをアップすると思う
        '''
        bucket = storage.Client().bucket(BUCKET_NAME)
        blob = bucket.blob('{}/{}'.format(
            datetime.datetime.now().strftime('category_classifier_%Y%m%d_%H%M%S'),
            model))
        blob.upload_from_filename(model)
        '''

    async def batch_predict(self, filepath: str):
        df = pd.read_csv(filepath)
        pred = self.model.predict(df.to_numpy())
        df['target_label_pred'] = pred
        file_utils.save_outputs(df, filepath.split('/')[-1])

    def online_predict(self, x):
        """
        - Prediction using self.model
        - Post-process
        """
        out = self.model.predict(x)
        return out
