import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { imageUploadMiddleware } from './utils/imageUpload.js';
import { uploadImageController } from './controllers/image.controller.js';

import cors from "cors";

const app = express();

app.use(
cors({
origin: "http://localhost:5173", // your Vite dev URL
})
);


app.use(express.json({ limit: "2mb" }));


const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Body parsers (for normal JSON / form fields)
app.use(express.json());
app.use(express.urlencoded({ extended: true }));


// Static files
app.use(express.static(path.join(__dirname, 'public')));

// Existing test route
app.get('/backend', async (req, res) => {
  try {
    const response = await fetch('http://localhost:8000/try2');
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error fetching backend');
  }
});

// NEW: /uploading endpoint
// First: imageUploadMiddleware (multer) > adds req.file
// Then:  uploadImageController  > validates, converts, stores, responds
app.post('/upload', imageUploadMiddleware, uploadImageController);


export default app;
