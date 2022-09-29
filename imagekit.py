import os
from imagekitio import ImageKit

imagekit = ImageKit(
    private_key=os.environ.get("PRIVATE_KEY","Key Not Found"),
    public_key=os.environ.get("PUBLIC_KEY","Key Not Found"),
    url_endpoint="https://ik.imagekit.io/zwcfsadeijm/",
)

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