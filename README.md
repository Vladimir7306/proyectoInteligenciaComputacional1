# Editor del grafo CETYS

Abre `editorCETYS.html` en el navegador con conexión a internet. No requiere instalar Python ni iniciar un servidor. Los archivos editor.css y editor.js deben permanecer junto al HTML.

## Uso
1. Activa **Colocar nodos** y haz clic en el mapa.
2. Completa nombre, edificio, piso, categoría y notas; pulsa **Guardar nodo**. Puedes mover los nodos arrastrándolos en modo Seleccionar.
3. En conexiones, elige origen y destino, tipo, costo en metros, accesibilidad y sentido. Pulsa **Guardar conexión**.
4. Para conexiones verticales crea un acceso por piso, aunque compartan coordenadas. Usa el selector de piso para distinguirlos. Las conexiones coincidentes se dibujan como un anillo.
5. Selecciona una conexión desde la lista o haciendo clic en su línea para modificarla.
6. Exporta **grafoCETYS.json** para respaldar el trabajo. Importar reemplaza el grafo tras validar el archivo y pedir confirmación.

El borrador se guarda en el almacenamiento local del navegador después de cada cambio confirmado. No se comparte entre navegadores y puede perderse al borrar sus datos; el JSON es el respaldo portable. Los cambios escritos en formularios requieren pulsar Guardar antes de exportar.

## Modelo
- Nodo: id, name, building, floor (entero), category, lat, lng, notes.
- Arista: id, source, target, cost (metros, no negativo), type, accessible, bidirectional.
- accessible: true = verificado accesible; false = no accesible; null = por verificar.
- bidirectional: false permite únicamente source → target.
- type: pasillo, sendero, escalera, elevador o rampa.
- Una escalera siempre es no accesible. Cambiar entre pisos requiere escalera, elevador o rampa.
- La distancia estimada es horizontal en línea recta; para escaleras y rampas hay que medir el recorrido real. Mantén la misma unidad de costo en todas las aristas.

Los ocho lugares iniciales se copiaron de mapa.py. Piso 0 y edificio "Por verificar" son valores provisionales, no un levantamiento del campus. Las conexiones se registran manualmente para no presentar caminos supuestos como datos verificados.

## Leer desde Python
```python
import json

with open("grafoCETYS.json", encoding="utf-8") as archivo:
    grafo = json.load(archivo)

adyacencia = {nodo["id"]: [] for nodo in grafo["nodes"]}
for arista in grafo["edges"]:
    adyacencia[arista["source"]].append((arista["target"], arista))
    if arista["bidirectional"]:
        adyacencia[arista["target"]].append((arista["source"], arista))
```

El editor prepara los datos; la búsqueda con Dijkstra y las consultas por movilidad son la siguiente etapa. El mapa anterior mapaCETYS.html y su generador mapa.py siguen disponibles por separado.

