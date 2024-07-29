from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# http://127.0.0.1:8000
app = FastAPI()

@app.get("/")
def index():
    return {"Hello": "World"}

# Primer endpoint -------------------- 1
def developer(desarrollador: str):
    salida = {}
    Steam_games_important = pd.read_parquet("./Datasets/Steam_games_endpoint_1.parquet")
    # Imprimir información relevante antes del bucle
    print("Desarrollador:", desarrollador)
    print("Valores únicos de release_year:", Steam_games_important[Steam_games_important["developer"] == desarrollador]["release_year"].unique())

    if desarrollador not in Steam_games_important["developer"].unique():
        raise HTTPException(status_code=404, detail="Developer not found")
    
    for año in Steam_games_important[Steam_games_important["developer"] == desarrollador]["release_year"].unique():
        # Agregar más impresiones dentro del bucle si es necesario
        print("Año actual:", año)

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
        print("Resultado:", resultado)
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")

# Segundo endpoint -------------------- 2
def user_data(user_id):
    try:
        user_id_str = str(user_id)
        # Cargamos los dataframes dentro de la función
        user_items = pd.read_parquet("./Datasets/user_items_endpoint_2.parquet")
        user_reviews = pd.read_parquet("./Datasets/user_reviews_endpoint_2.parquet")
        usuario_juego_precio = pd.read_parquet("./Datasets/steam_games_and_users_endpoint_2.parquet")
        print("Archivos leídos correctamente")
        diccionario_de_retorno = {} # Diccionario que va a almacenar las variables correspondientes a la salida de la función

        if user_items[user_items["user_id"] == user_id_str].empty: # En caso de que no haya usuarios con el ID ingresado, se muestra lo siguiente:
            return {"Detail":"No se encontraron datos para el usuario con ID: " + user_id_str}
        else: # En caso de que haya usuarios con el ID ingresado, se muestra lo siguiente
            print("Condicional pasado exitosamente")
            # Se cuenta la cantidad de juegos que tiene el usuario
            cantidad_juegos = user_items[user_items["user_id"] == user_id_str]["user_id"].count()

            print(f"Cantidad de juegos: {cantidad_juegos}, Tipo: {type(cantidad_juegos)}")
            # Se cuenta la cantidad de recomendaciones. En la columna recommend aparece "True" o "False", tuve en cuenta sólo las que aparece "True" del usuario ingresado.
            cantidad_de_recomendaciones = user_reviews[(user_reviews["user_id"] == user_id_str) & (user_reviews["recommend"] == True)]["recommend"].count()

            print(f"Cantidad de recomendaciones: {cantidad_de_recomendaciones}, Tipo: {type(cantidad_de_recomendaciones)}")
            # Se cuenta la cantidad de dinero gastado por el usuario, haciendo una suma de la columna "price" de los juegos que tiene el usuario. 
            cantidad_dinero_gastado = usuario_juego_precio[usuario_juego_precio["user_id"] == user_id_str]["price"].sum()

            print(f"Cantidad de dinero gastado: {cantidad_dinero_gastado}, Tipo: {type(cantidad_dinero_gastado)}")
            # A partir del ID ingresado, del dinero gastado, del porcentaje de recomendación, y de la cantidad de juegos, se almacenan en el diccionario previamente creado con las claves correspondientes.
            diccionario_de_retorno["Usuario"] = user_id_str
            print("Primera parte del diccionario hecha")
            diccionario_de_retorno["Dinero gastado"] = f"{round(cantidad_dinero_gastado, 2)} USD"
            print("Segunda parte del diccionario hecha")
            # Si el usuario no hizo recomendaciones, para no tener errores de división por 0, defino que el porcentaje de recomendación es de 0%
            if cantidad_de_recomendaciones == 0:
                porcentaje_recomendacion = 0
                diccionario_de_retorno["Porcentaje de recomendación"] = f"{porcentaje_recomendacion}%"
            else:
                # Si hizo recomendaciones, se hace el calculo normalmente
                porcentaje_recomendacion = round((cantidad_de_recomendaciones * 100) / cantidad_juegos, 2)
                diccionario_de_retorno["Porcentaje de recomendación"] = f"{porcentaje_recomendacion}%"

            print(f"Porcentaje de recomendación: {diccionario_de_retorno['Porcentaje de recomendación']}, Tipo: {type(porcentaje_recomendacion)}")
            print("Tercera parte del diccionario hecha")
            diccionario_de_retorno["Cantidad de juegos"] = cantidad_juegos
            print("Cuarta parte del diccionario hecha")
            
            # Se devuelve el diccionario creado
            return diccionario_de_retorno
        
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Archivo Parquet no encontrado: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")
    
