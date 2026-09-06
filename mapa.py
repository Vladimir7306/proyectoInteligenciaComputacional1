import folium 
m = folium.Map([32.505466272730324, -116.9246645749568], zoom_start=100)

folium.Marker(
    location=[32.505466272730324, -116.9246645749568],
    tooltip="Click me!",
    popup="iOS lab",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

folium.Marker(
    location=[32.50578344907374, -116.9245173616592],
    tooltip="Click me!",
    popup="Cafeteria",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

folium.Marker(
    location=[32.505974471951035, -116.92374581691023],
    tooltip="Click me!",
    popup="CECE 2",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

folium.Marker(
    location=[32.50605804433695, -116.92384314480552],
    tooltip="Click me!",
    popup="Bano CECE",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

folium.Marker(
    location=[32.505540457116126, -116.92477443434825],
    tooltip="Click me!",
    popup="Bano administrativo",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

folium.Marker(
    location=[32.5053044959788, -116.92364268473547],
    tooltip="Click me!",
    popup="Bano E4",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

folium.Marker(
    location=[32.5051333068815, -116.92359715209908],
    tooltip="Click me!",
    popup="Juice N Joy",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

folium.Marker(
    location=[32.50575049717793, -116.92488192328878],
    tooltip="Click me!",
    popup="salon heterogeneas",
    icon=folium.Icon(icon="cloud"),
).add_to(m)


camino1 = [
    (32.505466272730324, -116.9246645749568),
    (32.50521456330664, -116.92454384784416),
    (32.50498044383497, -116.92446136991676), # Convergencia 
    (32.50518326369503, -116.9236318424405),
    (32.5051333068815, -116.92359715209908),
]

camino2 = [
    (32.505466272730324, -116.9246645749568),
    (32.50521456330664, -116.92454384784416),
    (32.50516074338134, -116.92471686343046),
    (32.50495947984576, -116.92467334900876),
    (32.50498044383497, -116.92446136991676),
     (32.50518326369503, -116.9236318424405),
    (32.5051333068815, -116.92359715209908),
   
]

folium.PolyLine(camino1, tooltip="Coast").add_to(m)
folium.PolyLine(camino2, tooltip="Coast").add_to(m)


m.save("mapaCETYS.html")