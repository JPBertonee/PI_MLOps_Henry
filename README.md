# PROYECTO INDIVIDUAL 1  
## ***Machine Learning Operations (MLOps)***

## **Introducción** 

El objetivo de este proyecto es desarrollar un Producto Mínimo Viable (MVP) que incluya una API desplegada en un servicio en la nube y la implementación de un de Machine Learning. 

En primer lugar, se proporcionan datos que serán fundamentales para este proyecto. Estos datos incluyen información sobre los comentarios de los usuarios de los juegos, detalles sobre los juegos disponibles en la plataforma Steam y informacion respecto a los usuarios de la plataforma. 

La primera funcionalidad importante del MVP es el desarrollo y la aplicación de 6 funciones que retornen información relevante sobre los datos pasados como parametros y asi tener respuesta a las preguntas de negocio. 

Una de estas funciones, a modo de ejemplo, es el desarrollo de un modelo de análisis de sentimientos aplicado a los comentarios de los usuarios de juegos. Este modelo permitirá evaluar de manera automática si los comentarios son positivos, negativos o neutros. Esto proporcionará información valiosa sobre la satisfacción de los usuarios con los juegos y permitirá a Steam tomar decisiones informadas sobre mejoras y actualizaciones. El resto de las funciones serán explicadas en el desarrollo del proyecto. 

La segunda funcionalidad es un sistema de recomendación de juegos. Este sistema se basa en ofrecer recomendaciones de juegos a partir de la simiulud que tienen con respecto a el/los géneros. 

En resumen, este proyecto representa un esfuerzo integral para mejorar la experiencia de los usuarios en Steam al aprovechar el poder de la ciencia de datos y el Machine Learning.

## **Contexto**

Steam es una plataforma de distribución digital y comunidad de jugadores líder en la industria de los videojuegos. Desarrollada por Valve Corporation, Steam ofrece a los usuarios una amplia gama de juegos para PC y otras plataformas. También es conocida por su sólida infraestructura de actualización y gestión de juegos, así como por su plataforma de desarrollo de juegos Steamworks, que brinda a los desarrolladores herramientas para crear y publicar juegos en la plataforma. Steam ha sido un pionero en la distribución digital de videojuegos y ha desempeñado un papel fundamental en la evolución de la industria de los videojuegos en línea.

## **Datasets**

El desarrollo del proyecto esta basado en tres datasets de la plataforma Steam:

1. ***steam_games:*** información relacionada a los juegos dentro de la plataforma Steam. Por ejemplo: Nombre del juego, género, fecha de lanzamiento, entre otras. 

2. ***user_reviews:*** información que detalla las reviews realizadas por los usuarios de la plataforma Steam.

3. ***user_items:*** información acerca de la actividad de los usuarios dentro de la plataforma Steam.

Para entender el detalle de cada uno de los datasets, siga el siguiente enlace: [Detalles DataSets](Diccionario_de_datos.xlsx)

## **Desarrollo**

Para seguir en detalle el desarrollo del proyecto, siga el siguiente enlace: [Desarrollo](Desarrollo.ipynb)

A continuación se explicará, de forma breve, el paso a paso del desarrollo del proyecto.

### 1. Ingesta de datos:
En este paso se cargan los datasets mencionados anteriormente con el objetivo de poder trabajarlos. 
### 2. Tratamiento de datos - ETL
Una vez cargados los datos, es común que necesiten ser limpiados y transformados para que sean útiles en el análisis. Este proceso implica la transformación de los datos para que sean coherentes y que el resultado del análisis cumpla con el obejetivo. 
### 3. Feature Engineering
Como se menciono en la introducción, una parte del proyecto incluye el desarrollo de un modelo de análisis de sentimientos aplicado a los comentarios de los usuarios de juegos. Este modelo se desarrolla sobre el dataset **user_reviews** 
### 4. Funciones y disponibiliación de datos
Otra parte importante del proyecto es la creación de las funciones. A continuacion detallamos cada una de ellas:

+ **`userdata(User_id: str)`:** Esta función toma como entrada el ID de un usuario y devuelve la cantidad de dinero gastado por ese usuario, el porcentaje de recomendación basado en las revisiones (reviews.recommend) y la cantidad de items relacionados con ese usuario.

+ **`countreviews(YYYY-MM-DD y YYYY-MM-DD: str)`:** Esta función toma dos fechas en formato YYYY-MM-DD como entrada y devuelve la cantidad de usuarios que realizaron reviews entre esas dos fechas, así como el porcentaje de recomendación basado en las reviews realizadas durante ese período.

+ **`genre(género: str)`:** Esta función toma un género como entrada y devuelve la posición en la que se encuentra ese género en un ranking analizado bajo la columna PlayTimeForever.

+ **`userforgenre(género: str)`:** Esta función toma un género como entrada y devuelve los cinco usuarios con más horas de juego en ese género, junto con sus URL de usuario (del juego) y sus IDs de usuario.

+ **`developer(desarrollador: str)`:** Esta función toma como entrada el nombre de una empresa desarrolladora y devuelve la cantidad de items (juegos o contenido) producidos por esa empresa por año, así como el porcentaje de contenido gratuito en esos items.

+ **`sentiment_analysis(año: int)`:** Esta función toma un año como entrada y devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento para ese año en particular.

Estas funciones deben poder consumirse de forma local y desde un servidor web. Para ello utilizamos el framework ***FastAPI*** y el servidor web ***Render***
### 5. Análisis exploratorio de datos - EDA
En este paso se realiza el análisis exploratorio de los datos presentes en el archivo que sirve como base para la creación del modelo de recomendación que es el paso próximo para la finalizacón del proyecto. 

Antes de construir un modelo de machine learning, es esencial comprender los datos a través del análisis exploratorio. Esto incluye la visualización de datos, la identificación de patrones, la detección de valores atípicos y la comprensión de las relaciones entre las variables.

### 6. Modelamiento (Machine Learning Model Development)
En este paso, desarrollamos el modelo de machine learning utilizando los datos preparados anteriormente. Como base para el mismo se utiliza el dataset **steam_games**. Incluye la creación de una función, el modelo propieamente dicho y la adaptación de los datos que alimentaran a la función para que retornen el valor esperado. 

En este caso la funcion a crear es la siguiente: 

+ **`def recomendacion_juego( id de producto )`:** Esta función toma el id de un juego como entrada y devuelve una lista con 5 juegos recomendados similares al ingresado considerando para dicha similitud, los generos del juego. 

## **Conslusiones**