@app.get("/user_data/{user_id}",response_model=dict)
async def recommend_use(user_id : Optional[str] = "sandwiches1 / 76561197970982474"):
    try:
        resultado = user_data(user_id)
        resultado = {k: (int(v) if isinstance(v, np.integer) else float(v) if isinstance(v, np.floating) else v) for k, v in resultado.items()}
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error inesperado:", str(e))
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    
# Tercer endpoint -------------------- 3
def usuario_por_genero(genero): # Se ingresa el genero de vídeojuegos
    try:

        diccionario_de_salida = {} # Se crea el diccionario que posteriormente va a devolver la función cómo salida

        steam_games_filtrable_por_genero = steam_games.explode("genres") # Se crea un nuevo dataframe a partir del original de vídeojuegos con el método .explode, lo cuál facilita que sea filtrado posteriormente por el genero ingresado.

        juegos_con_el_genero_dado = steam_games_filtrable_por_genero[steam_games_filtrable_por_genero["genres"] == genero] # Se filtra el dataframe previamente creado por el genero ingresado en la función

        juegos_con_el_genero_dado = juegos_con_el_genero_dado.drop(columns=["genres","release_date","descripción_temporal"]) # Se eliminan las columnas irrelevantes para optimizar el rendimiento de la función. 

        juegos_con_el_genero_dado = juegos_con_el_genero_dado.sort_values("año_salida") # Se ordenan los juegos por el año de salida

        usuarios_que_jugaron_juegos_con_el_genero_dado = pd.merge(juegos_con_el_genero_dado, user_items, on='item_id', how='inner') # Se unen los datafrmae de juegos con el genero ingresado con la función (juegos_con_el_genero_dado), con el de juegos que tienen los usuarios (user_items).

        usuarios_que_jugaron_juegos_con_el_genero_dado.drop(columns=["item_id","item_name_y"], inplace=True) # Nuevamente se eliminan las columnas irrelevante para optimizar el rendimiento de la función

        usuarios_del_genero_con_horas_sumadas = usuarios_que_jugaron_juegos_con_el_genero_dado.groupby(["user_id"]).sum().reset_index() # Se suman las horas de cada usuario de todos los juegos que jugó. EJ: Juan jugó dos juegos, 2 y 3 horas respectivamente, en total Juan jugó 5 horas.

        jugador_del_genero_con_mas_horas = usuarios_del_genero_con_horas_sumadas[usuarios_del_genero_con_horas_sumadas["playtime_forever"] == usuarios_del_genero_con_horas_sumadas["playtime_forever"].max()]["user_id"].iloc[0] # Se filtra el dataframe por el usuario que más horas acumule en el genero dado, y se conserva sólo el user_id

        diccionario_de_salida[f"Usuario con más horas para el género {genero}"] = jugador_del_genero_con_mas_horas # Se crea la primera clave:valor del diccionario, la clave es el genero ingresado y el valor es el nombre del jugador, sería genero:user

        datos_usuario_top = usuarios_que_jugaron_juegos_con_el_genero_dado[(usuarios_que_jugaron_juegos_con_el_genero_dado["user_id"] == jugador_del_genero_con_mas_horas) & (usuarios_que_jugaron_juegos_con_el_genero_dado["playtime_forever"] != 0)]

        jugador_top_del_genero_agrupado_por_nombre_y_año = datos_usuario_top.groupby(["año_salida"]).sum().reset_index()

        horas_jugadas_por_año = []
        for año in jugador_top_del_genero_agrupado_por_nombre_y_año["año_salida"]: # Bucle que recorre cada año del dataframe
            # A partir de los años, queremos saber el valor correspondiente a playtime_forever
            tiempo_de_juego_de_cada_año_en_minutos = jugador_top_del_genero_agrupado_por_nombre_y_año[jugador_top_del_genero_agrupado_por_nombre_y_año["año_salida"] == año]["playtime_forever"]
            tiempo_de_juego_de_cada_año_en_horas = round(tiempo_de_juego_de_cada_año_en_minutos / 60, 2)
            diccionario_temporal = {}
            diccionario_temporal[int(año)] = tiempo_de_juego_de_cada_año_en_horas.iloc[0]
            horas_jugadas_por_año.append(diccionario_temporal)
            

        diccionario_de_salida["Horas jugadas en los distintos años"] = horas_jugadas_por_año

        return diccionario_de_salida
    except Exception as e:
        return e
    
@app.get("/user_data/{user_id}",response_model=dict)
async def recommend_use(user_id : Optional[str] = "sandwiches1 / 76561197970982474"):
    try:
        resultado = user_data(user_id)
        resultado = {k: (int(v) if isinstance(v, np.integer) else float(v) if isinstance(v, np.floating) else v) for k, v in resultado.items()}
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error inesperado:", str(e))
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")





# Función que toma cómo argumento el ID de un juego y recomienda 5 similares
def recomendacion_juego(id_juego):

    juegos_steam = pd.read_parquet("./Datasets/id_name_categorical_of_games.parquet")

    cv = CountVectorizer(max_features=15, stop_words='english')
    vector = cv.fit_transform(juegos_steam["categorical"]).toarray()
    similitud = cosine_similarity(vector)

    # Busca en 
    indice_juego = juegos_steam[juegos_steam["item_id"] == id_juego].index[0]

    distancias = sorted(list(enumerate(similitud[indice_juego])), reverse=True, key=lambda x: x[1])
    
    juegos_recomendados = []

    for i in distancias[1:6]:
        juegos_recomendados.append(juegos_steam.iloc[i[0]].item_name)
    
    

    return {"Juegos recomendados":juegos_recomendados}


@app.get("/recomendacion_juego/{id_juego}",response_model=dict)
async def recommend_use(id_local : str = Query(default="430240", description="Nombre del juego: Duplexer")):
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