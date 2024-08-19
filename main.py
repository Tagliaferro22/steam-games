from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging


# http://127.0.0.1:8000
app = FastAPI(
    title = 'Machine Learning Operations (MLOps)',
    description='API para realizar consultas',
    version='Mateo Tagliaferro (2024)'
)

@app.get("/")
def index():
    return {"Hello": "World"}



# Primer endpoint -------------------- 1
def developer(desarrollador: str):
    salida = {}
    Steam_games_important = pd.read_parquet("./Datasets/endpoint_1/Steam_games_endpoint_1.parquet")
    # Imprimir información relevante antes del bucle


    if desarrollador not in Steam_games_important["developer"].unique():
        raise HTTPException(status_code=404, detail="Developer not found")
    
    for año in Steam_games_important[Steam_games_important["developer"] == desarrollador]["release_year"].unique():
        # Agregar más impresiones dentro del bucle si es necesario
        

        cant_items_anual = Steam_games_important[(Steam_games_important["release_year"] == año) & (Steam_games_important["developer"] == desarrollador)]["developer"].count()
        cant_items_gratuitos_anual = Steam_games_important[(Steam_games_important["release_year"] == año) & (Steam_games_important["developer"] == desarrollador) & (Steam_games_important["price"] == 0)]["developer"].count()
        
        pre_salida = {
            "Cantidad items": int(cant_items_anual), 
            "Contenido gratuito (%)": f"{(cant_items_gratuitos_anual / cant_items_anual) * 100}%"
        }
        
        salida[int(año)] = pre_salida

    return salida

@app.get("/developer/{desarrollador}",response_model=dict)
async def developer_use(desarrollador_local : str = Query(default="ebi-hime")):
    try:
        resultado = developer(desarrollador_local)
        # Imprimir el resultado para depuración
        
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")

# Segundo endpoint -------------------- 2
# El endpoint está así en el main:
def informacion_usuario(user_id):
    try:
        user_id_str = str(user_id)
        # Cargamos los dataframes dentro de la función
        user_items = pd.read_parquet("./Datasets/endpoint_2/users_items.parquet")

        user_reviews = pd.read_parquet("./Datasets/endpoint_2/user_reviews_endpoint_2.parquet")

        usuario_juego_precio = pd.read_parquet("./Datasets/endpoint_2/usuarios_y_dinero_gastado.parquet")

        print("Archivos leídos correctamente")
        
        diccionario_de_retorno = {} # Diccionario que va a almacenar las variables correspondientes a la salida de la función

        if user_items[user_items["user_id"] == user_id_str].empty: # En caso de que no haya usuarios con el ID ingresado, se muestra lo siguiente:
            return {"Detail":"No se encontraron datos para el usuario con ID: " + user_id_str}
        else: # En caso de que haya usuarios con el ID ingresado, se muestra lo siguiente
            
            # Se cuenta la cantidad de juegos que tiene el usuario
            print("Condicional pasado correctamente")
            cantidad_juegos = user_items[user_items["user_id"] == user_id_str]["items_count"].iloc[0]

            print(f"Cantidad de juegos: {cantidad_juegos}, Tipo: {type(cantidad_juegos)}")

            # Se cuenta la cantidad de recomendaciones. En la columna recommend aparece "True" o "False", tuve en cuenta sólo las que aparece "True" del usuario ingresado.
            cantidad_de_recomendaciones = user_reviews[(user_reviews["user_id"] == user_id_str) & (user_reviews["recommend"] == True)]["recommend"].count()
            print("Cantidad de recomendaciones obtenidas")
            
            # Se cuenta la cantidad de dinero gastado por el usuario, haciendo una suma de la columna "price" de los juegos que tiene el usuario. 
            cantidad_dinero_gastado = usuario_juego_precio[usuario_juego_precio["user_id"] == user_id_str]["dinero_gastado"].iloc[0]

            cantidad_dinero_gastado = round(cantidad_dinero_gastado, 2)
            print("Cantidad de dinero gastado obtenido")

            # A partir del ID ingresado, del dinero gastado, del porcentaje de recomendación, y de la cantidad de juegos, se almacenan en el diccionario previamente creado con las claves correspondientes.
            diccionario_de_retorno["Usuario"] = user_id_str
            print("Usuario agregado al diccionario de salida")

            diccionario_de_retorno["Dinero gastado"] = f"{cantidad_dinero_gastado} USD"
            print("Dinero gastado agregado al diccionario de salida")
            
            # Si el usuario no hizo recomendaciones, para no tener errores de división por 0, defino que el porcentaje de recomendación es de 0%
            if cantidad_de_recomendaciones == 0:
                porcentaje_recomendacion = 0
                diccionario_de_retorno["Porcentaje de recomendación"] = f"{porcentaje_recomendacion}%"
            else:
                # Si hizo recomendaciones, se hace el calculo normalmente
                porcentaje_recomendacion = round((cantidad_de_recomendaciones * 100) / cantidad_juegos, 2)
                diccionario_de_retorno["Porcentaje de recomendación"] = f"{porcentaje_recomendacion}%"

            print("Porcentaje de recomendación agregado al diccionario de salida")

            diccionario_de_retorno["Cantidad de juegos"] = cantidad_juegos
            print("Cantidad de juegos agregados al diccionario de salida")
            
            # Se devuelve el diccionario creado
            return diccionario_de_retorno
        
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Archivo Parquet no encontrado: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")
    
