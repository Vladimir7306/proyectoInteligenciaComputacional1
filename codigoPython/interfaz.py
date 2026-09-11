from diccionario import crearGrafo
from dijkstra import dijkstra
from mapa import mapa_interactivo, mostrar_error_ruta #Super interactivo

#Al usar este codigo se corre el Json mas reciente dentro de la carpeta codigoPython
# 
def mas_cercano():
        inicio_s = input("¿Dónde andas?")
        select = input("¿A qué categoría de lugar quieres ir?")
        nodos_cat = []
        for id_nodo, datos in ybg.items():
                if datos.get('category') == select:
                        nodos_cat.append(id_nodo)
            
        if not nodos_cat:
                print("No existe esa categoria")
        else:
                menor_costo = float('inf')
                mejor_ruta = []
                mejor_nodo = None
                for n in nodos_cat:
                        ruta, costo = dijkstra(inicio_s, n,ybg)            
                        if costo < menor_costo:
                                menor_costo = costo
                                mejor_ruta = ruta
                                mejor_nodo = n
                
                if menor_costo == float('inf'):
                        mostrar_error_ruta()
                        print("No hay ningún camino disponible hacia los lugares de esa categoría.")
                else:
                        mapa_interactivo(mejor_ruta, ybg)
                        nombre_destino = ybg[mejor_nodo]['name']
                        print(f"\n¡Listo! El lugar más cercano es: {nombre_destino}")
                        print(f"La ruta que debes seguir es: {mejor_ruta}")
                        print(f"Costo total del trayecto: {menor_costo}")
                        print("Ya puedes consultar el mapa de la ruta (ElCETYS.html)")


def especifico():
        inicio = input("\n Desde: ")
        final = input("\n Hasta: ")

        respuesta = input("Deseas evitar algun tipo de camino en especifico? (y/n)")
        if respuesta == 'y':
                evito = input("Que quieres evitar?")
                print("Desplegando ruta y costo:")
                ruta, costo = dijkstra(inicio,final,ybg,evito)
                if costo == float('inf'):
                        mostrar_error_ruta()
                        return
                coordenadas = mapa_interactivo(ruta,ybg)
                print(f"La ruta que debes de seguir es: {ruta} \n")
                print(f"Tiene un costo de {costo}\n")
                print("Ya puesdes consultar el mapa de la ruta")


        elif respuesta == 'n':
                print("Desplegando ruta y costo:")
                ruta, costo = dijkstra(inicio,final,ybg)
                if costo == float('inf'):
                        mostrar_error_ruta()
                        return
                coordenadas = mapa_interactivo(ruta,ybg)
                print(f"La ruta que debes de seguir es: {ruta} \n")
                print(f"Tiene un costo de {costo}\n")
                print("Ya puesdes consultar el mapa de la ruta")  

ybg = crearGrafo()
print("\n BIENVENIDO A CETYS UNIVERSIDAD, ¿A DONDE QUIERES IR? \n")

primeros_10 = list(ybg.items())[:10] 
for indice, (id_nodo, datos) in enumerate(primeros_10):
        id = id_nodo
        nombre = datos.get('name', 'Sin nombre')
        print(f"{indice + 1}. {id} .{nombre}")

print("Que quieres hacer?")
print("1. Buscar la distancia mas cernaca a un lugar de una categoria especifica? ")
print("2. Ir a un lugar en especifico")
opcion = input("Quiero: ")
match opcion:
        case "1":
                mas_cercano()
        case "2":
                especifico()    







