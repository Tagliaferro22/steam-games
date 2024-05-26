from fastapi import FastAPI, HTTPException
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# http://127.0.0.1:8000
app = FastAPI()

# Variables necesarias
Steam_games_important = pd.read_parquet("C:/Users/crisr/OneDrive/Escritorio/Mateo/Programacion/SoyHenry/Proyecto_Individual_uno/carpeta_raiz/Datasets/Steam_games_endpoint_1.parquet")
juegos_steam = pd.read_parquet("Datasets\id_name_categorical_of_games.parquet")
cv = CountVectorizer(max_features=15, stop_words='english')
vector = cv.fit_transform(juegos_steam["categorical"]).toarray()
similitud = cosine_similarity(vector)

@app.get("/")
def index():
    return {"Hello": "World"}

def developer(desarrollador: str):
    salida = {}

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
async def developer_use(desarrollador_local : str):
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

    # Busca en 
    indice_juego = juegos_steam[juegos_steam["item_id"] == id_juego].index[0]

    distancias = sorted(list(enumerate(similitud[indice_juego])), reverse=True, key=lambda x: x[1])
    
    juegos_recomendados = []
    detalles_juego = []
    salida = {}

    for i in distancias[1:6]:
        juegos_recomendados.append(juegos_steam.iloc[i[0]].item_name)
        detalles_juego.append(juegos_steam.iloc[i[0]].categorical)
    
    for i,j in enumerate(juegos_recomendados):
        salida[j] = detalles_juego[i]

    return salida

@app.get("/recomendacion_juego/{id_juego}",response_model=dict)
async def recommend_use(id_local : str):
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