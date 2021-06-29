import random

class Generator:
    def __init__(self, x,y, objects):
        self.x = x
        self.y = y
        self.objects = objects
        self.final = []
    def generate(self):
        self.final = []
        for i in range(self.y):
            row = []
            for i in range(self.x):
                row.append(random.choice(self.objects))
            self.final.append(row)
        return self.final    