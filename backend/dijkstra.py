import heapq
import math

from streets import StreetGraph


def dijkstra(
    streets: StreetGraph, start: int, end: int
) -> tuple[float, list[tuple[float, float]]]:
    visited = {start}
    prev: dict[int, int] = {}
    weights: dict[int, float] = {start: 0}
    to_visit: list[tuple[float, int]] = [(0.0, start)]
    while len(to_visit) > 0:
        (weight, cur) = heapq.heappop(to_visit)
        visited.add(cur)
        if cur == end:
            break
        if streets.get(cur) is None:
            continue
        for neighbour_id, info in streets[cur].items():
            if neighbour_id in visited:
                continue
            new_time = info.time + weight
            if new_time < weights.get(neighbour_id, math.inf):
                weights[neighbour_id] = new_time
                prev[neighbour_id] = cur
                heapq.heappush(to_visit, (new_time, neighbour_id))
    if end not in visited:
        raise ValueError("End unreachable")

    path: list[tuple[float, float]] = []
    cur = end
    while cur != start:
        prev_node = prev[cur]
        path[:0] = streets[prev_node][cur].coordinates
        cur = prev_node
    print(f"Dist: {weights[end]}s")
    return (weights[end], path)
