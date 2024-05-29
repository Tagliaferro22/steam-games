En este proyecto, desarrollo el rol de un Data Scientist de Steam, una plataforma distribuidora de video juegos.

---

[Imagen de Data Science]
[Imagen del logo de steam]

---

Empecé desde 0 y terminé creando un MVP (Minimun Viable Product), me encontré con varios problemas, cómo por ejemplo, la lectura
de los archivos, que estaban comprimidos en un formato que desconocía (.gzip), era un dataset almacenado en formato JSON y tuve
que aplicar varios procesos de ETL para poder desanidar algunas de las columnas que traían originalmente, que en su interior
contenían varias columnas anidadas.

[Imagen de tirar del ovillo]

---

Trabajé principalmente con un dataset, el cuál se llama "steam_games", en él se encuentran varios datos acerca de los juegos, 
cómo por ejemplo su nombre, desarrollador, fecha de lanzamiento, id, precio entre otras cosas. 
Los datasets tal cuál me los dieron, están en la carpeta rawData dentro de la carpeta ETL (ETL/rawData), en ella, desarrollé todo el proceso de ETL que consideré necesario para cada uno de los archivos individualmente. Luego de este proceso, exporté
los datasets resultantes en formato .parquet con compresión snappy a la carpeta EDA, para justamente hacer lo que el nombre
de la carpeta indica. En ella, realicé un análisis exploratorio de los datasets, y terminé de hacer ciertas transformaciones
que consideré necesarias para la función de la API que desarrollé y el sistema de recomendación implementando modelos de 
Machine Learning.

