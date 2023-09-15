from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import funciones_api as funciones

app = FastAPI()

# http://127.0.0.1:8000

@app.get(path="/", 
         response_class=HTMLResponse,
         tags=["Home"])