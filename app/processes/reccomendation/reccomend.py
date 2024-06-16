import requests
import numpy as np
from fastapi import FastAPI, HTTPException
from typing import List
from dataclasses_custom.FBT import FBT
import pandas as pd
import os

app = FastAPI()
url = 'http://api:8000/products'


@app.get('/get_reccomendations/{number}')
def get_reccomendations(number: int):
    try:
        documents = requests.get(url).json()
        profit = [item.get('sell_price') - item.get('buy_price') for item in documents if item.get('is_enabled')]
        if profit:
            profit = np.array(profit)/max(profit)*2/3
            quantites = [item.get('quantity') for item in documents]
            quantites = np.array(quantites)/max(quantites)*1/3
            score = profit+quantites
            names = [{"id":item.get('id'), "score":sc} for item,sc in zip(documents,score)]
            sorted_data = sorted(names, key=lambda x: x['score'], reverse=True)
            products = [requests.get(f'{url}/{item["id"]}').json() for item in sorted_data[:number]]
        else:
            products =[]
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post('/freq_together')
def frequently_bought_together(item_ids: List[str]):
    try:
        if os.path.exists('data/orders_from_db.csv'):
            df = pd.read_csv('data/orders_from_db.csv')
            fbt = FBT(df,threshold=0.1)
            products = [requests.get(f'{url}/{item}').json() for item in list(fbt.get_reccomendation(item_ids).keys())]
            return products
        else:
            return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put('/update_orders')
def update_orders(order: List[str]):
    try:
        if os.path.exists('data/orders_from_db.csv'):
            df = pd.read_csv('data/orders_from_db.csv')
            df.loc[len(df)] = [len(df),order]
            df.to_csv('data/orders_from_db.csv',index=False)

        else:
            data = {'ids':order}
            pd.DataFrame(data).to_csv('data/orders_from_db.csv')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))