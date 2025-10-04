#Создай собственный Шутер!

from pygame import *
mixer.init()
font.init()
from random import randint
import time as time_module

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_size_x, player_size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) #отрисовывает заново

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost #переменная в основном коде будет меняться
        if self.rect.y > 440:
            self.rect.x = randint(5, 595)
            self.rect.y = -15
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill() #удаляет объект из всех групп в которых он состоит

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 450:
            self.rect.x = randint(5, 595)
            self.rect.y = -15



            

window = display.set_mode((700, 500))
display.set_caption("Shooter")
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
game = True
lost = 0
score = 0
end = False
num_fire = 0
reload_time = False
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(5, 620), -15, randint(1,4), 70, 45)
    monsters.add(monster)
for i in range(2):
    asteroid = Asteroid('asteroid.png', randint(5, 620), randint(-75, -15), randint(3, 4), 75, 60)
    asteroids.add(asteroid)
mixer.music.load('space.ogg')
mixer.music.set_volume(0.3)
mixer.music.play()
shoot = mixer.Sound('fire.ogg')
shoot.set_volume(0.5)
rocket = Player('rocket.png', 320, 395, 9, 75, 100)
font1 = font.SysFont("Calibri", 36)
font2 = font.SysFont("Calibri", 52)
while game:
    for e in event.get():
        if e.type == QUIT: #если нажали на крестик
            game = False
        if e.type == KEYDOWN and e.key == K_SPACE: # if keydown если нажата какая-то клавиша
            if num_fire <= 5 and reload_time == False:
                shoot.play()
                rocket.fire() 
                num_fire += 1
            if num_fire > 5 and reload_time == False:
                reload_start = time_module.time()
                reload_time = True
            
    if end == False:
        window.blit(background,(0, 0))
        rocket.update()
        monsters.update()
        bullets.update() #движение пули
        asteroids.update()
        sprite_list = sprite.groupcollide(monsters, bullets, True, True) # список столкнувшихся монстров и пулей
        for i in sprite_list:
            monster = Enemy('ufo.png', randint(5, 620), -15, randint(1,4), 70, 45)
            monsters.add(monster)
            score += 1
        if reload_time == True:
            text_reload = font1.render('Reloading...', 1, (133, 16, 180))
            window.blit(text_reload, (300, 450))
            if time_module.time() - reload_start >= 1.5:
                reload_time = False
                num_fire = 0
        rocket.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text_win = font1.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text_win, (10, 20))
        if score >= 10: #ОСТАНОВИЛИСЬ ЗДЕСЬ
            end = True
            text_end_win = font2.render('YOU WIN', 1, (144, 255, 108))
            window.blit(text_end_win, (250, 200))
        if lost >= 5 or sprite.spritecollide(rocket, monsters, False) or sprite.spritecollide(rocket, asteroids, False):
            end = True
            text_end_lost = font2.render('GAME OVER', 1, (255, 72, 58))
            window.blit(text_end_lost, (250, 200))
    display.update()
    time.delay(50) #замедляет на 50 милисек




    

