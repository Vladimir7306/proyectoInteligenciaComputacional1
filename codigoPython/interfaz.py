from diccionario import crearGrafo
from dijkstra import dijkstra
from mapa import mapa_interactivo #Super interactivo

#Al usar este codigo se corre el Json mas reciente dentro de la carpeta codigoPython

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







