from decouple import config
from imagekitio import ImageKit

imagekit = ImageKit(
    private_key=config("PRIVATE_KEY"),
    public_key=config("PUBLIC_KEY"),
    url_endpoint=config("URL_ENDPOINT"),
)

# imagekit_url = imagekit.url(
#     {
#         "path": "/default-image.jpg",

#         "url_endpoint": config("URL_ENDPOINT"),
#         "transformation": [{"height": "1100", "width": "400", "format": "png", "e-grayscale": "true"}],
#     }
# )

# print(imagekit_url)


def getImagekitURL(file_url, file_name):
    imagekit_url = imagekit.upload_file(
        file=file_url,  # required
        file_name=file_name,  # required
        options={
            "folder": "imagekit-bot-test",
            "use_unique_file_name": True,
        }
    )

    return imagekit_url["response"]["url"]
