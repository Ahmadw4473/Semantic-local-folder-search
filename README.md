# Semantic Folder Search

<img width="1681" height="910" alt="image" src="https://github.com/user-attachments/assets/3c6c0b43-cd1a-4bcf-8b40-dbfd489b89c8" />


A local semantic image search app built with React, FastAPI, CLIP embeddings, and ChromaDB.

The app scans images from your local Pictures folder, generates image embeddings using `openai/clip-vit-base-patch32`, stores them in ChromaDB, and lets you search images using natural language queries.

## Features

- Search local images using text prompts
- Generate image embeddings with CLIP
- Store embeddings in ChromaDB
- FastAPI backend for search and image serving
- React frontend for entering queries and viewing results

## Tech Stack

- React
- FastAPI
- Transformers
- PyTorch
- ChromaDB
- Pillow

## Setup

Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```powershell
pip install fastapi uvicorn transformers torch pillow chromadb
```

Install frontend dependencies:

```powershell
npm install
```

## Run Backend

```powershell
.\.venv\Scripts\python.exe -m uvicorn server.app:app --reload
```

FastAPI will run at:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Run Frontend

```powershell
npm start
```

React will run at:

```text
http://localhost:3000
```

## API

### Search Image

```http
POST /getImage
```

Request body:

```json
{
  "text": "query"
}
```

Response:

```json
{
  "image": "C:\\Users\\User\\Pictures\\example.jpg"
}
```

### Serve Image

```http
GET /image?path=...
```

Returns the actual image file so the frontend can display it.

## How It Works

1. Images are scanned from the local Pictures folder.
2. Each image is converted into a CLIP embedding.
3. Embeddings are stored in ChromaDB.
4. A search query is converted into a text embedding.
5. ChromaDB finds the most similar image embedding.
6. FastAPI returns the matching image path.
7. React displays the image through the backend `/image` endpoint.

## Notes

- The CLIP model may download on first run.
- The first backend startup can be slow because image embeddings are generated.
- ChromaDB data is stored locally.
- This app is intended for local development and learning.
