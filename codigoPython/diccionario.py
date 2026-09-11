import json

# Use gemini para hacer la funcion mas limpia aunque inicialmente la habia usado porque n1 no tenia vecinos
# lo cual era porque escribi mal accesibility o accesible  
# abrimos el archivo json y lo guardamos en la variable grafo
def crearGrafo():
    # Abrimos el json y lo leemos, guardamos su contenido en una variable llamada grafo
    with open("grafoCETYS.json", "r", encoding="utf-8") as archivo:
        grafo = json.load(archivo)
    # Hacemos un diccionario donde guardemos la informacion tanto de lo nodos como de las aristas
    grafoCETYS = {}
    #Iteramos en todos los nodos del json 
    for nodo in grafo["nodes"]:
        #Guaradamos el id de cada nodo en como nuestras keys
        id_nodo = nodo["id"]
        #Y ahora para cada key es de cir para cada nodo le metemos lo siguiente elementos 
        grafoCETYS[id_nodo] = {
            "name": nodo.get("name"),
            "lat": nodo.get("lat"),
            "lng": nodo.get("lng"),
            "category": nodo.get("category"),
            "vecinos": []
        }
        
    # En el JSON buscamos las aristas y obtenemos su origen y destino 
    for arista in grafo["edges"]:
        origen = arista["source"]
        destino = arista["target"]
        # guardamos los siguiente elementos en cada arista
        info_conexion = {
            'id_arista': arista['id'],
            'destino': destino,
            'tipo': arista['type'],
            'costo': arista['cost'],
        }
        
        # y ya lo guardamos en el grafo, pero primero checamos que exista el nodo de origen de la arista
        if origen in grafoCETYS:
            grafoCETYS[origen]['vecinos'].append(info_conexion)

        # En el caso de las aristas bidireccionales tomamos el origen como el destino ya que apuntan al revez     
        if arista.get('bidirectional', False):
            doble_conexion = {
                'id_arista': arista['id'],
                'destino': origen,
                'tipo': arista['type'],
                'costo': arista['cost'],
            }
            
            # lo mismo que arriba 
            if destino in grafoCETYS:
                grafoCETYS[destino]['vecinos'].append(doble_conexion)
                
    return grafoCETYS
