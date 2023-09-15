from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import funciones_api as funciones

app = FastAPI()

# http://127.0.0.1:8000

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Presentación de FastAPI</title>
    </head>
    <body>
        <header>
            <h1>Bienvenido a mi Aplicación FastAPI</h1>
        </header>
        <main>
            <p>Esta es una presentación simple de una página web construida con FastAPI.</p>
            <p>Puedes agregar más contenido y personalizarlo según tus necesidades.</p>
        </main>
        <footer>
            <p>&copy; - 2023 -  Juan Pablo Bertone</p>
        </footer>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)



