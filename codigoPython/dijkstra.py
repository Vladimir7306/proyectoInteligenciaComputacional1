from diccionario import crearGrafo
#Ya despues mueves este a la interfaz 
import heapq
ybg = crearGrafo()

def build_path_but_for_la_terminal(parent,target):
    path = [target]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
        path.reverse()
    return path

def build_path_pero_pal_folium():
    raise ValueError()


def dijkstra(grafo, origen, destino):
    # Inicializamos las distancias con infinito para todos los nodos
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0
    
    # Diccionario para reconstruir el camino más corto
    padres = {nodo: None for nodo in grafo}
    
    # Cola de prioridad que almacena tuplas (costo_acumulado, nodo_actual)
    cola_prioridad = [(0, origen)]
    
    while cola_prioridad:
        costo_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        # Si llegamos al nodo destino, detenemos la búsqueda (optimización)
        if nodo_actual == destino:
            break
            
        # Si extraemos un camino obsoleto (más largo que el ya registrado), lo ignoramos
        if costo_actual > distancias[nodo_actual]:
            continue
            
        # Revisamos todos los vecinos del nodo actual
        for vecino in grafo[nodo_actual].get('vecinos', []):
            nodo_vecino = vecino['destino']
            costo_arista = vecino['costo']
            
            # Calculamos el costo de llegar a este vecino a través del nodo actual
            nuevo_costo = costo_actual + costo_arista
            
            # Si encontramos un camino más barato hacia el vecino, lo actualizamos
            if nuevo_costo < distancias.get(nodo_vecino, float('inf')):
                distancias[nodo_vecino] = nuevo_costo
                padres[nodo_vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (nuevo_costo, nodo_vecino))
                
    # Reconstrucción de la ruta desde el destino hacia el origen
    ruta = []
    nodo_actual = destino
    
    while nodo_actual is not None:
        ruta.append(nodo_actual)
        nodo_actual = padres.get(nodo_actual)
        
    ruta.reverse() # Invertimos para que vaya de origen a destino
    
    # Verificamos si realmente se encontró un camino válido
    if len(ruta) == 1 and origen != destino:
        return {
            "ruta": [],
            "costo_total": float('inf'),
            "mensaje": "No hay un camino disponible entre los nodos indicados."
        }
        
    return {
        "ruta": ruta,
        "costo_total": distancias[destino]
    }

primer = dijkstra(ybg, 'n1', 'n8')
print(primer)
