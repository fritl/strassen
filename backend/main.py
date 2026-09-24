from pathlib import Path

import folium

from dijkstra import dijkstra
from streets import find_next_node, load_gpkg

G = load_gpkg(Path("./data/strassen.gpkg"), "strassen")
print(len(G.keys()))

start = (46.043, 10.403)
start = (start[1], start[0])
end = (48.3593, 17.0264)
end = (end[1], end[0])

print("Finding next node start")
start_node = find_next_node(G, start)
print("Finding next node end")
end_node = find_next_node(G, end)
print("Finding path")
time, path = dijkstra(G, start_node, end_node)

print(f"Found path duration: {time / 60:.1f}m")
print("Creating map")
m = folium.Map(location=[47.5, 14.0], zoom_start=8)
folium.PolyLine([lat, lon] for lon, lat in path).add_to(m)
print("Saving map")
m.save("path.html")
