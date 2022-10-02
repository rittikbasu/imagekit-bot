import os
from imagekitio import ImageKit

imagekit = ImageKit(
    private_key=os.environ.get("PRIVATE_KEY","Key Not Found"),
    public_key=os.environ.get("PUBLIC_KEY","Key Not Found"),
    url_endpoint="https://ik.imagekit.io/zwcfsadeijm/",
)

def getImagekitURL(file_url, file_name):
    try:
        imagekit_data = imagekit.upload_file(
            file=file_url,  # required
            file_name=file_name,  # required
            options={
                "folder": "imagekit-bot-test",
                "use_unique_file_name": True,
            }
        )
        imagekit_url = imagekit_data["response"]["url"]
        file_id = imagekit_data["response"]["fileId"]
        size = imagekit_data["response"]["size"]
        if file_id == 'non-image':
            print('delete')
            imagekit.delete_file(file_id)
            return False
        return imagekit_url, file_id, size
    except Exception as e:
        print(e)
        return False