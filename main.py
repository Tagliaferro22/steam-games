from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# http://127.0.0.1:8000
app = FastAPI()

@app.get("/")
def index():
    return {"Hello": "World"}


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

def user_data(user_id):
    # Cargamos los dataframes dentro de la función
    user_items = pd.read_parquet("./Datasets/user_items_endpoint_2.parquet")
    user_reviews = pd.read_parquet("./Datasets/user_reviews_endpoint_2.parquet")
    usuario_juego_precio = pd.read_parquet("./Datasets/steam_games_and_users_endpoint_2.parquet")

    diccionario_de_retorno = {} # Diccionario que va a almacenar las variables correspondientes a la salida de la función

    if user_items[user_items["user_id"] == str(user_id)].empty: # En caso de que no haya usuarios con el ID ingresado, se muestra lo siguiente:
        return "No se encontraron datos para el usuario con ID: " + str(user_id)
    else: # En caso de que haya usuarios con el ID ingresado, se muestra lo siguiente

        # Se cuenta la cantidad de juegos que tiene el usuario
        cantidad_juegos = user_items[user_items["user_id"] == str(user_id)]["user_id"].count()

        # Se cuenta la cantidad de recomendaciones. En la columna recommend aparece "True" o "False", tuve en cuenta sólo las que aparece "True" del usuario ingresado.
        cantidad_de_recomendaciones = user_reviews[(user_reviews["user_id"] == str(user_id)) & user_reviews["recommend"] == True]["recommend"].count()

        # Se cuenta la cantidad de dinero gastado por el usuario, haciendo una suma de la columna "price" de los juegos que tiene el usuario. 
        cantidad_dinero_gastado = usuario_juego_precio[usuario_juego_precio["user_id"] == str(user_id)]["price"].sum()

        # A partir del ID ingresado, del dinero gastado, del porcentaje de recomendación, y de la cantidad de juegos, se almacenan en el diccionario previamente creado con las claves correspondientes.
        diccionario_de_retorno["Usuario"] = user_id
        diccionario_de_retorno["Dinero gastado"] = f"{round(cantidad_dinero_gastado, 2)} USD"

        # Si el usuario no hizo recomendaciones, para no tener errores de división por 0, defino que el porcentaje de recomendación es de 0%
        if cantidad_de_recomendaciones == 0:
            diccionario_de_retorno["Porcentaje de recomendaciones"] = "0%"
        else:
            # Si hizo recomendaciones, se hace el calculo normalmente
            diccionario_de_retorno["Porcentaje de recomendación"] = f"{round((cantidad_de_recomendaciones * 100) / cantidad_juegos, 2)}%"
        
        diccionario_de_retorno["Cantidad de juegos"] = cantidad_juegos
        
        # Se devuelve el diccionario creado
        return diccionario_de_retorno
    
@app.get("/user_data/{user_id}",response_model=dict)
async def recommend_use(id_local : str = Query(default="sandwiches1 / 76561197970982479")):
    try:
        resultado = user_data(id_local)
        # Imprimir el resultado para depuración
        print("Resultado:", resultado)
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")