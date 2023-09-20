import base64
import os
from io import BytesIO

import faiss
import numpy as np
import requests
from flask import Flask, render_template, request, send_from_directory
from PIL import Image

app = Flask(__name__)

INFERENCE_ENDPOINT = "https://infer.roboflow.com"
API_KEY = ""
DATASET_PATH = "./"

metadata = {
    "Reputation": {"youtube": "wIft-t-MQuE", "image": "Reputation.jpg"},
    "Lover": {"youtube": "p1cEvNn88jM", "image": "Lover.jpg"},
    "1989": {"youtube": "JLYYYnzEYJI", "image": "1989.jpg"},
    "Midnights": {"youtube": "4l4mZ0i5WCU", "image": "Midnights.png"},
}


def get_image_embedding(image: str) -> dict:
    image = image.convert("RGB")

    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    payload = {
        "body": API_KEY,
        "image": {"type": "base64", "value": image},
    }

    data = requests.post(
        INFERENCE_ENDPOINT + "/clip/embed_image?api_key=" + API_KEY, json=payload
    )

    response = data.json()

    embedding = response["embeddings"]

    return embedding


"""## Build the Search Index

Below, we build a search index using Roboflow Inference.
"""

index = faiss.IndexFlatL2(512)
file_names = []

TRAIN_IMAGES = os.path.join(DATASET_PATH, "covers")

for frame_name in os.listdir(TRAIN_IMAGES):
    try:
        frame = Image.open(os.path.join(TRAIN_IMAGES, frame_name))
    except IOError:
        print("error computing embedding for", frame_name)
        continue

    embedding = get_image_embedding(frame)

    index.add(np.array(embedding).astype(np.float32))

    file_names.append(frame_name)


@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = get_image_embedding(Image.open(request.files["file"].stream))

        D, I = index.search(np.array(query).astype(np.float32), 1)

        top_result = file_names[I[0][0]]

        album = top_result.split(".")[0]

        album_metadata = metadata.get(album, None)

        return render_template("index.html", album=album, album_metadata=album_metadata)

    return render_template("index.html")


@app.route("/covers/<path:path>")
def send_covers(path):
    return send_from_directory("covers", path)


if __name__ == "__main__":
    app.run(debug=True)
