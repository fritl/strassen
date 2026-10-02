from sklearn.neighbors import BallTree
from math import radians
from dataclasses import dataclass
from pathlib import Path

import fiona


@dataclass(frozen=True)
class EdgeInfo:
    time: float
    coordinates: tuple[tuple[float, float], ...]


type StreetGraph = dict[int, dict[int, EdgeInfo]]


def load_gpkg(file: Path, layer: str) -> StreetGraph:
    with fiona.open(
        file,
        layer=layer,
        include_fields=[
            "node_from_short_id",
            "node_to_short_id",
            "length",
            "construction_state",
            "access_tow",
            "oneway_car",
            "speed_tow_car",
            "maxspeed_tow_car",
            "access_bkw",
            "speed_bkw_car",
            "maxspeed_bkw_car",
        ],
    ) as src:
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
                    continue
                coords.reverse()
                add_edge(to_node, from_node, length, speed, tuple(coords))
    return G


class NodeIndex:
    def __init__(self, streets: StreetGraph):
        self.__node_ids = []
        self.__coordinates = []
        for id, v in streets.items():
            self.__node_ids.append(id)
            c = next(iter(v.values())).coordinates[0]
            self.__coordinates.append((radians(c[1]), radians(c[0])))
        self.__tree = BallTree(self.__coordinates, metric="haversine")

    def find_next_node(self, coords: tuple[float, float]) -> int:
        _, id = self.__tree.query([[radians(coords[1]), radians(coords[0])]])
        return self.__node_ids[id[0][0]]


def node_to_coords(streets: StreetGraph, id: int) -> tuple[float, float]:
    return next(iter(streets[id].values())).coordinates[0]
