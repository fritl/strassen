from dataclasses import dataclass
import fiona
from pathlib import Path


@dataclass(frozen=True)
class EdgeInfo:
    time: float
    coordinates: tuple[tuple[float, float], ...]


type StreetGraph = dict[int, set[tuple[int, EdgeInfo]]]


def load_gpkg(file: Path, layer: str) -> StreetGraph:
    with fiona.open(file, layer=layer) as src:
        G: StreetGraph = dict()

        def add_edge(
            from_node: int,
            to_node: int,
            length: float,
            speed: int,
            coordinates: tuple[tuple[float, float], ...],
        ):
            if G.get(from_node) is None:
                G[from_node] = set()
            G[from_node].add(
                (
                    to_node,
                    EdgeInfo(
                        3.6 / (speed * length),
                        tuple(coordinates),
                    ),
                )
            )

        for feat in src:
            geom = feat["geometry"]
            props = feat["properties"]

            coords: list[tuple[float, float]] = geom["coordinates"]
            from_node = props["node_from_short_id"]
            to_node = props["node_to_short_id"]
            length = props["length"]

            if length == 0:
                continue

            acces_tow = props.get("access_tow")
            if (
                (acces_tow is None and props["oneway_car"] == 1)
                or (acces_tow is not None and acces_tow & 4)
            ) and props["speed_tow_car"] != 0:
                add_edge(
                    from_node, to_node, length, props["speed_tow_car"], tuple(coords)
                )

            access_bkw = props.get("access_bkw")
            if (
                (access_bkw is None and props["oneway_car"] == 0)
                or (access_bkw is not None and access_bkw & 4)
            ) and props["speed_bkw_car"] != 0:
                coords.reverse()
                add_edge(
                    to_node, from_node, length, props["speed_bkw_car"], tuple(coords)
                )
    return G

