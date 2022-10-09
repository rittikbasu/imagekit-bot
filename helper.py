from validators import url
from replit import db
from imagekit import getImagekitURL
from db import writeToDB

def checkFileSize(key, file_size):
    if key in db.keys():
        storageUsed = db[key]["storageUsed"] + file_size
    else:
        storageUsed = file_size
    if (storageUsed) > 100000000:
        return "You have exhausted your 100MB limit"
    elif file_size > 25000000:
        return "File size is too large"
    else:
        return storageUsed

def imagekitResponse(key, file_url, file_name, storageUsed, isUrl=False):
    imagekit_data = getImagekitURL(file_url, file_name)
    if imagekit_data:
        imagekit_url = imagekit_data[0]
        file_id = imagekit_data[1]
        if isUrl:
            size = imagekit_data[2]
            writeToDB(key=key, image_link=imagekit_url, file_size=size, file_id=file_id)
        else:
            writeToDB(key=key, image_link=imagekit_url, file_size=storageUsed, file_id=file_id)
        return imagekit_url
    else:
        return 'Only image files are supported.'

def processImageData(key, token, file_name, file_path, isUrl=False, file_size=0):
    print(file_size, file_name, file_path)
    if isUrl:
        storageUsed = checkFileSize(key=key, file_size=0)
        if type(storageUsed) != 'str':
            response = imagekitResponse(key=key, file_url=file_path, file_name=file_name, storageUsed=storageUsed, isUrl=True)
            return response
        else:
            return storageUsed
    else:
        storageUsed = checkFileSize(key, file_size)
        if type(storageUsed) != 'str':
            file_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
            response = imagekitResponse(key=key, file_url=file_url, file_name=file_name, storageUsed=storageUsed)
            return response
        else:
            return storageUsed


def is_url(string):
    valid=url(string)
    if valid == True:
        return True
    else:
        return False