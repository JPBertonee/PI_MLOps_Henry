"""
FUNCIONES API's
"""


# IMPORTAMOS LIBRERIAS A UTILIZAR
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# INSTANCIAMOS LA APLICACION 
app = FastAPI()


# LECTURA DE ARCHIVOS UTILIZADOS EN LAS FUNCIONES
df_f1 = pd.read_parquet('data/df_f1.parquet')
df_f1_2 = pd.read_parquet('data/df_f1_2.parquet')
df_f1_3 = pd.read_parquet('data/df_f1_3.parquet')
df_f2 = pd.read_parquet('data/df_f2.parquet')
df_ranking = pd.read_parquet('data/df_ranking.parquet')
df_user_genre= pd.read_parquet('data/df_user_genre.parquet')
df_f5 = pd.read_parquet('data/df_f5.parquet')
df_f6 = pd.read_parquet('data/df_f6.parquet')

# Definir funciones de carga de datos bajo demanda
def cargar_datos_modelo():
    df_modelo_final = pd.read_parquet('data/df_modelo_final.parquet')
    return df_modelo_final

def cerrar_datos(df):
    df.close()

# HTML de la página de presentación
pagina_presentacion = """
<!DOCTYPE html>
<html>
<head>
    <title>Mi Página Web en FastAPI</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 5px;
        }
        h1 {
            color: #333;
        }
        p {
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bienvenido a mi entorno FastAPI</h1>
        <p>A continuación encontrará 6 funciones que le permitirán obtener información acerca de la plataforma de juegos Steam.</p>
        <p>Para poder acceder a ellas, le recomiento agregar en la url actual, lo siguiente --> /docs.</p>
        <b>Ejemplo: www.suURL.com/docs.</b>
        <p>De esta manera podrá acceder a la información de las funciones y entender el contexto y como utilizarlas.</p>
        <div>
        <p>Autor: Juan Pablo Bertone. <2023></p>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def mostrar_pagina_presentacion():
    return pagina_presentacion


# FUNCION 1
@app.get("/userdata/{user_id}", name = "USERDATA")
async def userdata(user_id:str):
    '''
    <b>Objetivo:</b>
    
    Devuelve, para el usuario pasado como parametro,
    el dinero gastado, el porcentaje de recomendación 
    y la cantidad de items del mismo.
    
    <b>Argumento:</b>
    
    user_id (str): ID de identifiación del usuario 
    
    <b>Ejemplo:</b>
    
    user_id: 76561197970982479
    
    '''
    # Calcula la suma de la columna precio filtrando por el usuario.
    money = round(df_f1[df_f1['user_id'] == user_id]['price'].sum(),2)
    
    # Calcula la cantidad de reviews para el usuario. 
    tot_recommend = df_f1_2[df_f1_2['user_id'] == user_id]['recommend'].sum()
    
    # Calcula la cantidad de reviews filtrando por el usuario en el DataFrame df_reviews_full.
    tot_items = df_f1_3[df_f1_3['user_id'] == user_id]['items_count'].iloc[0].item()

    return {'Usuario:': user_id,
            'Cantidad de dinero gastado:': round(money,2),
            # Hacemos el cociente para calcular el porcentaje.
            'Porcentaje de recomendación:': round((tot_recommend / tot_items) * 100, 2),
            'Cantidad de items:': tot_items
            }


# FUNCION 2
@app.get("/countreviews/{inicio}/{fin}", name = "COUNTREVIEWS")
def countreviews(inicio, fin):
    '''
    <b>Objetivo:</b>
    
    Devuelve la cantidad de usuarios que realizaron reviews entre 
    las fechas dadas y el porcentaje de recomendacion de esos usuarios.
    
    <b>Argumentos:</b>
    
    inicio (str): Fecha de inicio del periodo a evaluar.
    
    fin (str): Fecha de fin del periodo a evaluar
    
    <b>Ejemplo:</b>
    
    inicio: 2010-12-30
    
    fin: 2013-06-25
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
@app.get("/genre/{genero}", name = "GENRE")
def genre(genero):

    '''
    <b>Objetivo:</b>
    
    Devuelve en que puesto se encuentra el género 
    en el ranking "Mayor cantidad de horas jugadas en la plataforma".

    <b>Argumento:</b>
    
    genre (str): El género de juegos del cual se quiere conocer el ranking de horas jugadas. 
    
    <b>Ejemplo:</b>
    
    genero: Action

    '''
    # Filtramos el ranking según el género
    posicion = df_ranking[df_ranking['genres'] == genero]['Posicion'].iloc[0].item()
    
    return {'El género': genero, 
            'se encuentra en la posición':posicion
    }

    
# FUNCION 4
@app.get("/userforgenre/{genre}", name = "USERFORGENRE")
def userforgenre(genre):
    '''
    
    <b>Objetivo:</b>
    
    Devuelve el TOP 5 de usuarios con más horas jugadas en un género específico.

    <b>Argumento:</b>
    
    genre (str): El género de juegos para el que se desea obtener el TOP 5 de usuarios.
    
    <b>Ejemplo:</b>
    
    genero: Adventure
    
    '''

    # Filtrar el DataFrame para obtener datos específicos del género
    data = df_user_genre[df_user_genre['genres'] == genre]

    # Tomar los primeros 5 registros del DataFrame
    top5 = data[['user_id', 'user_url', 'playtime_forever']].head(5).reset_index(drop=True)

    return  {'El TOP 5 de usuarios para el género' : genre, 
             'es el siguiente' : top5}
    

# FUNCION 5
@app.get("/developer/{desarrollador}", name = "DEVELOPER")
def developer(desarrollador):

    '''
    
    <b>Objetivo:</b>
    
    Devuelve cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.

    <b>Argumento:</b>
    
    desarrolador (str): El developer del juego (item) para el cual se desea obtener los valores mencionados. 
    
    <b>Ejemplo:</b>
    
    Desarrolador: Valve

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
@app.get("/sentimet_analysis/{anio}", name = "SENTIMENT_ANALYSIS")
def sentiment_analysis(anio):
    ''' 
    <b>Objetivo:</b>
    
    Devuelve un DataFrame con la cantidad de registros de reseñas de usuarios categorizados por análisis de sentimiento para un año específico.
    
    <b>Argumentos:</b>
    
    anio (int): Año en el cual queremos obtener el análisis de sentimiento.
    
    <b>Ejemplo:</b>
    
    anio: 2012
   
    '''
    anio = int(anio)
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


# FUNCION 7
@app.get("/recomendacion_juego/{id}", name = "RECOMENDACIÓN JUEGO")
def recomendacion_juego(id):
    """
    <b>Objetivo:</b>
    
    Devuelve una lista de 5 juegos similares al pasado como argumento, basandose en el género del mismo.
    
    <b>Argumentos:</b>
    
    id (int): ID de identificación del juego.
    
    <b>Ejemplo:</b>
    
    id: 449940 
    
    """
    id = int(id)
    
    df_modelo_final = cargar_datos_modelo()
    
    # Filtrar el juego de entrada por su ID
    juego_seleccionado = df_modelo_final[df_modelo_final['id'] == id]

    # Calcular la matriz de similitud coseno
    similitudes = cosine_similarity(df_modelo_final.iloc[:,3:])
    
    # Obtener las puntuaciones de similitud del juego de entrada con otros juegos
    similarity_scores = similitudes[df_modelo_final[df_modelo_final['id'] == id].index[0]]
    
    # Obtener los índices de los juegos más similares (excluyendo el juego de entrada)
    indices_juegos_similares = similarity_scores.argsort()[::-1][1:6]
    
    # Obtener los nombres de los juegos recomendados
    juegos_recomendados = df_modelo_final.iloc[indices_juegos_similares]['app_name']
    
    cerrar_datos(df_modelo_final)
    
    return juegos_recomendados