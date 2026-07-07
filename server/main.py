from pathlib import Path
from transformers import pipeline

folder_path = Path.home() / "Pictures"

extensions = {".jpg", ".png", ".jpeg"}
images = []
for path in folder_path.rglob("*"):
    if path.is_file() and path.suffix.lower() in extensions:
        images.append(path)

print(images[:20])


pipe = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")
pipe(
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/hub/parrots.png",
    candidate_labels=["animals", "humans", "landscape"],
)
