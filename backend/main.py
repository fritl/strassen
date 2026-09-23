from pathlib import Path
from load_streets import load_gpkg

G = load_gpkg(Path("./data/WichtigeStrassen.gpkg"), "wichtigestrassen")
print(len(G.keys()))
