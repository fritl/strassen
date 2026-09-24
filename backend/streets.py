import math
from dataclasses import dataclass
from pathlib import Path

import fiona
from pyproj import Geod


@dataclass(frozen=True)
class EdgeInfo:
    time: float
    coordinates: tuple[tuple[float, float], ...]


type StreetGraph = dict[int, dict[int, EdgeInfo]]


def load_gpkg(file: Path, layer: str) -> StreetGraph:
    with fiona.open(file, layer=layer) as src:
        G: StreetGraph = {}

        def add_edge(
            from_node: int,
            to_node: int,
            length: float,
            speed: int,
            coordinates: tuple[tuple[float, float], ...],
        ):
            if G.get(from_node) is None:
                G[from_node] = {}

            G[from_node][to_node] = EdgeInfo(
                (3.6 * length) / speed,
                tuple(coordinates),
            )

        num_edges = len(src)
        speed_skips = 0
        for i, feat in enumerate(src):
            if i % 10000 == 0:
                print(f"{i} / {num_edges}")
            geom = feat["geometry"]
            props = feat["properties"]

            coords: list[tuple[float, float]] = geom["coordinates"]
            from_node = props["node_from_short_id"]
            to_node = props["node_to_short_id"]
            length = props["length"]

            if length <= 0:
                continue

            if props["construction_state"] != 5:
                continue

            acces_tow = props.get("access_tow")
            if (acces_tow is None and props["oneway_car"] == 1) or (
                acces_tow is not None and acces_tow & 4
            ):
                speed = props["speed_tow_car"]
                if speed <= 0:
                    speed = props["maxspeed_tow_car"]
                if speed <= 0:
                    speed_skips += 1
                    continue
                add_edge(from_node, to_node, length, speed, tuple(coords))

            access_bkw = props.get("access_bkw")
            if (access_bkw is None and props["oneway_car"] == 0) or (
                access_bkw is not None and access_bkw & 4
            ):
                speed = props["speed_bkw_car"]
                if speed <= 0:
                    speed = props["maxspeed_bkw_car"]
                if speed <= 0:
                    speed_skips += 1
                    continue
                coords.reverse()
                add_edge(to_node, from_node, length, speed, tuple(coords))
    print("Speed skips:", speed_skips)
    return G


def find_next_node(streets: StreetGraph, coords: tuple[float, float]) -> int:
    geod = Geod(ellps="WGS84")
    min_dist = math.inf
    min_node = -1
    for node in streets:
        node_coords = next(iter(streets[node].values())).coordinates[0]
        _, _, d = geod.inv(node_coords[1], node_coords[0], coords[1], coords[0])
        if d < min_dist:
            min_dist = d
            min_node = node
    return min_node
