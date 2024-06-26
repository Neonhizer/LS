from fastapi import FastAPI
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from pyod.models.knn import KNN


app = FastAPI()

neigh = None
clf = None

@app.on_event("startup")
def load_train_model():
    df = pd.read_csv("iris_ok.csv")
    global neigh, clf
    neigh = KNeighborsClassifier(
        n_neighbors=len(np.unique(df['y'])))
    neigh.fit(df[df.columns[:4]].values.tolist(), 
              df['y'])
    clf = KNN()
    clf.fit(df[df.columns[:4]].values.tolist(), 
              df['y'])   
    print("Training finished!")


@app.get("/anomaly")
def anomaly(p1: float, p2: float, p3: float, p4: float):
    result = clf.predict([[p1, p2, p3, p4]])[0]
    return {'result': int(result)}


@app.get("/predict")
def predict(p1: float, p2: float, p3: float, p4: float):
    result = neigh.predict([[p1, p2, p3, p4]])[0]
    return {'result': int(result)}


@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    import os
    uvicorn.run(app, host=os.environ['HOST'],
                 port=os.environ['PORT'])