import folium 
from folium.plugins import TimestampedGeoJson
from datetime import datetime, timedelta
from pathlib import Path
import webbrowser
from dijkstra import build_path_pero_pal_folium

# Esta funcion en su mayoria viene en la documentacion de folium, sin embargo le pedi a Gemini
# Que me ayudara a adaptar el tema de los tiempos dinamicos, ya que como el numero de nodos tiende 
# a variar por cada ruta los tiempos para que se impriman los nodos tambien lo hacen, fuera de eso el resto
# es codigo de ejemplo de folium adaptado
def mapa_interactivo(nodos, grafo):
    m = folium.Map([32.505466272730324, -116.9246645749568], zoom_start=19)

    coordenadas = build_path_pero_pal_folium(nodos,grafo)

    tiempo_inicial = datetime(2026, 9, 10, 12, 0, 0)
    tiempos_dinamicos = []
    
    for i in range(len(coordenadas)):
        nuevo_paso = tiempo_inicial + timedelta(minutes=i) 
        tiempos_dinamicos.append(nuevo_paso.isoformat() + "Z")

    lines = []
    for i in range(len(coordenadas) - 1):
        segmento = {
            "coordinates": [
                coordenadas[i],      
                coordenadas[i+1]    
            ],
            "dates": [
                tiempos_dinamicos[i],   
                tiempos_dinamicos[i+1]  
            ],
            "color": "blue", 
            "weight": 5
        }
        lines.append(segmento)

    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": line["coordinates"],
            },
            "properties": {
                "times": line["dates"],
                "style": {
                    "color": line["color"],
                    "weight": line["weight"] if "weight" in line else 5,
                },
            },
        }
        for line in lines
    ]

    folium.plugins.TimestampedGeoJson(
        {
            "type": "FeatureCollection",
            "features": features,
        },
        period="PT1M",
        add_last_point=True,
    ).add_to(m)
    

    # apertura automatica del mapa en el navegador 
    archivo_mapa = Path("ElCETYS.html").resolve()
    m.save(str(archivo_mapa))
    webbrowser.open_new_tab(archivo_mapa.as_uri())


def mostrar_error_ruta():
    mensaje = "Error: no existe una ruta disponible entre los nodos seleccionados."
    print(mensaje)
    archivo_mapa = Path("ElCETYS.html").resolve()
    archivo_mapa.write_text(
        '<!DOCTYPE html><html lang="es"><meta charset="utf-8">'
        '<title>Ruta no disponible</title><body><h1>'
        + mensaje + '</h1></body></html>',
        encoding="utf-8",
    )
    webbrowser.open_new_tab(archivo_mapa.as_uri())
