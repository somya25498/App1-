let map;
let searchMarker;

// AQI Color Helper
function getAQIColor(aqi) {
    if (aqi <= 50) return '#00e400';
    if (aqi <= 100) return '#ffff00';
    if (aqi <= 150) return '#ff7e00';
    if (aqi <= 200) return '#ff0000';
    if (aqi <= 300) return '#8f3f97';
    return '#7e0023';
}

document.addEventListener('DOMContentLoaded', () => {
    // Initialize map centered on Delhi
    map = L.map('map').setView([28.6139, 77.2090], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Click → Forecast
    map.on('click', (e) => {
        const { lat, lng } = e.latlng;
        goToForecast('Selected Location', lat, lng);
    });

    document.getElementById('searchBtn').addEventListener('click', searchLocation);
});

// Search Function
function searchLocation() {
    const query = document.getElementById('locationSearch').value.trim();
    if (!query) return;

    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}, Delhi, India`)
        .then(res => res.json())
        .then(data => {
            if (!data.length) return alert('Location not found');

            const place = data[0];
            const lat = +place.lat;
            const lon = +place.lon;

            map.flyTo([lat, lon], 15);

            if (searchMarker) map.removeLayer(searchMarker);

            searchMarker = L.marker([lat, lon]).addTo(map)
                .bindPopup(`
                    <b>${place.display_name}</b><br><br>
                    <button onclick="goToForecast('${place.display_name}', ${lat}, ${lon})">
                        View 7-Day AI Forecast
                    </button>
                `)
                .openPopup();
        });
}

// Redirect to forecast page
function goToForecast(name, lat, lon) {
    window.location.href = `forecast.html?name=${encodeURIComponent(name)}&lat=${lat}&lon=${lon}`;
}
