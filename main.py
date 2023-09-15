from fastapi import FastAPI
import funciones_api as funciones

app = FastAPI()

# http://127.0.0.1:8000

@app.get("/")

