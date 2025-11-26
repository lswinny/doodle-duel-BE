from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World2"}

@app.get("/scoreImage")
async def get():
    return {"newMessage": "New Endpoint"}
