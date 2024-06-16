from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()


class Number(BaseModel):
    value: int

# add opinion about the product to the database
@app.get("/add_opinion/add_opinion/")
async def add_customer_opinion(user_id: int = Query(default=1), 
                               product_id: int = Query(default=1),
                               opinion_text: str = Query(dafault='')):
    opinion_status: str = 'NULL'
    if opinion_status == 'PASS':
        return 'Opinion added'
    else:
        return {'ERROR' : opinion_status}

# chceck if customer bought the product given their id
@app.get("/add_opinion/check_if_bought/")
async def check_if_bought(user_id: int = Query(default=1), 
                          product_id: int = Query(default=1)):
    opinion_status: str = 'NULL'
    if opinion_status == 'PASS':
        return 'Opinion added'
    else:
        return {'ERROR' : opinion_status}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