@app.get("/informacion_usuario/{user_id}",response_model=dict)
async def informacion_usuario_use(user_id : Optional[str] = "sandwiches1 / 76561197970982474"):
    try:
        resultado = informacion_usuario(user_id)
        resultado = {k: (int(v) if isinstance(v, np.integer) else float(v) if isinstance(v, np.floating) else v) for k, v in resultado.items()}
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error inesperado:", str(e))
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    
# Tercer endpoint -------------------- 3
def usuario_por_genero(genero: str): # Se ingresa a la función el genero que se quiere determinar el usuario top
    try:

        # Ruta al archivo
        ruta_especifica = f"./Datasets/endpoint_3/genero_{genero}.parquet"
        print(f"Cargando data desde: {ruta_especifica}")  
        try:
            usuarios_que_jugaron_juegos_con_el_genero_dado = pd.read_parquet(ruta_especifica)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"Género {genero} no encontrado")
        
        print(1)
        # Se suman las horas de los distintos usuarios en el genero ingresado en la función
        usuarios_del_genero_con_horas_sumadas = usuarios_que_jugaron_juegos_con_el_genero_dado.groupby("user_id")["playtime_forever"].sum()
        print(2)

        # Se determina el nombre del usuario que acumula más horas jugadas en el genero ingresado
        jugador_con_mas_horas = usuarios_del_genero_con_horas_sumadas.idxmax()
        print(3)

        # Se agrega al diccionario de salida el nombre del usuario que acumula más horas en el genero ingresado
        diccionario_de_salida = {
            f"Usuario con más horas para el género {genero}": jugador_con_mas_horas
        }

        # Se suma la cantidad de horas del usuario top del genero
        cantidad_de_horas_acumuladas_en_distintos_años = usuarios_que_jugaron_juegos_con_el_genero_dado[usuarios_que_jugaron_juegos_con_el_genero_dado["user_id"] == jugador_con_mas_horas].groupby("año_salida")["playtime_forever"].sum()
        print(4)

        # Se crea una lista de diccionarios que tiene este formato: [{Año:Horas jugadas}, {Año:Horas jugadas}, ...]
        horas_jugadas_por_año = [
            {int(año): round(horas / 60, 2)}
            for año, horas in cantidad_de_horas_acumuladas_en_distintos_años.items()
            
        ]
        print(5)

        # Se agrega al diccionario de salida la lista creada anteriormente
        diccionario_de_salida["Horas jugadas en los distintos años"] = horas_jugadas_por_año

        print(6)
        return diccionario_de_salida
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Archivo Parquet no encontrado: {str(e)}")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@app.get("/usuario_por_genero/{genero}", response_model=dict)
async def usuario_por_genero_use(genero: str):
    try:
        resultado = usuario_por_genero(genero)
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Cuarto endpoint -------------------- 4
def mejor_desarrollador_del_anio(anio):
    """
    En este noveno prototipo, voy a ingresar un año a la función, y me va a devolver una lista de diccionarios con los top 3 desarrolladores
    """
    try:
        desarrolladores_y_reseñas = pd.read_parquet("./Datasets/endpoint_4/desarrolladores_y_reseñas.parquet")

        diccionario_salida = {}

        año_int = int(anio) # Chequeo si lo ingresado a la función es un número transformable a entero, en caso de que lo sea, lo almaceno en la variable año_int

        reseñas_del_año_dado = desarrolladores_y_reseñas[desarrolladores_y_reseñas["año"] == año_int] # Filtro el dataframe de reseñas con el año dado y con recommend == True

        desarrolladores_top = reseñas_del_año_dado["developer"].value_counts().nlargest(3) # Cuento las reseñas positivas de cada desarrollador y se guardan unicamente los 3 desarrolladores con más reseñas

        diccionario_interno = {f"Puesto nº{puesto}": {desarrollador: f"{recomendaciones} recomendaciones"} 
                               for puesto, (desarrollador, recomendaciones) in enumerate(desarrolladores_top.items(), 1)}

        diccionario_salida[año_int] = diccionario_interno # Finalmente el diccionario de salida tiene cómo clave el año ingresado y cómo valor el diccionario interno previamente creado

        return diccionario_salida
    except Exception as e:
        return e

