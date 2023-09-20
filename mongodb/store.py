import uuid

from PIL import Image
import io

from bson import ObjectId
from pymongo import MongoClient


def store(config, image_path):
    client = MongoClient(config.get("database", "mongodb_uri"))
    db = client[config.get("database", "db")]
    collection = db[config.get("database", "collection_image")]


    img = Image.open(image_path)
    img_byte_arr = io.BytesIO()

    img.save(img_byte_arr, format=img.format)
    img_byte_arr = img_byte_arr.getvalue()

    doc = {'image': img_byte_arr}

    # Step 4: Insert the document into the collection
    result = collection.insert_one(doc)

    client.close()

    print("Image stored successfully!", result.inserted_id)
    return result.inserted_id




def get(config, id):
    client = MongoClient(config.get("database", "mongodb_uri"))
    db = client[config.get("database", "db")]
    collection = db[config.get("database", "collection_image")]

    doc = collection.find_one({"_id": ObjectId(id)})
    if doc:
        img_byte_arr = doc['image']
        img = Image.open(io.BytesIO(img_byte_arr))

        img.show()

        random_file_capture_image_path = config.get('file', 'image_out_dir') + str(uuid.uuid4()) + '.png'

        with open(random_file_capture_image_path, "wb") as f:
            f.write(img_byte_arr)

        client.close()
        print(f"Image saved successfully! Location: {random_file_capture_image_path}")
    else:
        client.close()
        print(f"No document found with _id: {id}")
