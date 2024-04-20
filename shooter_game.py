#Створи власний Шутер!

from pygame import *
#import pygame
from random import randint
#pygame.init()
from time import time as timer



class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w,h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        win.blit(self.image, (self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self, ) -> None:
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < W-80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx-5, self.rect.y, 10,20,10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(80, W-160)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


bullets = sprite.Group()
rel_time = False
num_fire = 0


W,H = 700, 500
win = display.set_mode((W,H))
display.set_caption("Shooter game")
bg = transform.scale(image.load("galaxy.jpg"), (W,H))
max_enemy = 6
max_asteroid = max_enemy//3
max_lost = 3
goal = 10
lost = 0
life = 3

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound("fire.ogg")

font.init()
text1 = font.SysFont(None, 80)
text2 = font.SysFont(None, 36)

text_win = text1.render("YOU WIN!", 1, (0,255,0))
text_lose = text1.render("YOU LOSE!", 1, (255,0,0))


player = Player("rocket.png", W//2, H-100, 80, 100, 10)

asteroids = sprite.Group()
for i in range(max_asteroid):
    asteroid = Enemy('asteroid.png', randint(80, W-160), -60, 80, 50, randint(1,7))
    asteroids.add(asteroid)
monsters = sprite.Group()
for i in range(max_enemy):
    enemy = Enemy('ufo.png', randint(80, W-160), -60, 80, 50, randint(1,5))
    monsters.add(enemy)

game = True
clock = time.Clock()
FPS = 30
finish = False
score = 0
ammo = transform.scale(image.load('bullet.png'), (10, 20))
while game:
    x = 20
    y = H - 50
    for e in event.get():
        if e.type == QUIT:
            game = False
    if e.type == KEYDOWN:
        if e.key == K_SPACE:
            if num_fire < max_enemy//6*5 and rel_time == False:
                num_fire += 1
                player.fire()
                fire.play()
            if num_fire >= max_enemy//6*5 and rel_time == False:
                last_time = timer()
                rel_time = True
    if e.type == MOUSEBUTTONDOWN:
        if num_fire < max_enemy//6*5 and rel_time == False:
                num_fire += 1
                player.fire()
                fire.play()
        if num_fire >= max_enemy//3*2 and rel_time == False:
            last_time = timer()
            rel_time = True



    win.blit(bg, (0,0))
    if not finish:
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(win)
        bullets.update()
        bullets.draw(win)
        asteroids.update()
        asteroids.draw(win)


        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = text1.render('Wait for reloading...', 1, (150,0,0))
                win.blit(reload, (200, H-150))
            else:
                num_fire = 0
                rel_time = False

        for b in range(max_enemy//3*2-num_fire):
            win.blit(ammo, (x, y))
            x += 5

        text_lost = text2.render('Lost: '+str(lost), 1, (255,255,255),(40, 137, 67))
        text_score = text2.render('Score: '+str(score), 1, (255,255,255),(40, 137, 67))
        win.blit(text_score, (10,20))
        win.blit(text_lost, (10,50))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            enemy = Enemy("ufo.png", randint(80,W-160),
                          60, 80, 50, randint(1, 5))
            monsters.add(enemy)

        if (sprite.spritecollide(player, monsters, False)
        or sprite.spritecollide(player, asteroids, False)):
            sprite.spritecollide(player, asteroids, True)
            sprite.spritecollide(player, asteroids, True)
            life -= 1

        if lost >= max_lost or life <= 0:
            if max_enemy > 6:
                max_enemy -= 1
                goal -= 2
            finish = True
            win.blit(text_lose, (200, 200))

        if score >= goal:
            max_enemy += 1
            goal += 2
            life *= 2
            finish  = True
            win.blit(text_win, (200,200))

        if life >= 3:
            life_color = (0, 150, 0)
        elif life == 2:
            life_color = (150, 150, 0)
        elif life == 1:
            life_color = (150, 0, 0)
        else:
            life_color = (255, 0 ,0)

        text_life = text1.render(str(life), 1 , life_color)
        win.blit(text_life, (W-100, 20))

    else:
        finish = False
        time.delay(2000)
        for b in bullets:
            b.kill()

        for m in monsters:
            m.kill()
        for a in monsters:
            a.kill()

        score = 0
        lost = 0
        rel_time = False
        num_fire = 0
        life = 3

        for m in range(1,max_enemy):
            enemy = Enemy("ufo.png", randint(80, W-160),60, 80, 50, randint(1,5))
            monsters.add(enemy)

    display.update()
    clock.tick(FPS)




