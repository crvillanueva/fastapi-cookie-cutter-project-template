from fastapi import FastAPI

app = FastAPI(title=" API")


@app.get("/")
async def root():
    return {"msg": "Hello"}
