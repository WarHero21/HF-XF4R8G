import json

class Data(object):
    def __init__(self, image, description, filename, number_of_detection, username, date, id=-1):
        
        # The id of the image which is given by MongoDB.
        self.id = id

        # The image in a PIL format.
        self.image = image

        # The description of the image.
        self.description = description

        # The number of detected cars on the image.
        self.number_of_detection = number_of_detection

        # The user who uploaded the image.
        self.username = username

        # The upload date.
        self.date = date

        # The image's filename.
        self.filename = filename

    
    def to_db(self):
        return {
            'image': self.image,
            'description': self.description,
            'number_of_detection': self.number_of_detection,
            'username': self.username,
            'date': self.date,
            'filename': self.filename,
        }
    
    def to_cookie(self):
        value = json.dumps({
            'description': self.description,
            'number_of_detection': self.number_of_detection,
            'username': self.username,
            'date': self.date,
            'filename': self.filename,
        })

        return value

    @staticmethod
    def from_db(data):
        id = data["_id"]
        image = data["image"]
        description = data["description"]
        number_of_detection = data["number_of_detection"]
        username = data["username"]
        date = data["date"]
        filename = data["filename"]
        return Data(id=id, image=image, description=description, number_of_detection=number_of_detection, username=username, date=date, filename=filename)
    
    @staticmethod
    def from_cookie(cookie):
        value = json.loads(cookie)
        
        id = -1
        image = None
        description = value["description"]
        number_of_detection = value["number_of_detection"]
        username = value["username"]
        date = value["date"]
        filename = value["filename"]

        return Data(id=id, image=image, description=description, number_of_detection=number_of_detection, username=username, date=date, filename=filename)
