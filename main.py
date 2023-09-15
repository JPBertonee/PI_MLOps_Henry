from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import funciones_api as funciones
import pandas as pd 

app = FastAPI()

df_items_full = pd.read_parquet('data/df_items_full.parquet')
df_f1 = pd.read_parquet('data/df_f1.parquet')
df_items_recommend = pd.read_parquet('data/df_items_recommend.parquet')
df_f2 = pd.read_parquet('data/df_f2.parquet')
df_ranking = pd.read_parquet('data/df_ranking.parquet')
df_user_genre= pd.read_parquet('data/df_user_genre.parquet')
df_f5 = pd.read_parquet('data/df_f5.parquet')
df_f6 = pd.read_parquet('data/df_f6.parquet')

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

@app.get("/userdata/{user_id}", name = "userdata (user_id)")
async def userdata(user_id:str):
    '''
    La siguiente función filtra por el usuario pasado como argumento
    y arroja el dinero gastado por dicho usuario, el porcentaje de recomendación 
    y la cantidad de items del mismo. 
    
    Argumento:
    user_id (str): ID de identifiación del usuario 
    
    '''
    # Verificamos si el usuario existe en el DataFrame
    if user_id in df_f1['user_id'].values and user_id in df_items_recommend['user_id'].values and user_id in df_items_full['user_id'].values:
        # Calcula la suma de la columna precio filtrando por el usuario.
        money = df_f1[df_f1['user_id'] == user_id]['price'].sum().item()
        
        # Calcula la cantidad de reviews totales de todos los usuarios en el DataFrame df_reviews_full.
        tot_recommend = df_items_recommend[df_items_recommend['user_id'] == user_id]['recommend'].sum()
       
        # Calcula la cantidad de reviews filtrando por el usuario en el DataFrame df_reviews_full.
        tot_items = df_items_recommend[df_items_recommend['user_id'] == user_id]['items_count'].iloc[0].item()
        
        # Calcula la cantidad de items filtrando por el usuario en el DataFrame df_items_full.
        cant_items = df_items_full[df_items_full['user_id'] == user_id]['items_count'].iloc[0].item()

        return {'Usuario:': user_id,
                'Cantidad de dinero gastado:': money,
                # Hacemos el cociente para calcular el porcentaje.
                'Porcentaje de recomendación:': round((tot_recommend / tot_items) * 100, 2),
                'Cantidad de items:': cant_items
                }
    else:
        return 'Usuario no encontrado'




