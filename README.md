En este proyecto, desarrollo el rol de un Data Scientist de Steam, una plataforma distribuidora de video juegos.

---

![Logo_steam][(https://github.com/Tagliaferro22/steam-games/blob/main/img/logo_steam.jpg)]

https://github.com/Tagliaferro22/steam-games/blob/main/img/logo_steam.jpg

---

Empecé desde 0 y terminé creando un MVP (Minimun Viable Product), me encontré con varios problemas, cómo por ejemplo, la lectura
de los archivos, que estaban comprimidos en un formato que desconocía (.gzip); era un dataset almacenado en formato JSON y tuve
que aplicar varios procesos de ETL para poder desanidar algunas de las columnas que traían originalmente, que en su interior
contenían varias anidadas.

[Imagen de tirar del ovillo]

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

Para la primera función la consigna era la siguiente:
[Imagen de consigna endpoint 1]
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

---

Para el sistema de recomendación, la consigna era la siguiente:
[Imagen de consigna de sist recomendación]
Lo que decidí hacer fué usar una columna que había agregado en el dataset de juegos, llamada "categorical", en ella se alojaban todos los datos pertinentes al juego "tags", "genres" y "specs", usando scikit-learn, vectoricé esa columna y a partir de esa vectorización, utilicé el algoritmo de similitud del coseno. El cuál de lo que se encarga (de forma simple y muy resumida) es de encontrar palabras similares a las del juego ingresado. Por ejemplo, ingresamos el id de cierto juego que sabemos que es de acción, lo que hace ese algoritmo (nuevamente recalco, de forma simple y muy resumida) es buscar otros juegos que también sean de acción y de tematicas similares. Para nosotros quizás resulte simple saber que por ejemplo el Counter Strike es similar al Call of Duty (dos juegos de disparos), pero para un algoritmo que sólo entiende números no, es por eso que el proceso de ETL previamente realizado era de suma importancia para crear esa columna artificial llamada "categorical" y buscar los juegos a partir de allí.

---

Cómo conclusión y cierre, se podría terminar de hacer las otras funciones para que el trabajo quede completamente realizado, y terminar de especificar los detalles que requieren ciertas columnas, cómo por ejemplo, el tiempo de juego de un usuario, que no se sabe si está medido en horas, minutos o segundos, y es un dato bastante relevante.
Saludos y muchas gracias.

