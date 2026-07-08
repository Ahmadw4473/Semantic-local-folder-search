from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .services.GetEmbeddings import getImage, get_text_embedding
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryData(BaseModel):
    text: str

@app.post('/getImage')
def get_image_path(query: QueryData):
    queryEmbedding=get_text_embedding(query.text)
    return {"image": getImage(queryEmbedding)}

@app.get("/image")
def serve_image(path: str):
    return FileResponse(path)