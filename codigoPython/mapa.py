import folium 
from folium.plugins import TimestampedGeoJson
from datetime import datetime, timedelta
from dijkstra import build_path_pero_pal_folium, dijkstra
from diccionario import crearGrafo

grafito = crearGrafo()

ruta, costo = dijkstra('n1','n8', grafito)

def mapa_interactivo(nodos, grafo):
    m = folium.Map([32.505466272730324, -116.9246645749568], zoom_start=19)

    coordenadas = build_path_pero_pal_folium(nodos,grafo)

    tiempo_inicial = datetime(2026, 9, 10, 12, 0, 0)
    tiempos_dinamicos = []
    
    for i in range(len(coordenadas)):
        nuevo_paso = tiempo_inicial + timedelta(minutes=i) # Incrementa 1 hora por nodo
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
    
    m.save("ElCETYS.html")

mapa_interactivo(ruta,grafito)