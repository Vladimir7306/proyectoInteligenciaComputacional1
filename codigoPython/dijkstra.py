from diccionario import crearGrafo
import heapq
ybg = crearGrafo()

def build_path_but_for_la_terminal(parent,target):
    path = [target]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    path.reverse()
    return path    

def dijkstra(start,goal,grafo, evitar=[None]):
    dist = {node: float('inf') for node in grafo}
    dist[start] = 0
    padres = {nodo: None for nodo in grafo}
    pq = [(0,start)]
    while pq:
        d, current =  heapq.heappop(pq)
        if current == goal:
            break
        if d > dist[current]:
            continue
        for vecino in grafo[current]["vecinos"]:
            if vecino['tipo'] in evitar:
                continue
            neighbor = vecino["destino"]
            costo = vecino["costo"]
            new_dist = d + costo
            if new_dist < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_dist
                padres[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

    return build_path_but_for_la_terminal(padres,goal), dist[goal]


# En esta funcion le pasamos los nodo y devuelve las coordendas en donde se encuentran
def build_path_pero_pal_folium(nodos,grafo):
    # Hacemos una lista vacia que vamos a llenar
    lista_coordenadas = []
    # Iteramos cada nodo existente 
    for id in nodos:
        #en un arreglo metemos la latitud y longitud, tiene que ser un arreglo porque si no 
        #folium no lo acepta 
        coordenadas = [grafo[id]['lng'], grafo[id]['lat']]
        #metemos la coordenadas de cada no a la lista vacia
        lista_coordenadas.append(coordenadas)
        #devolvemos la lista 
    return lista_coordenadas



