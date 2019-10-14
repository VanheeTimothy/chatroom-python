import uuid

class User():

    def __init__(self, name, nickname, email, password=None):
        self.Name = name
        self.nickname = nickname
        self.email = email
        self.password = password
        self.uniqueId = uuid.uuid4()

