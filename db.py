from replit import db

def writeToDB(key,image_link,file_size,file_id):
    if key in db.keys():
        db[key]["images"].append(image_link)
        db[key]["file_id"].append(file_id)
        db[key]["storageUsed"] += file_size
    else:
        db[key] = {"storageUsed": file_size, "images":[image_link], "file_id":[file_id], "paid":False}


def getUserData(key):
    storageTemplate = '<b>Storage Left:</b> '
    imagesTemplate = '<b>Images stored in imagekitBot</b>\n'
    if key in db.keys():
        storageUsed = db[key]["storageUsed"]
        if storageUsed > 0:
            storageUsed = 100 - round((storageUsed/1000000),2)
        images = db[key].get("images", None)
        allImages = ''
        if images:
            for index, image in enumerate(images):
                allImages += f'{index+1}) {image}\n\n'
            return f'{storageTemplate}{storageUsed}MB\n\n{imagesTemplate}{allImages}'
        else:
            allImages = 'None'
            return f'{storageTemplate}{storageUsed}MB\n\n{imagesTemplate}{allImages}'
    else:
        storageUsed = '100'
        allImages = 'None'
        return f'{storageTemplate}{storageUsed}MB\n\n{imagesTemplate}{allImages}'