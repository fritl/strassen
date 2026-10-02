from contextlib import contextmanager, asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from dijkstra import dijkstra
from streets import find_next_node, load_gpkg, node_to_coords, StreetGraph

G: StreetGraph


@asynccontextmanager
async def lifespan(app: FastAPI):
    global G
    G = load_gpkg(Path("./data/strassen.gpkg"), "strassen")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/api/nearest_node")
def nearest_node(lat: float, lon: float) -> tuple[float, float]:
    return node_to_coords(G, find_next_node(G, (lon, lat)))


@app.get("/api/route")
def get_path(
    start_lat: float, start_lng: float, end_lat: float, end_lng: float
) -> tuple[float, list[tuple[float, float]]]:
    start_node = find_next_node(G, (start_lng, start_lat))
    end_node = find_next_node(G, (end_lng, end_lat))

    return dijkstra(G, start_node, end_node)
