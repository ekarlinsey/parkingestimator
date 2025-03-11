// Initialize the map
var map = L.map('map').setView([37.7749, -122.4194], 13); // Center on San Francisco
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Add Leaflet Draw for();
map.addLayer(drawnItems);
var drawControl = new L.Control.Draw({
    edit: { featureGroup: drawnItems },
    draw: { polygon: true }
});
map.addControl(drawControl);

// Handle polygon creation
map.on('draw:created', function (e) {
    var layer = e.layer;
    drawnItems.addLayer(layer);

    // Get polygon coordinates
    var polygonCoords = layer.toGeoJSON().geometry.coordinates[0].map(coord => [coord[1], coord[0]]);

    // Send the polygon to the backend
    fetch('/estimate_parking', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ polygon: polygonCoords })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `Estimated Parking Spaces: ${data.estimated_parking}`;
    })
    .catch(error => console.error('Error:', error));
});
