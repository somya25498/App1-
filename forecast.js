document.addEventListener('DOMContentLoaded', async () => {
    const params = new URLSearchParams(window.location.search);
    const name = params.get('name') || 'Selected Location';
    const lat = params.get('lat');
    const lon = params.get('lon');

    const forecastContainer = document.getElementById('forecast');

    if (!lat || !lon) {
        forecastContainer.innerHTML = '<p style="padding:20px">❌ Location data missing.</p>';
        return;
    }

    try {
        // 1️⃣ Fetch current AQI data
        const res = await fetch(`http://localhost:3000/forecast?lat=${lat}&lon=${lon}`);
        const data = await res.json();

        if (!data.list || !data.list.length) {
            throw new Error('No AQI data received');
        }

        const aqi = data.list[0].main.aqi;
        const pm25 = data.list[0].components.pm2_5;

        // 2️⃣ Fetch AI Prediction
        const predictRes = await fetch(
            `http://localhost:3000/predict?aqi=${aqi}&pm25=${pm25}`
        );
        const predictData = await predictRes.json();

        // 3️⃣ Create Forecast Card
        const card = document.createElement('div');
        card.className = 'forecast-card';
        card.innerHTML = `
            <h3>${name}</h3>
            <div class="aqi">Current AQI: ${aqi}</div>
            <canvas id="aqiChart"></canvas>
        `;
        forecastContainer.appendChild(card);

        // 4️⃣ Render Chart
        const ctx = document.getElementById('aqiChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Day 1','Day 2','Day 3','Day 4','Day 5','Day 6','Day 7'],
                datasets: [{
                    label: 'Predicted AQI',
                    data: predictData.forecast,
                    borderColor: '#8f3f97',
                    backgroundColor: 'rgba(143,63,151,0.15)',
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: true }
                }
            }
        });

    } catch (error) {
        console.error(error);
        forecastContainer.innerHTML =
            '<p style="padding:20px">⚠️ Failed to load forecast data.</p>';
    }
});
const rankBtn = document.getElementById('rankBtn');

if (rankBtn) {
    rankBtn.addEventListener('click', () => {
        const params = new URLSearchParams(window.location.search);
        window.location.href = `rank.html?${params.toString()}`;
    });
}
