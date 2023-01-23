from pygame import *

class Dino(sprite.Sprite):
    def __init__(self):
        super().__init__()
        
window = display.set_mode((700, 500))

background = transform.scale(image.load('background.jpg'), (700, 500))






FPS = 30
clock = time.Clock()

game = True
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
    window.blit(background, (0, 0))



    clock.tick(FPS)
    display.update()
