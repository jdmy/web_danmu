class Danmu():
    def __init__(self, text, id, x, y):
        self.text = text
        self.id = id
        self.x = x
        self.y = y

    def move(self):
        self.x -= 5