from diccionario import crearGrafo
from dijkstra import dijkstra
from mapa import mapa_interactivo #Realmente no es muy interactivo lol

# Estoy a punto de desmayarme porque no he dormido y me acabo de dar cuenta de que jorge no puso
# como tipo de arista los elevadores lol xd, porfa si testean este codigo usen el JSON nuevo 
# de jorge que no meti yo

ybg = crearGrafo()
print("\n BIENVENIDO A CETYS UNIVERSIDAD, ¿A DONDE QUIERES IR? \n")

primeros_10 = list(ybg.items())[:10] 
for indice, (id_nodo, datos) in enumerate(primeros_10):
        id = id_nodo
        nombre = datos.get('name', 'Sin nombre')
        print(f"{indice + 1}. {id} .{nombre}")

inicio = input("\n Desde: ")
final = input("\n Hasta: ")

respuesta = input("Deseas evitar algun tipo de camino en especifico? (y/n)")
if respuesta == 'y':
        evito = input("Que quieres evitar?")
        print("Desplegando ruta y costo:")
        ruta, costo = dijkstra(inicio,final,ybg,evito)
        coordenadas = mapa_interactivo(ruta,ybg)
        print(f"La ruta que debes de seguir es: {ruta} \n")
        print(f"Tiene un costo de {costo}\n")
        print("Ya puesdes consultar el mapa de la ruta")


elif respuesta == 'n':
        print("Desplegando ruta y costo:")
        ruta, costo = dijkstra(inicio,final,ybg)
        coordenadas = mapa_interactivo(ruta,ybg)
        print(f"La ruta que debes de seguir es: {ruta} \n")
        print(f"Tiene un costo de {costo}\n")
        print("Ya puesdes consultar el mapa de la ruta")        







