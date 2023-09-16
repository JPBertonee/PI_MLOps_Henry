"""
FUNCIONES API's
"""


# IMPORTAMOS LIBRERIAS A UTILIZAR
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd


# INSTANCIAMOS LA APLICACION 
app = FastAPI()


# LECTURA DE ARCHIVOS UTILIZADOS EN LAS FUNCIONES
 
df_items_full = pd.read_parquet('data/df_items_full.parquet')
df_f1 = pd.read_parquet('data/df_f1.parquet')
df_reviews_full = pd.read_parquet('data/df_reviews_full.parquet')
df_f2 = pd.read_parquet('data/df_f2.parquet')
df_ranking = pd.read_parquet('data/df_ranking.parquet')
df_user_genre= pd.read_parquet('data/df_user_genre.parquet')
df_f5 = pd.read_parquet('data/df_f5.parquet')
df_f6 = pd.read_parquet('data/df_f6.parquet')


# PRESENTACION API
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


# FUNCION 1
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
        money = df_f1[df_f1['user_id'] == user_id]['price'].sum()
        
        # Calcula la cantidad de reviews para el usuario. 
        tot_recommend = df_reviews_full[df_reviews_full['user_id'] == user_id]['recommend'].sum()
       
        # Calcula la cantidad de reviews filtrando por el usuario en el DataFrame df_reviews_full.
        tot_items = df_items_full[df_items_full['user_id'] == user_id]['items_count'].iloc[0]

        return {'Usuario:': user_id,
                'Cantidad de dinero gastado:': money,
                # Hacemos el cociente para calcular el porcentaje.
                'Porcentaje de recomendación:': round((tot_recommend / tot_items) * 100, 2),
                'Cantidad de items:': tot_items
                }
    else:
        return 'Usuario no encontrado'



# FUNCION 2
@app.get("/countreviews/{inicio}/{fin}", name = "countreviews (Fecha Inicio / Fecha Fin)")
def countreviews(inicio, fin):
    '''
    Calcula la cantidad de usuarios que realizaron reviews entre las fechas dadas y 
    el porcentaje de recomendacion de esos usuarios.
    
    Argumentos:
    
    inicio (str): Fecha de inicio del periodo a evaluar.
    
    fin (str): Fecha de fin del periodo a evaluar
    '''
    inicio = pd.to_datetime(inicio)
    fin = pd.to_datetime(fin) 
    
    # Filtra las filas del DataFrame que estén dentro del rango de fechas
    reviews_entre_fechas = df_f2[(df_f2['posted'] >= inicio) & (df_f2['posted'] <= fin)]
    
    # Calcula la cantidad de usuarios únicos que realizaron reviews en ese período
    cantidad_usuarios = reviews_entre_fechas['user_id'].nunique()
    
    reviews_reco = round(reviews_entre_fechas['recommend'].sum() / reviews_entre_fechas['recommend'].count() * 100,2).item()
    
    return {'Cantidad de usuarios:': cantidad_usuarios,
            # Hacemos el cociente para calcular el porcentaje.
        'Porcentaje de recomendación:': reviews_reco
    }
    
    
# FUNCION 3
@app.get("/genre/{genero}", name = "Genre (Genero)")
def genre(genero):

    '''
    Esta función nos aroja en que puesto del ranking 'Playtime_Forever' se encuentra 
    el género pasado como input.

    Argumento: 
    
    genre (str): El género de juegos del cual se quiere conocer el ranking de horas jugadas. 

    '''
    # Filtramos el ranking según el género
    posicion = df_ranking[df_ranking['genres'] == genero]['Posicion'].iloc[0].item()
    
    return {'El género': genero, 
            'se encuentra en la posición':posicion
    }

    
# FUNCION 4
@app.get("/userforgenre/{genre}", name = "User for Genre (Genero)")
def userforgenre(genre):
    '''
    Devuelve el TOP 5 de usuarios con más horas jugadas en un género específico.

    Argumento:
    
    genre (str): El género de juegos para el que se desea obtener el TOP 5 de usuarios.
    
    '''

    # Filtrar el DataFrame para obtener datos específicos del género
    data = df_user_genre[df_user_genre['genres'] == genre]

    # Tomar los primeros 5 registros del DataFrame
    top5 = data[['user_id', 'user_url', 'playtime_forever']].head(5).reset_index(drop=True)

    return  {'El TOP 5 de usuarios para el género' : genre, 
             'es el siguiente' : top5}
    

# FUNCION 5
@app.get("/developer/{desarrollador}", name = "Developer (Desarrollador)")
def developer(desarrollador):

    '''
    Devuelve cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.

    Argumento:
    
    desarrolador (str): El developer del juego (item) para el cual se desea obtener los valores mencionados. 

    '''

    # Filtramos el DataFrame por el desarrollador dado
    developer_df = df_f5[df_f5['developer'] == desarrollador]

    # Calculamos la cantidad de ítems gratuitos (Free) por año para el desarrollador
    items_free_por_anio = developer_df[developer_df['price'] == 0].groupby(developer_df['release_date'].dt.year)['item_id'].nunique()

    # Calculamos la cantidad total de ítems por año para el desarrollador
    items_totales_por_anio = developer_df.groupby(developer_df['release_date'].dt.year)['item_id'].nunique()

    # Rellenamos los años faltantes en el DataFrame de items_free_por_anio con ceros para que no arroje error el dataframe
    for year in items_totales_por_anio.index:
        if year not in items_free_por_anio.index:
            items_free_por_anio[year] = 0

    # Ordenamos el DataFrame por año
    items_free_por_anio = items_free_por_anio.sort_index()

    # Calculamos el porcentaje de contenido Free por año
    porcentaje_free = (items_free_por_anio / items_totales_por_anio) * 100

    resultados = pd.DataFrame({
        'Año': items_free_por_anio.index,
        'Cantidad de Items': items_totales_por_anio.values,
        'Porcentaje Free': porcentaje_free.values
    })
    
    return resultados.to_dict(orient = 'records')


# FUNCION 6
@app.get("/sentimet_analysis/{anio}", name = "Análisis de Sentimiento (Año)")
def sentiment_analysis(anio):
    ''' 
    Devuelve un DataFrame con la cantidad de registros de reseñas de usuarios categorizados por análisis de sentimiento para un año específico.
    
    Argumentos:
    
    anio (int): Año en el cual queremos obtener el análisis de sentimiento.
    df_f6 (DataFrame): El DataFrame que contiene los datos de reseñas y sentimientos.
   
    '''
    
    df_f6['anio'] = df_f6['anio'].astype(int)    
    
    # Filtramos el DataFrame según el año definido como argumento
    df_filtered = df_f6[df_f6['anio'] == anio]
    df_filtered['sentimiento'] = df_f6['sentimiento'].astype(int)
    
    # Iniciamos contadores
    positivos = 0
    negativos = 0
    neutros = 0 
    
    # Obtenemos la cantidad de valores positivos, negativos y neutros
    for i in df_filtered['sentimiento']:
        if i == 2:
            positivos += 1
        elif i == 1:
            neutros += 1
        elif i == 0:
            negativos += 1 
            
    # Crear un DataFrame con los resultados
    return {
        'Positivos': positivos,
        'Neutros': neutros,
        'Negativos': negativos
    }
