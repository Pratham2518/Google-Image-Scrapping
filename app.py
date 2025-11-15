from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import logging
import os

# Setup logging
logging.basicConfig(filename="scrapper.log", level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get user input
            query = request.form['content'].strip().replace(" ", "+")
            save_directory = "images/"

            # Create directory if not exists
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            # Fake header to mimic browser
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            }

            # Google Image search request
            url = f"https://www.google.com/search?q={query}&tbm=isch"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")

            # Find image tags
            image_tags = soup.find_all("img")
            if image_tags:
                del image_tags[0]  # Remove Google logo if exists

            image_urls = []
            for index, image_tag in enumerate(image_tags):
                image_url = image_tag.get('src')
                if image_url:
                    image_urls.append(image_url)
                    # Save image locally
                    image_data = requests.get(image_url).content
                    file_path = os.path.join(save_directory, f"{query}_{index}.jpg")
                    with open(file_path, "wb") as f:
                        f.write(image_data)

            # Pass data to result.html
            return render_template("result.html", query=query, images=image_urls)

        except Exception as e:
            logging.exception("Error while downloading images:")
            return f"Something went wrong: {str(e)}"

    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