@app.get("/mejor_desarrollador_del_anio/{anio}", response_model=dict)
async def mejor_desarrollador_del_anio_use(anio: int):
    try:
        resultado = mejor_desarrollador_del_anio(anio)
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


# Quinto endpoint -------------------- 5
def analisis_resenias_desarrollador(desarrollador):
    """
    En este sexto prototipo del endpoint, se va a ingresar a la función un nombre de un desarrollador, y va a devolver mediante un diccionario la cantidad de juegos de ese desarrollador, las reseñas de todos los juegos de ese desarrollador, y  también las cualidades de esas reseñas, osea cuantas corresponden a negativas, neutras y positivas.
    """
    try:
        diccionario_salida = {}
        diccionario_salida_interno = {}

        juegos = pd.read_parquet("./Datasets/endpoint_5/juegos.parquet")
        reseñas = pd.read_parquet("./Datasets/endpoint_5/resenias.parquet")

        juegos_filtrados_por_desarrollador = juegos[juegos["developer"] == desarrollador]

        diccionario_salida_interno["Cantidad de juegos"] = len(juegos_filtrados_por_desarrollador)

        id_juegos_desarrollador = juegos_filtrados_por_desarrollador["item_id"].values

        reseñas_juegos_desarrolladora = reseñas[reseñas["item_id"].isin(id_juegos_desarrollador)]

        diccionario_salida_interno["Cantidad de reseñas"] = len(reseñas_juegos_desarrolladora)

        cant_reseñas_negativas = len(reseñas_juegos_desarrolladora[reseñas_juegos_desarrolladora["puntaje"] == 0])

        cant_reseñas_neutras = len(reseñas_juegos_desarrolladora[reseñas_juegos_desarrolladora["puntaje"] == 1])

        cant_reseñas_positivas = len(reseñas_juegos_desarrolladora[reseñas_juegos_desarrolladora["puntaje"] == 2])

        lista_reseñas = [f"Negativas = {cant_reseñas_negativas}",       f"Neutras = {cant_reseñas_neutras}", 
            f"Positivas = {cant_reseñas_positivas}"]
        

        diccionario_salida_interno["Cualidad de las reseñas"] = lista_reseñas

        diccionario_salida[desarrollador] = diccionario_salida_interno

        return diccionario_salida
    except Exception as e:
        return e

@app.get("/analisis_resenias_desarrollador/{desarrollador}", response_model=dict)
async def analisis_resenias_desarrollador_use(desarrollador : str):
    try:
        resultado = analisis_resenias_desarrollador(desarrollador)
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


# Sistema de recomendación item-item
def recomendacion_juego(id_juego):
    # Cargamos el archivo solo con las columnas necesarias
    juegos_steam = pd.read_parquet("./Datasets/recomendacion/uno/steam_games_id_name_categorical.parquet", columns=["item_id", "item_name", "categorical_string"])
    
    # Transformamos el id del juego en str, para evitar inconvenientes
    id_juego = str(id_juego)

    # Comprobamos que exista el juego ingresado
    juego_ingresado = juegos_steam[juegos_steam["item_id"] == id_juego]
    if juego_ingresado.empty:
        raise ValueError(f"No se encontró ningún juego con el ID {id_juego}")
    
    # Determinamos el nombre del juego ingresado, las categorías del mismo y el índice
    nombre_juego = juego_ingresado["item_name"].iloc[0]
    categorias_juego = juego_ingresado["categorical_string"].iloc[0]
    indice_juego = juego_ingresado.index[0]
    
    # Liberamos memoria
    del juego_ingresado
    
    # Determinamos qué archivo de similitud cargar
    archivo_similitud = f"./Datasets/recomendacion/uno/similitud_entre_juegos{min(indice_juego // 1800 + 1, 13)}.parquet"
    
    # Cargamos solo la columna necesaria
    similitud_entre_juegos = pd.read_parquet(archivo_similitud, columns=[str(indice_juego)])
    
    # Determinamos la distancia entre el juego ingresado y los demás
    distancias = sorted(list(enumerate(similitud_entre_juegos[str(indice_juego)])), reverse=True, key=lambda x: x[1])[1:6]
    
    # Liberamos memoria
    del similitud_entre_juegos
    
    # Creamos una variable que va almacenar lo que su nombre indica
    juegos_recomendados_y_caracteristicas = {}
    
    # Recorremos la lista de distancias y almacenamos sus valores en el diccionario previamente creado
    for i, _ in distancias:
        juego = juegos_steam.iloc[i]
        juegos_recomendados_y_caracteristicas[juego.item_name] = juego.categorical_string
    
    # Devolvemos la salida correspondiente
    return {
        "Nombre del juego ingresado": nombre_juego,
        "Características del juego ingresado": categorias_juego,
        "Juegos recomendados": juegos_recomendados_y_caracteristicas
    }
    

        
    

