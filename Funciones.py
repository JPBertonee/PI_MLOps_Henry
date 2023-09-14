'''
FUNCIONES
'''

# Leemos los dataframes que alimentaran a las distintas funciones
df_items_full = pd.read_parquet('df_itrms_full.parquet')
df_items_games = pd.read_parquet('df_items_games.parquet')
df_items_recommend = pd.read_parquet('df_items_recommend.parquet')
df_f2 = pd.read_parquet('df_f2.parquet')
df_ranking = pd.read_parquet('df_ranking.parquet')
df_user_genre= pd.read_parquet('df_user_genre.parquet')
df_f5 = pd.read_parquet('df_f5.parquet')
df_f6 = pd.read_parquet('df_f6.parquet')


# Función 1

def userdata(user_id):
    '''
    La siguiente función filtra por el usuario pasado como argumento
    y arroja el dinero gastado por dicho usuario, el porcentaje de recomendación 
    y la cantidad de items del mismo. 
    
    Argumento:
    user_id (str): ID de identifiación del usuario 
    
    '''
    # Verificamos si el usuario existe en el DataFrame
    if user_id in df_items_games['user_id'].values and user_id in df_items_recommend['user_id'].values and user_id in df_items_full['user_id'].values:
        # Calcula la suma de la columna precio filtrando por el usuario.
        money = df_items_games[df_items_games['user_id'] == user_id]['price'].sum()
        
        # Calcula la cantidad de reviews totales de todos los usuarios en el DataFrame df_reviews_full.
        tot_recommend = df_items_recommend[df_items_recommend['user_id'] == user_id]['recommend'].sum()
       
        # Calcula la cantidad de reviews filtrando por el usuario en el DataFrame df_reviews_full.
        tot_items = df_items_recommend[df_items_recommend['user_id'] == user_id]['items_count'].iloc[0]
        
        # Calcula la cantidad de items filtrando por el usuario en el DataFrame df_items_full.
        cant_items = df_items_full[df_items_full['user_id'] == user_id]['items_count'].iloc[0]

        return {'Usuario:': user_id,
                'Cantidad de dinero gastado:': money,
                # Hacemos el cociente para calcular el porcentaje.
                'Porcentaje de recomendación:': round((tot_recommend / tot_items) * 100, 2),
                'Cantidad de items:': cant_items
                }
    else:
        return 'Usuario no encontrado'
    
    
# Función 2
    
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
    
    reviews_reco = round(reviews_entre_fechas['recommend'].sum() / reviews_entre_fechas['recommend'].count() * 100,2)
    
    return {'Cantidad de usuarios:': cantidad_usuarios,
            # Hacemos el cociente para calcular el porcentaje.
        'Porcentaje de recomendación:': reviews_reco
    }
    
    
# Función 3

def genre(genero):

    '''
    Esta función nos aroja en que puesto del ranking 'Playtime_Forever' se encuentra 
    el género pasado como input.

    Argumento: 
    genre (str): El género de juegos del cual se quiere conocer el ranquin de horas jugadas. 

    '''

    #Filtramos el ranking según el genero y mostramos el valor de la columna posicion. 
    posicion = df_ranking[df_ranking['genres'] == genero]['Posicion'].iloc[0]

    return 'El género', genero, 'se encuentra en la posición', posicion
    
    
# Función 4
    
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

    # Crear un mensaje descriptivo
    mensaje = f'El TOP 5 de usuarios para el género "{genre}" es el siguiente'

    return mensaje, top5


# Función 5

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
    
    # Creamos un DataFrame con los resultados
    resultados = pd.DataFrame({
        'Año': items_free_por_anio.index,
        'Cantidad de Items': items_totales_por_anio.values,
        'Porcentaje Free': porcentaje_free.values
    })
    
    return resultados
    
    
# Función 6

def sentiment_analysis(anio):
    ''' 
    Devuelve un DataFrame con la cantidad de registros de reseñas de usuarios categorizados por análisis de sentimiento para un año específico.
    
    Argumentos:
    anio (int): Año en el cual queremos obtener el análisis de sentimiento.
    df_f6 (DataFrame): El DataFrame que contiene los datos de reseñas y sentimientos.
   
    '''

    # Filtramos el DataFrame según el año definido como argumento
    df_filtered = df_f6[df_f6['posted'].dt.year == anio]
    
    # Utilizamos value_counts() para contar los valores únicos en la columna 'sentimiento'
    sentiment_counts = df_filtered['sentimiento'].value_counts()

    # Obtenemos la cantidad de valores positivos, negativos y neutros
    positivos = sentiment_counts.get(2, 0)  # Valor 2 para positivos 
    neutros = sentiment_counts.get(1, 0)   # Valor 1 para neutros 
    negativos = sentiment_counts.get(0, 0) # Valor 0 para negativos 

    # Crear un DataFrame con los resultados
    resultado = pd.DataFrame({
        'Positivos': [positivos],
        'Neutros': [neutros],
        'Negativos': [negativos]
    })

    return resultado
    
    