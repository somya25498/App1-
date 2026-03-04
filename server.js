import express from 'express';
import fetch from 'node-fetch';
import cors from 'cors';

const app = express();
app.use(cors());

const API_KEY ="89de5e68472f0225ba881d3d01b68e22";

app.get('/forecast', async (req, res) => {
    const { lat, lon } = req.query;

    if (!lat || !lon) {
        return res.status(400).json({ error: 'Missing coordinates' });
    }

    try {
        const url = `https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat=${lat}&lon=${lon}&appid=${API_KEY}`;
        const response = await fetch(url);
        const data = await response.json();

        res.json(data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch AQI data' });
    }
});

app.listen(3000, () => {
    console.log('Backend running on http://localhost:3000');
});