import './styles.css'
import "./reset.css"
import L from "leaflet"
import "leaflet/dist/leaflet.css"

var map = L.map('map').setView([47, 13], 8);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let start = L.marker([47.821983709487405, 13.0444997549057], { draggable: true, title: "Startpunkt" }).addTo(map)
let end = L.marker([48.18086191030826, 16.37550294399262], { draggable: true, title: "Zielpunkt" }).addTo(map)

function onMove(e) {
    start.setLatLng([47.821983709487405, 13.0444997549057])
    end.setLatLng([48.18086191030826, 16.37550294399262])
}

start.on("dragend", onMove)
end.on("dragend", onMove)
