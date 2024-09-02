![Banner](img/banner.png)
-
<center> Bienvenidos sean a este proyecto, en el cuál desarrollo el rol de un Científico de datos trabajando para Steam, una plataforma distribuidora de videojuegos.</center>

---
![data_science](img/data_science.jpg)


![steam](img/logo_steam.jpg)

---

# <center> Introducción / descripción del proyecto </center>

Para este proyecto educativo me pidieron que desarrolle un _MVP (Minimun Viable Product / Producto Mínimo Viable)_ para la plataforma distribuidora de videojuegos **Steam**. 

Trabajando cómo científico e ingeniero de datos dentro de Steam, soy el encargado de crear un sistema de recomendación de videojuegos para usuarios. El cuál explico con más detalle [mas adelante.](#-sistemas-de-recomendacion)

Para este proyecto, utilicé una serie de tecnologías, las cuales se listan a continuación:
- Python: Para el despliegue de la API mediante FastAPI y Render
- Jupyter Notebook: Para la creación y desarrollo tanto de los sistemas de recomendación cómo de los endpoints que se me pedían para este proyecto.
- Visual Studio Code: Para escribir el código
- Pandas: Para leer los conjuntos de datos los cuáles explico con más detalle [a continuación.](#-conjuntos-de-datos)
- Numpy: Para complementar a la librería pandas.
- Scikit-learn
- Uvicorn
- FastAPI
- Ast
- Matplotlib
- Render

## <center> Conjuntos de datos </center>

Tengo 3 conjuntos de datos que corresponden a lo que es la base de datos de Steam.

- User_items: En esta tabla, tenemos disponibles todos los datos de los juegos adquiridos por determinados usuarios.
Echando un vistazo a la tabla original nos encontramos con las siguientes columnas:
  - user_id: Identificador único de cada usuario
  - items_count: Cantidad de juegos que tiene el usuario
  - steam_id: El identificador único dentro de steam
  - user_url: El enlace para acceder a la página web dentro de Steam correspondiente al usuario 
  - items: Los juegos del usuario, una columna anidada, de la cuál hablo con más detalle en la parte del [ETL.](#etl)

La cabecera de la tabla originalmente se veía así:
![Cabecera de la tabla user_items](img/user_items_cabecera.png)

- User_reviews: En esta tabla, tenemos disponibles todas las reseñas hechas por los usuarios a los distitintos juegos que adquirieron. Echando un vistazo a la tabla original, nos encontramos con las siguientes columnas:

  - user_id: El identificador único de cada usuario
  - user_url: El enlace correspondiente a cada usuario.
  - reviews: Las reseñas hechas por el usuario, nuevamente, una columna con datos anidados, que explico con más detalle en la parte del [ETL.](#etl)

Un fragmento de la tabla originalmente se veía así:
![Tabla de user_reviews](img/user_reviews_tabla_original.png)

- Steam_games: En esta tabla, tenenemos disponbibles todos los datos correspondientes a los juegos disponibles dentro de Steam, echando un vistazo a sus columnas originales, nos encontramos con:
  - publisher: El publicador / lanzador del juego.
  - genres: Los géneros del juego.
  - app_name: El nombre de la aplicación / juego.
  -	title: El titulo del juego, similar a app_name
  -	url: El enlace dónde se puede encontrar el juego dentro de Steam
  -	release_date: La fecha de salida del juego
  -	tags: Las etiquetas / categorías del juego, similar a genres.
  -	reviews_url: La página web dentro de Steam dónde están disponibles las reseñas hechas al juego.
  -	specs: Las especificaciones del juego, similar a tags y a genres.
  -	price: El precio del juego
  -	early_access: Si hubo o no acceso temprano al juego
  -	id: El identificador único de cada videojuego dentro de Steam
  -	developer: El desarrollador del vídeojuego, similar al publisher. 

La cabecera de la tabla originalmente se veía así:
![Cabecera de la tabla steam_games](img/steam_games_cabecera.png)


Con todas estas tablas, sus columnas y sus datos asociados, empecé desde 0 y creé un MVP (Minimun Viable Product) con varias funcionalidades. Pero primero, veamos que objetivos cumplí en este proyecto.

### <center> Objetivos y alcances del proyecto </center>


✅ Transformaciones: para el desarrollo de los [endpoints](#endpoints) y de los [sistemas de recomendación](#sistemas-de-recomendacion), me encontré con varios inconvenientes, los cuáles explico con más detalle en la parte del [ETL](#etl).

✅ Análisis exploratorio de datos (EDA): Luego de haber podido leer los datos, me encargué de realizar un análisis exploratorio de los datos, el cuál explico con más detalle enla parte del [EDA](#eda).

✅ Análisis de sentimientos: A partir de las reseñas hechas por los usuarios hacia determinados juegos, determiné si se trataba de una reseña negativa, neutra o positiva.

✅ Desarrollo óptimo y funcional de una API mediante el framework de FastAPI y su respectivo despliegue en Render. 

✅ Desarrollo e implementación de ciertos [endpoints / funciones](#endpoints) para utilizar dentro de la API.

✅ Desarrollo e implementación de modelos de Machine Learning orientados a dos [sistemas de recomendación de videojuegos.](#sistemas-de-recomendacion)

✅ Todo lo anterior fué logrado mediante muchas horas de dedicación y el desarrollo de un código limpio, prolijo y escalable.

---

### <center> ETL </center>

Comencemos por el principio, respondiendo la siguiente pregunta ¿Que es ETL? ETL son siglas en inglés que corresponden a Extract, Transform and Load. En español sería ETC, Extracción, Transformación y Carga.

Pero en nuestro proyecto, ¿Extraer qué? Bueno, el primero de los inconvenientes con los que me encontré cuando comenzaba a desarrollar o más bien querer desarrollar el proyecto, fué el de tratar de leer los archivos correspondientes a los [conjuntos de datos](#conjuntos-de-datos) previamente mencionados.

Los archivos estaban comprimidos en un formato que desconocía (.gzip); era un dataset almacenado en formato JSON y con ayuda de un compañero, implementamos un código capaz de leerlos y almacenarlos dentro de un Dataframe de la librería pandas, con lo cuál se volvió mucho más manejable.

En la primera tabla (user_items) hago mención a que la columna "items" era una columna anidada. Y capaz te estés preguntando ¿Que es una columna anidada? Bueno, bajo mi punto de vista, una columna anidada es una columna que en su interior contiene varios datos de distintos tipos, ¿Alguna vez vieron un ovillo de lana? 

![data_science](img/ovillo.jpg)

Bueno, haciendo una análogia con un ovillo de lana, la columna items de la tabla user_items se veía justamente de la siguiente manera:

![analogía](img/tabla_user_items_analogia.png)

Explico con más detalle el procedimiento que seguí con esta tabla (user_items) y sus justificaciones en la carpeta ETL de este mismo proyecto, específicamente en el archivo [ETL_user_items.ipynb](ETL/ETL_user_items.ipynb). 

Los ovillos compartían la forma / estructura pero eran de distintos tamaños. 

Resumidamente, lo que hice fué lo siguiente:

En cada celda de esta columna, había una lista de diccionarios. Bueno bueno bueno, creo que me estoy poniendo muy nerd / geek...

![nerd](img/nerd.jpg)

Bueno, lo que quiero decir con esto, es que la columna se "veía" similar a la siguiente imagen. 

![Especificacion](img/columna_items_en_detalle_analogia.png)

Cómo vemos, los ovillos no eran exactamente ovillos (era una lista de diccionarios), sino que era un conjunto de datos que compartían la misma estructura. Siguiendo con la analogía, en cada celda, había una lista (que sería en este caso la cuerda superior que está atada) y dentro de esta misma estaban contenidas cuerdas. En todas las celdas había 4 cuerdas, lo que cambiaba era el largo de estas 4 cuerdas. Y si nos ponemos más especificos, el largo de estas 4 cuerdas estaba determinado por una columna llamada items_count.

A partir de esta situación, y en base a los requisitos del proyecto, en el proceso de transformación de esta tabla, decidí quedarme sólo con dos columnas: user_id e items. Originalmente la tabla tenía 88310 filas y 5 columnas. Luego de este cambio se quedó con 88310 filas y 2 columnas.

Si hacemos zoom a la primera celda por ejemplo, podríamos ver algo así:

![zoom](img/columna_items_zoom_celda.png)

Vemos que en la imagen anterior hay 4 columnas, que son las equivalentes a las 4 cuerdas con las que hacía la analogía. Las columnas son:

- item_id: El ID único de cada videojuego.
- item_name: El nombre del juego
- playtime_forever: la cantidad total de tiempo invertido por el usuario en ese juego.
- playtime_2weeks: La cantidad total de tiempo invertido por el usuario las últimas 2 semanas.

Además de esas 4 columnas, en la imagen se pueden ver 5 filas, pero en realidad, la cantidad de filas era exactamente el valor contenido en la columna previamente eliminada items_count, por ejemplo, para el primer usuario, había 277 filas, que equivalían a 277 juegos que posee ese primer usuario dentro de la tabla user_items.

Cómo esas 277 filas estaban contenidas en una única celda (y por eso anteriormente decía que la columna estaba anidada), lo que hice fué desanidar cada una de esas celdas, pudiendo ver así, sus respectivas filas incluidas. 

Hacer esto obviamente multiplicó el tamaño del conjunto de datos enormemente, ya sólo con el primer usuario, tenía 277 filas más, por que cada usuario puede tener más de un juego (y de hecho la mayoría tenía más de un juego). 

La estructura resultante de esta transformación se podía ver así:

![Tabla desanidada](img/tabla_user_items_desanidada.png)

Lo que hice fué conservar la columna user_id al final y repetirla por cada juego que tenga ese usuario, para saber a quién le corresponde cada juego.

Con esta hermosa transformación pasé de una tabla de 88310x5 a una tabla de 5153209x5... 

Algo similar hice en la tabla user_reviews. Originalmente esta tabla tenía 25799 filas x 3 columnas. 

La tabla originalmente se veía así:
![Tabla user_reviews original](img/user_reviews_tabla_original.png)

La columna user_url no la iba a utilizar, así que sólo conservé user_url y reviews. La cosa es que nuevamente tenía la misma situación: un usuario puede hacer más de una reseña, entonces la columna reviews estaba anidada. En su interior tenía 7 columnas (7 cuerdas si seguimos con la analogía), y la cantidad de filas dependía de la cantidad de reseñas que había hecho el usuario.

Finalmente, la tabla resultante de la transformación se ve así:

![Tabla user_reviews desanidada](img/user_reviews_desanidada.png)

Y colorín colorado, la explicación "sencilla" de las transformaciones se ha terminado. Ya que la tabla steam_games no requirió una importante transformación, sino que la única transformación que tuvo fué la de descompresión del archivo .gzip

---

Trabajé principalmente con un dataset, el cuál se llama "steam_games", en él se encuentran varios datos acerca de los juegos, 
cómo por ejemplo su nombre, desarrollador, fecha de lanzamiento, id, precio entre otras cosas. 
Los datasets tal cuál me los dieron, están en la carpeta rawData dentro de la carpeta ETL (ETL/rawData), en ella, desarrollé todo el proceso de ETL que consideré necesario para cada uno de los archivos individualmente. Luego de este proceso, exporté
los datasets resultantes en formato .parquet con compresión snappy a la carpeta EDA, para justamente hacer lo que el nombre
de la carpeta indica. En ella, realicé un análisis exploratorio de los datasets, y terminé de hacer ciertas transformaciones
que consideré necesarias para la función de la API que desarrollé y el sistema de recomendación implementando modelos de 
Machine Learning. Los mismos están contenidos en el archivo principal, llamado main.py.
Para darle "vida" a la API, usé un framework llamado FastAPI con el que pude desplegar mi API de forma local, luego subí las carpetas que usé a GitHub, y realicé un despliegue de manera "global" u "online" mediante Render para que cualquier persona con acceso a internet pueda usar la API que desarrollé. 

---

---

---

---

Cómo conclusión y cierre, se podría terminar de hacer las otras funciones para que el trabajo quede completamente realizado, y terminar de especificar los detalles que requieren ciertas columnas, cómo por ejemplo, el tiempo de juego de un usuario, que no se sabe si está medido en horas, minutos o segundos, y es un dato bastante relevante.
Saludos y muchas gracias.




### <center> EDA </center>

### <center> Endpoints </center>

- Primer endpoint: Para la función correspondiente al primer endpoint, la consigna era la siguiente:

![data_science](img/endpoint_1.png)

Entonces desarrolle una función que hace lo siguiente: Primero, evalúa si el desarrollador ingresado en la función existe en el dataset, si no existe, lanza el siguiente error: "Developer not found". Si el desarrollador si existe en el dataset, la función ingresa en un bucle que itera sobre cada año de manera única en los que el desarrollador sacó al menos un videojuego. 
Por ejemplo, si en 2015 sacó 3 juegos, en 2016 sacó 2 y en 2017 sacó 4, esos años aparecen 3, 2 y 4 veces respectivamente, por lo cuál, lo que hace el bucle es tomar esos años cómo valores únicos, apareciendo sólo una vez el 2015, el 2016 y el 2017.

Dentro del bucle, se crea una variable interna que cambia con cada iteración del mismo, la cuál almacena la cantidad de juegos que el desarrollador, esto lo hace (explicado de forma simple y resumida) aplicando un "filtro" para que busque la cantidad de veces que aparece ese desarrollador ingresado en la función y ese año que está definido por el bucle.
Luego, cuenta la cantidad de items gratuitos, esto lo hace nuevamente con otro "filtro" similar al anterior, sólo que agregandole el detalle que esta vez, el precio tiene que ser igual a 0.
Estos dos valores se almacenan en una variable llamada "pre_salida", que es un diccionario, el cuál tiene cómo pares clave valor lo siguiente: "{
            "Cantidad items": int(cant_items_anual), 
            "Contenido gratuito (%)": f"{(cant_items_gratuitos_anual / cant_items_anual) * 100}%"
        }". Luego la variable salida, osea, lo que finalmente muestra la función , lo que tiene de caracteristico es que tiene el año que se está iterando, por lo cuál, la salida quedaría de esta forma:
        {
          Año:{"Cantidad items": int(cant_items_anual), 
            "Contenido gratuito (%)": f"{(cant_items_gratuitos_anual / cant_items_anual) * 100}%"}
        }



### <center> Sistemas de recomendacion</center>

Primero aclaro que, la palabra recomendación no tiene acento en el título porque si lo ponía no me dejaba agregar la funcionalidad de que, al hacer click te redirija a esta parte del README. 

Habiendo dejado eso en claro, empecemos por lo básico, respondiendo a la siguiente pregunta, ¿Qué es un sistema de recomendación?
Según [Aprende machine learning . com](https://www.aprendemachinelearning.com/sistemas-de-recomendacion/)
"...son algoritmos que intentan 'predecir' los siguientes ítems (en nuestro proyecto, juegos) que querrá adquirir un usuario en particular."
Estamos rodeados de sistemas de recomendación, en Instagram por ejemplo, cuando comenzamos a ver reels, y hacemos "scroll" (deslizar para ver el siguiente contenido), el próximo vídeo que nos aparezca, es aquel que el algoritmo de Instagram nos ha recomendado.
En YouTube, cuando estamos viendo un video y nos aparece un "recomendado" o "para tí" es exactamente lo mismo. 

Para el sistema de recomendación, la consigna era la siguiente:

![data_science](img/modeloML.png)

Lo que decidí hacer fué usar una columna que había agregado en el dataset de juegos, llamada "categorical", en ella se alojaban todos los datos pertinentes al juego "tags", "genres" y "specs", usando scikit-learn, vectoricé esa columna y a partir de esa vectorización, utilicé el algoritmo de similitud del coseno. El cuál de lo que se encarga (de forma simple y muy resumida) es de encontrar palabras similares a las del juego ingresado. Por ejemplo, ingresamos el id de cierto juego que sabemos que es de acción, lo que hace ese algoritmo (nuevamente recalco, de forma simple y muy resumida) es buscar otros juegos que también sean de acción y de tematicas similares. Para nosotros quizás resulte simple saber que por ejemplo el Counter Strike es similar al Call of Duty (dos juegos de disparos), pero para un algoritmo que sólo entiende números no, es por eso que el proceso de ETL previamente realizado era de suma importancia para crear esa columna artificial llamada "categorical" y buscar los juegos a partir de allí.