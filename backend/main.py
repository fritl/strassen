import pickle
from pathlib import Path

from fastapi import FastAPI

from dijkstra import dijkstra
from streets import NodeIndex, load_gpkg, node_to_coords

SOURCE = Path("./data/strassen.gpkg")
CACHE = Path("cache/streets.pkl")

if CACHE.exists() and CACHE.stat().st_mtime > SOURCE.stat().st_mtime:
    with CACHE.open("rb") as f:
        G = pickle.load(f)
else:
    CACHE.parent.mkdir(exist_ok=True)
    G = load_gpkg(SOURCE, "strassen")
    with CACHE.open("wb") as f:
        pickle.dump(G, f, pickle.HIGHEST_PROTOCOL)


node_index = NodeIndex(G)
app = FastAPI()


@app.get("/api/nearest_node")
def nearest_node(lat: float, lon: float) -> tuple[float, float]:
    return node_to_coords(G, node_index.find_next_node((lon, lat)))


@app.get("/api/route")
def get_path(
    start_lat: float, start_lng: float, end_lat: float, end_lng: float
) -> tuple[float, list[tuple[float, float]]]:
    start_node = node_index.find_next_node((start_lng, start_lat))
    end_node = node_index.find_next_node((end_lng, end_lat))

    return dijkstra(G, start_node, end_node)
