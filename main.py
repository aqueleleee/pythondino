import time as t
from pygame import *
import random

font.init()
mixer.init()

class Ptero(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([280, 300])
        self.sprites = []
        self.sprites.append(
            transform.scale(
                image.load("assets\\Ptero1.png"), (84, 62)))
        self.sprites.append(
            transform.scale(
                image.load("assets\\Ptero2.png"), (84, 62)))
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]



class Cactus(sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = transform.scale(
                image.load(f"cacti/cactus{i}.png"), (100, 100))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def update(self):
        self.rect.x  -= game_speed

class Dino(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image1 = transform.scale(image.load('assets\\dino1.png'), (90, 120))
        self.image2 = transform.scale(image.load('assets\\dino2.png'), (90, 120))
        self.image3 = transform.scale(image.load('assets\\DinoDucking1.png'), (90, 60))
        self.image4 = transform.scale(image.load('assets\\DinoDucking2.png'), (90, 60))
        self.jumpImg = transform.scale(image.load('assets\\DinoJumping.png'), (90, 120))
        self.speed = 20
        self.speed_down = 10
        self.jumpCount = 30
        self.isJump = False
        self.foot = 1
        self.animCount = 0
        self.rect = self.image1.get_rect()
        self.rect.x = 100
        self.rect.y = 350


    def choose_foot(self, img1, img2, isduck=0):
        if self.animCount <= 10:
            self.foot = 1
            self.animCount +=1
        else:
            self.foot = 2
            self.animCount +=1
            if self.animCount == 20:
                self.animCount = 0

        if self.foot == 1:
            window.blit(img1, (self.rect.x, self.rect.y+isduck))
        else:
            window.blit(img2, (self.rect.x, self.rect.y+isduck))

    def run(self):
        presseds = key.get_pressed()
        if presseds[K_DOWN]:
            self.rect.y = 350
            self.isduck = True
            self.isJump = False
            self.choose_foot(self.image3, self.image4, 60)
        else:
            self.isduck = False
            if self.rect.y == 350:
                self.choose_foot(self.image1, self.image2)


    def jump(self):
        presseds = key.get_pressed()
        if (presseds[K_SPACE] or presseds[K_UP]) and self.isduck==False and self.rect.y == 350:
            self.isJump = True
            jump_sfx.play()

        if self.isJump :
            if self.jumpCount >= 0 and self.rect.y >= 100:
                self.rect.y -= self.speed
                self.jumpCount -= 1
            else:
                self.jumpCount = 30
                self.isJump = False
        elif self.rect.y <350 and self.isduck == False:
            self.rect.y += self.speed_down



clock = time.Clock()

window = display.set_mode((1100, 600))
FPS = 60

death_sfx = mixer.Sound("assets/sfx/lose.mp3")
points_sfx = mixer.Sound("assets/sfx/100points.mp3")
jump_sfx = mixer.Sound("assets/sfx/jump.mp3")

road_image = transform.scale(image.load('assets\\road.png'), (1100, 24))
road_x = 0
game_speed = 10
obstacle_spawn = False
obstacle_timer = 0
obstacle_cooldown = 2000
player_score = 0
player_score_max = 0
score_rect = (420, 310)

game_font = font.Font('assets\PressStart2P-Regular.ttf', 24)

sun = transform.scale(image.load('assets\\sun.png'), (100, 100))
cloud_group = sprite.Group()
obstacle_group = sprite.Group()
ptero_group =  sprite.Group()

dino = Dino()
game = True
finish = False

def end_game():
    global player_score
    global finish
    death_sfx.play()
    finish = True
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(530, 280))
    score_text = game_font.render(f"Score:{int(player_score)}", True, "black")
    window.blit(game_over_text, game_over_rect)
    window.blit(score_text, score_rect)
    player_score = 0
    cloud_group.empty()
    obstacle_group.empty()


if __name__ == '__main__':
    while game:
        for even in event.get():
            if even.type == QUIT:
                game = False
            if even.type == KEYDOWN:
                if even.key == K_SPACE:
                    finish = False


        if finish != True:
            window.fill((230, 230, 230))
            road_x -= game_speed
            window.blit(road_image, (road_x, 450))
            window.blit(road_image, (road_x + 1100, 450))
            if road_x <= -1100:
                road_x = 0

            window.blit(sun, (900, 100))

            player_score += 0.1
            if player_score - player_score_max >= 100:
                points_sfx.play()
                player_score_max = player_score
            player_score_surface = game_font.render(str(int(player_score)), True, ("black"))
            window.blit(player_score_surface, (900, 10))

            dino.run()
            dino.jump()
            if dino.rect.y != 350:
                window.blit(dino.image1, (dino.rect.x, dino.rect.y))

            if time.get_ticks() - obstacle_timer >= obstacle_cooldown:
                obstacle_spawn = True

            if obstacle_spawn:
                obstacle_random = random.randint(1, 50)
                if obstacle_random in range(1, 7):
                    new_obstacle = Cactus(1100, 380)
                    obstacle_group.add(new_obstacle)
                    obstacle_timer = time.get_ticks()
                    obstacle_spawn = False
                elif obstacle_random in range(7, 10):
                    new_obstacle = Ptero()
                    obstacle_group.add(new_obstacle)
                    obstacle_timer = time.get_ticks()
                    obstacle_spawn = False

            ptero_group.update()
            ptero_group.draw(window)

            obstacle_group.update()
            obstacle_group.draw(window)

            if sprite.spritecollide(dino, obstacle_group, False) or sprite.spritecollide(dino, ptero_group, False):
                finish = True
                death_sfx.play()
                end_game()

        clock.tick(FPS)
        display.update()

