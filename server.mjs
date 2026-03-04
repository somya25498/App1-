import express from 'express';
import fetch from 'node-fetch';
import cors from 'cors';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
app.use(cors());
app.use(express.static(__dirname)); // Serve all files in Downloads folder

const API_KEY = "89de5e68472f0225ba881d3d01b68e22";

app.get('/forecast', async (req, res) => {
    const { lat, lon } = req.query;
    try {
        const url = `https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat=${lat}&lon=${lon}&appid=${API_KEY}`;
        const response = await fetch(url);
        const data = await response.json();
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch AQI' });
    }
});

app.get('/predict', (req, res) => {
    const { aqi, pm25 } = req.query;
    const python = spawn('python', ['predict_logic.py', aqi, pm25]);

    let dataString = '';
    python.stdout.on('data', (data) => {
        dataString += data.toString();
    });

    python.stdout.on('end', () => {
        try {
            const forecast = JSON.parse(dataString);
            res.json({ forecast });
        } catch (e) {
            res.status(500).json({ error: "AI output error" });
        }
    });
});

app.listen(3000, () => {
    console.log('Backend active on http://localhost:3000');
    console.log('Open http://localhost:3000/forecast.html in your browser');
});
