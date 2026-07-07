from pathlib import Path
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

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

query = "snow"

text_inputs = processor(text=[query], return_tensors="pt", padding=True)

with torch.inference_mode():
    text_embedding = normalize_embedding(model.get_text_features(**text_inputs))

results = []

for image_path in images:
    image = Image.open(image_path).convert("RGB")
    image_inputs = processor(images=image, return_tensors="pt")

    with torch.inference_mode():
        image_embedding = normalize_embedding(model.get_image_features(**image_inputs))

    score = (text_embedding @ image_embedding.T).item()
    results.append((score, image_path))

results.sort(reverse=True)


if results:
    print(results[0])
else:
    print(f"No images found in {folder_path}")
