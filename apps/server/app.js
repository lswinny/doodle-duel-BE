import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const app = express();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(express.static(path.join(__dirname, 'public')));

app.get('/backend', async (req, res) => {
  try {
    const response = await fetch('http://localhost:8000/try2');

    // If the backend returns JSON
    const data = await response.json();
    res.json(data);

    // OR if it returns plain text
    // const text = await response.text();
    // res.send(text);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error fetching backend');
  }
});

export default app;
