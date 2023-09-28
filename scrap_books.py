import subprocess
import tempfile

import cloudinary
from cloudinary.uploader import upload

# Credentials from a free cloudinary account
CLOUDINARY_CLOUD_NAME = "dt7vlqkfj"
CLOUDINARY_API_KEY = "244913289685442"
CLOUDINARY_API_SECRET = "X1fiH35aHxdG6ArP0xtIAYwH1Sc"


def get_scrapy_command(filename) -> str:
    return f"scrapy runspider gutenberg_spider.py -O {filename}"


def upload_to_cloudinary(filename: str) -> str | None:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
    )

    try:
        response = upload(filename, resource_type="raw")
        if "secure_url" in response:
            return response["secure_url"]
    except Exception as e:
        print("cloudinary error:", str(e))

    return None


if __name__ == "__main__":
    print("Scrapping books...")

    books_filename = tempfile.mktemp(prefix="gutenberg_", suffix=".json")
    command = get_scrapy_command(books_filename)

    try:
        subprocess.run(command, shell=True, universal_newlines=True)
        books_url = upload_to_cloudinary(books_filename)

        print("Books scrapped successfully!")
        print("Books temporary saved in", books_filename)

        if books_url is not None:
            print("Books saved in the url :", books_url)

    except subprocess.CalledProcessError as e:
        print("scrapy error:", e.returncode, e.output)
    except Exception as e:
        print("unexpected error:", str(e))
