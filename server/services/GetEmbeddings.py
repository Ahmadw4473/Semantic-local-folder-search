from pathlib import Path
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import chromadb

chroma_client = chromadb.PersistentClient(path="./server/chroma_db")
collection = chroma_client.get_or_create_collection(
    name="image_embeddings",
    metadata={"hnsw:space": "cosine"},
)

folder_path = Path.home() / "Pictures"

extensions = {".jpg", ".png", ".jpeg"}
images = []
for path in folder_path.rglob("*"):
    if path.is_file() and path.suffix.lower() in extensions:
        images.append(path)

print(images[:20])

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def normalize_embedding(model_output):
    embedding = getattr(model_output, "pooler_output", model_output)
    return embedding / embedding.norm(dim=-1, keepdim=True)


def tensor_to_vector(embedding):
    return embedding.squeeze(0).cpu().tolist()


def get_image_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    image_inputs = processor(images=image, return_tensors="pt")

    with torch.inference_mode():
        return normalize_embedding(model.get_image_features(**image_inputs))


def get_text_embedding(text):
    text_inputs = processor(text=[text], return_tensors="pt", padding=True)

    with torch.inference_mode():
        return normalize_embedding(model.get_text_features(**text_inputs))


for image_path in images:
    image_embedding = get_image_embedding(image_path)

    collection.upsert(
        ids=[str(image_path)],
        embeddings=[tensor_to_vector(image_embedding)],
        metadatas=[{"path": str(image_path)}],
        documents=[str(image_path)],
    )

# text_embedding = get_text_embedding(query)

def getImage(text_embedding):
    search_results = collection.query(
        query_embeddings=[tensor_to_vector(text_embedding)],
        n_results=1
    )

    if search_results["ids"] and search_results["ids"][0]:
        return search_results["ids"][0][0]

    return None
