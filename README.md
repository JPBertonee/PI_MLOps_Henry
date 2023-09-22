<h1 align=center>  🚀 PROYECTO INDIVIDUAL 1 🚀 </h1>
<h1 align=center> Machine Learning Operations (MLOps) </h1>

# **Introducción** 

El objetivo de este proyecto es desarrollar un Producto Mínimo Viable (MVP) que incluya una API desplegada en un servicio en la nube y la implementación de un modelo de Machine Learning. 

En primer lugar, se proporcionan datos que serán fundamentales para este proyecto. Estos datos incluyen información sobre los comentarios de los usuarios de los juegos, detalles sobre los juegos disponibles en la plataforma Steam y informacion respecto a los usuarios de la plataforma. 

La primera funcionalidad importante del MVP es el desarrollo y la aplicación de 6 funciones que retornen información relevante sobre los datos pasados como parametros y asi tener respuesta a las preguntas de negocio. 

Una de estas funciones, a modo de ejemplo, es el desarrollo de un modelo de análisis de sentimientos aplicado a los comentarios de los usuarios de juegos. Este modelo permitirá evaluar de manera automática si los comentarios son positivos, negativos o neutros. Esto proporcionará información valiosa sobre la satisfacción de los usuarios con los juegos y permitirá a Steam tomar decisiones informadas sobre mejoras y actualizaciones. El resto de las funciones serán explicadas en el desarrollo del proyecto. 

La segunda funcionalidad es un sistema de recomendación de juegos. Este sistema se basa en ofrecer recomendaciones de juegos a partir de la simiulud que tienen con respecto a el/los géneros. 

En resumen, este proyecto representa un esfuerzo integral para mejorar la experiencia de los usuarios en Steam al aprovechar el poder de la ciencia de datos y el Machine Learning.

# **Contexto**

Steam es una plataforma de distribución digital y comunidad de jugadores líder en la industria de los videojuegos. Desarrollada por Valve Corporation, Steam ofrece a los usuarios una amplia gama de juegos para PC y otras plataformas. También es conocida por su sólida infraestructura de actualización y gestión de juegos, así como por su plataforma de desarrollo de juegos Steamworks, que brinda a los desarrolladores herramientas para crear y publicar juegos en la plataforma. Steam ha sido un pionero en la distribución digital de videojuegos y ha desempeñado un papel fundamental en la evolución de la industria de los videojuegos en línea.

# **Datasets**

El desarrollo del proyecto esta basado en tres datasets de la plataforma Steam:

1. ***steam_games:*** información relacionada a los juegos dentro de la plataforma Steam. Por ejemplo: Nombre del juego, género, fecha de lanzamiento, entre otras. 

2. ***user_reviews:*** información que detalla las reviews realizadas por los usuarios de la plataforma Steam.

3. ***user_items:*** información acerca de la actividad de los usuarios dentro de la plataforma Steam.

Para entender el detalle de cada uno de los datasets, siga el siguiente enlace: [DataSets](Diccionario_de_datos.xlsx)

# **Desarrollo**

Para seguir en detalle el desarrollo del proyecto, siga el siguiente enlace: [Desarrollo](Desarrollo.ipynb)

A continuación se explicará, de forma breve, el paso a paso del desarrollo del proyecto.

### 1. Ingesta de datos:
En este paso se cargan los datasets mencionados anteriormente con el objetivo de poder trabajarlos. 
### 2. Tratamiento de datos - ETL
Una vez cargados los datos, es común que necesiten ser limpiados y transformados para que sean útiles en el análisis. Este proceso implica la transformación de los datos para que sean coherentes y que el resultado del análisis cumpla con el obejetivo. 
### 3. Feature Engineering
Como se menciono en la introducción, una parte del proyecto incluye el desarrollo de un modelo de análisis de sentimientos aplicado a los comentarios de los usuarios de juegos. Este modelo se desarrolla sobre el dataset **user_reviews**. Para este analisis se utilizó la libreria TextBlob. Esta librería permite mediante una de sus funciones, reconocer por procesamiento de lenguaje natural si un comentario tiene una intención positiva, negativa o neutra. 
### 4. Funciones y disponibiliación de datos
Otra parte importante del proyecto es la creación de las funciones. A continuacion detallamos cada una de ellas:

+ **`userdata(User_id: str)`:** Esta función toma como entrada el ID de un usuario y devuelve la cantidad de dinero gastado por ese usuario, el porcentaje de recomendación basado en las revisiones (reviews.recommend) y la cantidad de items relacionados con ese usuario.

