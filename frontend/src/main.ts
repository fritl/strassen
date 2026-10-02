import './styles.css'
import "./reset.css"
import L from "leaflet"
import "leaflet/dist/leaflet.css"
import startSvg from "./assets/icon_start.svg"
import endSvg from "./assets/icon_end.svg"

const button = document.querySelector<HTMLButtonElement>("#path_button");
button.disabled = true;
var map = L.map('map').setView([47, 13], 8);

let line;
const time_info = document.getElementById("time_info");

const start_icon = L.icon({
    iconUrl: startSvg,
    iconSize: [32, 32],
    iconAnchor: [16, 16]
})

const end_icon = L.icon({
    iconUrl: endSvg,
    iconSize: [32, 32],
    iconAnchor: [16, 32]
})

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const [[start_initial_lng, start_initial_lat], [end_initial_lng, end_initial_lat]] = await Promise.all([
    fetch(`/api/nearest_node?lat=${47.821983709487405}&lon=${13.0444997549057}`).then(res => res.json()),
    fetch(`/api/nearest_node?lat=${48.18086191030826}&lon=${16.37550294399262}`).then(res => res.json()),
])
let start = L.marker([start_initial_lat, start_initial_lng], { draggable: true, title: "Startpunkt", icon: start_icon }).addTo(map)
let end = L.marker([end_initial_lat, end_initial_lng], { draggable: true, title: "Zielpunkt", icon: end_icon }).addTo(map)
button.disabled = false;

async function onMove() {
    button.disabled = true;
    let end_coords = end.getLatLng();
    let start_coords = start.getLatLng();
    const start_req = fetch(`/api/nearest_node?lat=${start_coords.lat}&lon=${start_coords.lng}`).then((res) => res.json())
    const end_req = fetch(`/api/nearest_node?lat=${end_coords.lat}&lon=${end_coords.lng}`).then((res) => res.json())
    const [[start_lng, start_lat], [end_lng, end_lat]] = await Promise.all([start_req, end_req]);
    start.setLatLng([start_lat, start_lng])
    end.setLatLng([end_lat, end_lng])
    button.disabled = false;
}

function formatDuration(totalSeconds: number) {
    if (totalSeconds < 60) {
        return `${Math.round(totalSeconds)}s`;
    }

    const totalMinutes = Math.round(totalSeconds / 60);
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;

    return hours > 0 ? `${hours} Std. ${minutes} min.` : `${minutes} min.`;
}

async function showPath() {
    button.disabled = true;
    let end_coords = end.getLatLng();
    let start_coords = start.getLatLng();
    const [time, coords] = await fetch(`/api/route?start_lat=${start_coords.lat}&start_lng=${start_coords.lng}&end_lat=${end_coords.lat}&end_lng=${end_coords.lng}`).then(res => res.json())
    time_info.innerHTML = `Dauer: ${formatDuration(time)}`
    line?.remove();
    line = L.polyline(coords.map(([lng, lat]) => [lat, lng]), { color: "#002535" }).addTo(map);
    button.disabled = false;
}

button.addEventListener("click", showPath)

start.on("dragend", onMove)
end.on("dragend", onMove)
