https://github.com/capjamesg/media-search/assets/37276661/e46621eb-5c15-4a51-9825-3d8da6a72dd2

# Media Search

A media search and cataloguing system built with CLIP.

## How it Works

This application allows you to find the image most similar to an image uploaded via a web page.

You can then map the image to which an upload is most similar to metadata. In the example video above, an image of the Reputation album is uploaded. Then, the most similar image from a catalog is found. Then, information about the album is returned. In the example, the album cover and a link to a YouTube video of the first song in the album is displayed.

This demonstrates how you can use CLIP to enable cataloging and image-based information retrieval.

## Getting Started

First, clone this project repository and install the required dependencies:

```bash
git clone https://github.com/capjamesg/media-search.git
cd media-search
pip install -r requirements.txt
```

Then, export your [Roboflow API key](https://docs.roboflow.com/api-reference/authentication#retrieve-an-api-key) into your environment:

```bash
export ROBOFLOW_API_KEY=""
```

Then, copy all images you want to be able to search into the `covers` folder. Next, open the `app.py` file and modify the `metadata` dictionary to include relevant metadata. Here is an example:

```json
metadata = {
    "Reputation": {"youtube": "wIft-t-MQuE", "image": "Reputation.jpg"},
    "Lover": {"youtube": "p1cEvNn88jM", "image": "Lover.jpg"},
    "1989": {"youtube": "JLYYYnzEYJI", "image": "1989.jpg"},
    "Midnights": {"youtube": "4l4mZ0i5WCU", "image": "Midnights.png"},
}
```

The keys are the file names without the extensions in the `covers` folder and the values in this example are the YouTube IDs to the first song in the album and the full file name for the image cover.

Finally, you can run the application with the following command:

```bash
python app.py
```

The application will run at `http://localhost:5000`.

## License

This project is licensed under an [MIT license](LICENSE).
