import os
import pygame as pg
from random import randint
pg.init()

# Sprites
class Bird(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        bird_downflap = pg.transform.rotozoom(
            pg.image.load(
                os.path.join("game-objects", "yellowbird-downflap.png")
            ).convert_alpha(),
            0,
            1.5
        )
        bird_midflap = pg.transform.rotozoom(
            pg.image.load(
                os.path.join("game-objects", "yellowbird-midflap.png")
            ).convert_alpha(),
            0,
            1.5
        )       
        bird_upflap = pg.transform.rotozoom(
            pg.image.load(
                os.path.join("game-objects", "yellowbird-upflap.png")
            ).convert_alpha(),
            0,
            1.5
        ) 
        self.image_map = [bird_downflap, bird_midflap, bird_upflap]
        self.image_idx = 0
        self.gravity = 0
        self.image = self.image_map[self.image_idx].convert_alpha()
        self.rect = self.image.get_rect(midbottom = (50, 345))

    def update(self):
        self.animate()
        self.player_input()
        self.apply_gravity()

    def player_input(self): 
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]: self.gravity = -5

    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.y += int(self.gravity)
        if self.rect.bottom >= 578: self.rect.bottom = 578
    
    def animate(self):
        self.image_idx += 0.1
        if self.image_idx >= len(self.image_map): self.image_idx = 0
        self.image = self.image_map[int(self.image_idx)]

class Obstacle(pg.sprite.Sprite):
    def __init__(self, type, y_point):
        super().__init__()
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

# Constants
WINDOW_SIZE = (410, 690)
WIN = pg.display.set_mode(WINDOW_SIZE)
FPS = 60
CLOCK = pg.time.Clock()
PIPE_SPAWN_EVENT = pg.USEREVENT + 1
BACKGROUND = pg.transform.rotozoom(
    pg.image.load(
        os.path.join("game-objects", "background-day.png")
    )
    .convert(), 0, 1.5
)
GROUND = pg.transform.rotozoom(
    pg.image.load(
        os.path.join("game-objects", "base.png")
    )
    .convert(), 0, 1.5
)

# Variables
running = True
bird = pg.sprite.GroupSingle()
bird.add(Bird())
obstacles = pg.sprite.Group()

pg.display.set_caption("Flappy Bird")
pg.time.set_timer(PIPE_SPAWN_EVENT, 2800)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == PIPE_SPAWN_EVENT:
            y_point = randint(578, 738)
            obstacles.add(Obstacle("upper", y_point))
            obstacles.add(Obstacle("lower", y_point))
    
    WIN.blit(BACKGROUND, (0, 0))

    bird.draw(WIN)
    bird.update()

    obstacles.draw(WIN)
    obstacles.update()

    WIN.blit(GROUND, (0, 578))

    pg.display.update()
    CLOCK.tick(FPS)

pg.quit()