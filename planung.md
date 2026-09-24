# Daten
Daten von des
[GIP](https://www.data.gv.at/datasets/3fefc838-791d-4dde-975b-a4131a54e7c5) (Graphenintegrations-Plattform)
über OGD (Open Goverment Data) heruntergeladen.

Der Datensatz umfasst alle Straßen inklusive Fuß- und Radwege sowie
Wanderrouten und Fußwege. Nur Straßen die mit dem Auto befahren werden können sind relevant. Zur filterung wird die edge_category verwendet. Dabei werden folgende Kategorien gefiltert:
- A
- B
- BS
- G
- GI
- GS
- GW
- H
- I
- IO
- KR
- L
- LD
- LR
- LS
- P
- PO
- R
- S
- SD
- SS
- SW
- VS

Die genaue bedeutung dieser Buchstaben kann in der Datensatzbeschreibung nachgelesen werden.

Weiters sind folgende daten von den Straßen wichtig:
- Coordinates
- Oneway Car
- Speed Tow Car
- Speed Bkw Car
- Length
- Node from id
- Node to id
Dabei wird speed und length verwendet um die Gewichte des Graphens zu bestimmen

# Konzeptionelle Planung
Die Daten werden in Python eingelesen und als Graph dargestellt. Eine Webanwendung kann über eine API den kürzesten Weg zwischen zwei Punkten bekommen.

# Technische Planung

- Python
    - [Fiona](https://pypi.org/project/fiona/) - Einlesen von geopackage dateien
    - [Folium](https://pypi.org/project/folium/) - Zeichnen von Karten
    - [pyproj](https://pyproj4.github.io/pyproj/stable/) - Berechnen der Distanz zwischen zwei Koordinaten

# Offene Fragen
- API Planung
- Frontend Planung (eingabe von Punkten / Orten, Anzeige einer Karte mit der Route
- Technische Details (welches Webframework, Code struktur, ...)