@app.get("/recomendacion_juego/{id_juego}",response_model=dict)
async def recomendacion_juego_use(id_local : str = Query(default="430240", description="Nombre del juego: Duplexer")):
    try:
        resultado = recomendacion_juego(id_local)
        # Imprimir el resultado para depuración
        print("Resultado:", resultado)
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")
    
# Sistema de recomendación user-item
def recomendacion_usuario(usuario_elegido):
  try:
    logger = logging.getLogger("my_logger")

    print("Comenzando con la función")
    # Lectura de los archivos necesarios para trabajar
    similitud_de_usuarios_coseno = pd.read_parquet("./Datasets/recomendacion/similitud_entre_usuarios.parquet")
    matrix_norm = pd.read_parquet("./Datasets/recomendacion/matriz_normalizada.parquet")
    logger.info(f"Tamaño 1: {similitud_de_usuarios_coseno.shape}")
    logger.info(f"Tamaño 2: {matrix_norm.shape}")
    if similitud_de_usuarios_coseno.empty or matrix_norm.empty:
    # Manejar el caso de DataFrame vacío
        raise ValueError("El archivo Parquet está vacío.")
    print("Archivos leídos correctamente")

    if usuario_elegido not in matrix_norm.index:
            raise HTTPException(status_code=404, detail="Usuario no encontrado, intente con otro")
    
    # Busco los usuarios similares y los ordeno desde el más similar al menos similar. El 0.3 hace referencia a que el porcentaje minimo de similitud es un 30% y el 9 hace referencia al top 9 de usuarios más similares.
    usuarios_similares = similitud_de_usuarios_coseno[similitud_de_usuarios_coseno[usuario_elegido] > 0.3][usuario_elegido].sort_values(ascending=False)[:9] 

    juegos_jugados_por_usuario_elegido = matrix_norm[matrix_norm.index == usuario_elegido].dropna(axis=1,how="all").columns # Creamos un nuevo array que contenga los nombres de los juegos que el usuario elegio ha jugado

    # Juegos que usuarios similares han jugado. Eliminamos los juegos que ninguno de los usuarios similares haya jugado
    juegos_de_usuarios_similares = matrix_norm[matrix_norm.index.isin(usuarios_similares.index)].dropna(axis=1, how='all')

    # Eliminamos los juegos jugados por el usuario elegido
    juegos_de_usuarios_similares.drop(juegos_jugados_por_usuario_elegido,axis=1, inplace=True, errors='ignore')

    # Multiplicamos las puntuaciones de los juegos por las similitudes de los usuarios
    puntajes_ponderados = juegos_de_usuarios_similares.mul(usuarios_similares, axis=0)

        # Sumamos los puntajes ponderados por juego, ignorando NaN
    suma_puntajes = puntajes_ponderados.sum(axis=0, skipna=True)

        # Contamos la cantidad de usuarios que han puntuado cada juego
    conteo_puntajes = juegos_de_usuarios_similares.notna().mul(usuarios_similares, axis=0).sum(axis=0)

        # Calculamos el puntaje promedio de cada juego
    puntaje_promedio = suma_puntajes / conteo_puntajes

        # Convertimos el resultado en un DataFrame y lo ordenamos
    item_score = puntaje_promedio.reset_index().rename(columns={'index': 'item_name', 0: 'item_score'}).sort_values(by='item_score', ascending=False)

        # Seleccionamos los 5 mejores juegos
    lista_salida = item_score.head(5)['item_name'].tolist()

    return lista_salida
  except Exception as e:
    return e

@app.get("/recomendacion_usuario/{usuario_elegido}",response_model=dict)
async def recomendacion_usuario_use(id_local : str = Query(default="09879655452567", description="Otras opciones: Duplexer")):
    try:
        resultado = recomendacion_usuario(id_local)
        # Imprimir el resultado para depuración
        print("Resultado:", resultado)
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")