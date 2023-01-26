import time as t
from pygame import *

class Dino(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rectY = 300
        self.rectX = 100
        self.image1 = transform.scale(image.load('run1.png'), (100, 75))
        self.image2 = transform.scale(image.load('run2.png'), (100, 75))
        self.jumpImg = transform.scale(image.load('jump.png'), (100, 75))
        self.height = 100
        self.width = 75
        self.last_update = time.get_ticks()
        self.speed = 10
        self.run = True
        self.hightJump = 200
        self.roadY = 300
        self.gr = True

    def dinoRun(self):
        if self.rectY == 300:
            now = time.get_ticks()
            if now - self.last_update > 100:
                window.blit(self.image1, (self.rectX,self.rectY))
                self.last_update = now
            else:
                window.blit(self.image2, (self.rectX,self.rectY))
                t.sleep(0.06)
    def jump(self):
        if self.rectY > 200:
            self.rectY -= 10
            if self.rectY == 200:
                self.gr = True
        window.blit(self.jumpImg, (self.rectX, self.rectY))

    def update(self):
        presseds = key.get_pressed()
        if presseds[K_UP] or presseds[K_SPACE]:
            self.jump()
            self.gr = False

    def gravitation(self):
        if self.gr and self.rectY <= self.roadY:
            self.rectY += 10

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
        dino.update()
        dino.gravitation()

        clock.tick(FPS)
        display.update()

if __name__ == '__main__':
    draw()
