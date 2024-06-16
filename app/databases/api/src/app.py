from fastapi import FastAPI

from dotenv import load_dotenv
load_dotenv()  # noqa

from clients.postgres import init_db
from router import router


app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/heartbeat")
async def heartbeat():
    return {"status": "OK"}

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
