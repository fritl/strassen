# Daten
Daten von des
[GIP](https://www.data.gv.at/datasets/3fefc838-791d-4dde-975b-a4131a54e7c5) (Graphenintegrations-Plattform)
über OGD (Open Goverment Data) heruntergeladen.

Der Datensatz umfasst alle Straßen inklusive Fuß- und Radwege sowie
Wanderrouten und Fußwege. Dadurch sind insgesamt ca. 2 000 000
Straßenabschnitte enthalten. Dijkstra in Python wäre dafur zu langsam. Daher
werden die Straßen auf folgende eingegränzt:

- Straßen Transnational
- Straßen Transregional
- Straßen Zentralörtlich
- Straßen Regional

Dadurch kommt man auf 132 499 Abschnitte was wahrscheinlich in absehbarer Zeit berechnet werden kann.

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
## Verwendete Technologien

- Python
    - [Fiona](https://pypi.org/project/fiona/) - Einlesen von geopackage dateien
    - [Folium](https://pypi.org/project/folium/) - Zeichnen von Karten

# Offene Fragen
- API Planung
- Frontend Planung (eingabe von Punkten / Orten, Anzeige einer Karte mit der Route
- Technische Details (welches Webframework, Code struktur, ...)

