from pathlib import Path

folder_path = Path.home() / "Pictures"

extensions = {".jpg", ".png", ".jpeg"}
images = []
for path in folder_path.rglob("*"):
    if path.is_file() and path.suffix.lower() in extensions:
        images.append(path)

print(images[:20])
