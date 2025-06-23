class Obstacle(pg.sprite.Sprite):
    def __init__(self, type, y_point):
        super().__init__()
        self.passed = False
        if type == 'lower':
            self.image = pg.image.load(os.path.join("game-objects", "pipe-green.png")).convert_alpha()
            self.rect = self.image.get_rect(midbottom = (510, y_point))
        else:
            self.image = pg.transform.rotate(
                pg.image.load(os.path.join("game-objects", "pipe-green.png")).convert_alpha(),
                180
            )
            self.rect = self.image.get_rect(midbottom = (510, y_point - 450))

    def update(self):
        self.rect.x -= 2
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100: self.kill()