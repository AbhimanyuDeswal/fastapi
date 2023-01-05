from fastapi import FastAPI
from fastapi import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/createpost")
async def create_post(payload:dict = Body(...)):
    print(payload)
    return {"body": f"{payload}"}