+ **`countreviews(YYYY-MM-DD y YYYY-MM-DD: str)`:** Esta función toma dos fechas en formato YYYY-MM-DD como entrada y devuelve la cantidad de usuarios que realizaron reviews entre esas dos fechas, así como el porcentaje de recomendación basado en las reviews realizadas durante ese período.

+ **`genre(género: str)`:** Esta función toma un género como entrada y devuelve la posición en la que se encuentra ese género en un ranking analizado bajo la columna PlayTimeForever.

+ **`userforgenre(género: str)`:** Esta función toma un género como entrada y devuelve los cinco usuarios con más horas de juego en ese género, junto con sus URL de usuario (del juego) y sus IDs de usuario.

+ **`developer(desarrollador: str)`:** Esta función toma como entrada el nombre de una empresa desarrolladora y devuelve la cantidad de items (juegos o contenido) producidos por esa empresa por año, así como el porcentaje de contenido gratuito en esos items.

+ **`sentiment_analysis(año: int)`:** Esta función toma un año como entrada y devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento para ese año en particular.

Estas funciones deben poder consumirse de forma local y desde un servidor web. Para ello utilizamos el framework ***FastAPI*** y el servidor web ***Render***

El desarrollo de las funciones y la utilización del framework puede verlo en el siguiente archivo: [Desarrollo API](main.py)
### 5. Análisis exploratorio de datos - EDA
En este paso se realiza el análisis exploratorio de los datos presentes en el archivo que sirve como base para la creación del modelo de recomendación que es el paso próximo para la finalizacón del proyecto. 

Antes de construir un modelo de machine learning, es esencial comprender los datos a través del análisis exploratorio. Esto incluye la visualización de datos, la identificación de patrones, la detección de valores atípicos y la comprensión de las relaciones entre las variables.

### 6. Modelamiento (Machine Learning Model Development)
En este paso, desarrollamos el modelo de machine learning utilizando los datos preparados anteriormente. Como base para el mismo se utiliza el dataset **steam_games**. Incluye la creación de una función, el modelo propieamente dicho y la adaptación de los datos que alimentaran a la función para que retornen el valor esperado. 

En este caso la funcion a crear es la siguiente: 

+ **`def recomendacion_juego( id de producto )`:** Esta función toma el id de un juego como entrada y devuelve una lista con 5 juegos recomendados similares al ingresado considerando para dicha similitud, los generos del juego. 

Es importante mencionar que dicha función tambien se encuentra en FastAPI y deployada en Render junto a las funciones mencionadas en el punto 4. 

# **Deployment**
Para poder consumir la API de en la web, utilizamos el servicio web proporcionado por la plataforma **Render**.

Render construye y despliega automáticamente el servicioweb y de esta manera puede consumirse por cualquier usuario desde un navegador y utilizando internet. Para implementar un servicio web en Render, conectamos el repositorio de GitHub (precisamente este) donde se encuentra el archivo *main.py** que contiene el desarrollo de la API en el framework FastAPI. 

En el siguiente link se encuentra alojado el servicio web: [Deploy en Render](https://apis-d6pt.onrender.com)


# **Conslusiones**
Mediante el desarrollo de este proyecto se logró poner en practica lo aprendido durante el cursado de la carrera de Data Science en la academia Henry. Precisamente, hemos desarrollado algunas de las tareas llevadas a cabo por un Data Engineer y un Data Scientist. 

Dado que es un proyecto con intenciones academicas, algunos de los resultados obtenidos no son precisamente los esperados ya que para cumplir con los requisitos se recurrió a la reduccion de los datasets (por motivos de memoria al querer realizar el deplyment en el servicio web). 

Este proyecto ha sido un viaje de aprendizaje y desafío, enfrentando las realidades del mundo real. A lo largo del proyecto, se han enfrentado desafíos significativos relacionados con la calidad y madurez de los datos, la falta de procesos automatizados y la necesidad de desarrollar un MVP de manera rápida. A pesar de estos obstáculos, hemos aprendido la importancia de la limpieza y estructuración de datos, la elección adecuada de algoritmos de recomendación y la necesidad de equilibrar la velocidad con la calidad en la implementación de un MVP.

A pesar de los logros, reconocemos que el sistema de recomendación todavía tiene margen de mejora. La automatización de procesos, la incorporación de más fuentes de datos y la implementación de algoritmos de machine learning más avanzados son pasos futuros para perfeccionar el sistema.





