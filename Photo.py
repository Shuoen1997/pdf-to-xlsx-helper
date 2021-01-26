class Photo(object):

    def __init__(self, filename, user):
        self.file_name = filename
        self.user = user

    def store(self):
        print("Stored")