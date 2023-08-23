import arcade

class Car(arcade.Sprite):
    def __init__(self, image, scale, x, y):
        super().__init__(image, scale)
        self.center_x = x
        self.center_y = y
        self.speed = 5
        self.change_x = 0

class Enemy(arcade.Sprite):
    def __init__(self, image, scale, x, y):
        super().__init__(image, scale)
        self.center_x = x
        self.center_y = y
        self.speed = 7
        self.damage = 10

    def update(self):
        self.center_y -= self.speed
