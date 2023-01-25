import time as t
from pygame import *

class Dino(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image1 = transform.scale(image.load('run1.png'), (100, 75))
        self.image2 = transform.scale(image.load('run2.png'), (100, 75))
        self.height = 100
        self.width = 75
        self.last_update = time.get_ticks()
    def dinoRun(self):
        now = time.get_ticks()
        if now - self.last_update > 100:
            window.blit(self.image1, (100,300))
            self.last_update = now
        else:
            window.blit(self.image2, (100,300))
            t.sleep(0.06)


window = display.set_mode((700, 500))


FPS = 60
clock = time.Clock()


dino = Dino()

def draw():
    finish = False
    game = True
    while game:
        for even in event.get():
            if even.type == QUIT:
                game = False


        window.fill((255, 255, 255))
        dino.dinoRun()

        clock.tick(FPS)
        display.update()

if __name__ == '__main__':
    draw()
