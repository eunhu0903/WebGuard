from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "WebGuard API is running"}