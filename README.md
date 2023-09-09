# Proyecto Individual 1
Machine Learning Operations (MLOps)

## **Propuesta de trabajo**

**`Transformaciones`**:  Para este MVP no se te pide transformaciones de datos(` aunque encuentres una motivo para hacerlo `) pero trabajaremos en leer el dataset con el formato correcto. Puedes eliminar las columnas que no necesitan para responder las consultas o preparar los modelos de aprendizaje automático, y de esa manera optimizar el rendimiento de la API y el entrenamiento del modelo.

**`Feature Engineering`**:  En el dataset *user_reviews* se incluyen reseñas de juegos hechos por distintos usuarios. Debes crear la columna ***'sentiment_analysis'*** aplicando análisis de sentimiento con NLP con la siguiente escala: debe tomar el valor '0' si es malo, '1' si es neutral y '2' si es positivo. Esta nueva columna debe reemplazar la de user_reviews.review para facilitar el trabajo de los modelos de machine learning y el análisis de datos. De no ser posible este análisis por estar ausente la reseña escrita, debe tomar el valor de `1`.

**`Desarrollo API`**:   Propones disponibilizar los datos de la empresa usando el framework ***FastAPI***. Las consultas que propones son las siguientes:

<sub> Debes crear las siguientes funciones para los endpoints que se consumirán en la API, recuerden que deben tener un decorador por cada una (@app.get(‘/’)).<sub/>


+ def **userdata( *`User_id` : str* )**:
    Debe devolver `cantidad` de dinero gastado por el usuario, el `porcentaje` de recomendación en base a reviews.recommend y `cantidad de items`.

+ def **countreviews( *`YYYY-MM-DD` y `YYYY-MM-DD` : str* )**:
    `Cantidad de usuarios` que realizaron reviews entre las fechas dadas y, el `porcentaje` de recomendación de los mismos en base a reviews.recommend.

+ def **genre( *`género` : str* )**:
    Devuelve el `puesto` en el que se encuentra un género sobre el ranking de los mismos analizado bajo la columna PlayTimeForever. 

+ def **userforgenre( *`género` : str* )**:
    `Top 5` de usuarios con más horas de juego en el género dado, con su URL (del user) y user_id.

+ def **developer( *`desarrollador` : str* )**:
    `Cantidad` de items y `porcentaje` de contenido Free por año según empresa desarrolladora. 
Ejemplo de salida:
    | Activision ||
    |----------|----------|
    | Año  | Contenido Free  |
    | 2023   | 27% |
    | 2022    | 25%   |
    | xxxx    | xx%   |


+ def **sentiment_analysis( *`año` : int* )**:
    Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento. 

    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ejemplo de retorno: *{Negative = 182, Neutral = 120, Positive = 278}*



<br/>


> `Importante`<br>
El MVP _tiene_ que ser una API que pueda ser consumida segun los criterios de [API REST o RESTful](https://rockcontent.com/es/blog/api-rest/). Algunas herramientas como por ejemplo, Streamlit, si bien pueden brindar una interfaz de consulta, no cumplen con las condiciones para ser consideradas una API, sin workarounds.


**`Deployment`**: Conoces sobre [Render](https://render.com/docs/free#free-web-services) y tienes un [tutorial de Render](https://github.com/HX-FNegrete/render-fastapi-tutorial) que te hace la vida mas fácil :smile: . También podrías usar [Railway](https://railway.app/), o cualquier otro servicio que permita que la API pueda ser consumida desde la web.

<br/>

**`Análisis exploratorio de los datos`**: _(Exploratory Data Analysis-EDA)_

Ya los datos están limpios, ahora es tiempo de investigar las relaciones que hay entre las variables del dataset, ver si hay outliers o anomalías (que no tienen que ser errores necesariamente :eyes: ), y ver si hay algún patrón interesante que valga la pena explorar en un análisis posterior. Las nubes de palabras dan una buena idea de cuáles palabras son más frecuentes en los títulos, ¡podría ayudar al sistema de predicción! En esta ocasión vamos a pedirte que no uses librerías para hacer EDA automático ya que queremos que pongas en práctica los conceptos y tareas involucrados en el mismo. Puedes leer un poco más sobre EDA en [este articulo](https://medium.com/swlh/introduction-to-exploratory-data-analysis-eda-d83424e47151)

**`Modelo de aprendizaje automático`**: 

Una vez que toda la data es consumible por la API, está lista para consumir por los departamentos de Analytics y Machine Learning, y nuestro EDA nos permite entender bien los datos a los que tenemos acceso, es hora de entrenar nuestro modelo de machine learning para armar un **sistema de recomendación**. Para ello, te ofrecen dos propuestas de trabajo: En la primera, el modelo deberá tener una relación ítem-ítem, esto es se toma un item, en base a que tan similar esa ese ítem al resto, se recomiendan similares. Aquí el input es un juego y el output es una lista de juegos recomendados, para ello recomendamos aplicar la *similitud del coseno*. 
La otra propuesta para el sistema de recomendación debe aplicar el filtro user-item, esto es tomar un usuario, se encuentran usuarios similares y se recomiendan ítems que a esos usuarios similares les gustaron. En este caso el input es un usuario y el output es una lista de juegos que se le recomienda a ese usuario, en general se explican como “A usuarios que son similares a tí también les gustó…”. 
Deben crear al menos **uno** de los dos sistemas de recomendación (Si se atreven a tomar el desafío, para mostrar su capacidad al equipo, ¡pueden hacer ambos!). Tu líder pide que el modelo derive obligatoriamente en un GET/POST en la API símil al siguiente formato:

Si es un sistema de recomendación item-item:
+ def **recomendacion_juego( *`id de producto`* )**:
    Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

Si es un sistema de recomendación user-item:
+ def **recomendacion_usuario( *`id de usuario`* )**:
    Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario.