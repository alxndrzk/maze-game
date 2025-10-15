from pygame import *

class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, x, y, width, height):
        sprite.Sprite.__init__ (self)
        self.image = image.load(player_image)
        self.image = transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__ (self, player_image, x, y, width, height, speed_x, speed_y):
        GameSprite.__init__(self, player_image=player_image, x=x, y=y, width=width, height=height)
        self.speed_x = speed_x
        self.speed_y = speed_y
    
    def update(self):
        if pacman.rect.x > 0 and pacman.speed_x < 0:
            self.rect.x += self.speed_x
            
        if pacman.rect.x < 700 - 80 and pacman.speed_x > 0:
            self.rect.x += self.speed_x
        

        platform_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_x > 0:
            for p in platform_touched:
                self.speed_x = 0
                if p.rect.left < self.rect.right:
                    self.rect.right = p.rect.left
        
        if self.speed_x < 0:
            for p in platform_touched:
                self.speed_x = 0
                if p.rect.right > self.rect.left:
                    self.rect.left = p.rect.right

        if pacman.rect.y > 0 and pacman.speed_y < 0:
            self.rect.y += self.speed_y
        
        if pacman.rect.y < 500 - 80 and pacman.speed_y > 0:
            self.rect.y += self.speed_y
        
        platform_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_y > 0:
            for p in platform_touched:
                self.speed_y = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        
        if self.speed_y < 0:
            for p in platform_touched:
                self.speed_y = 0
                if p.rect.bottom > self.rect.top:
                    self.rect.top = p.rect.bottom
        
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def __init__ (self, player_image, x, y, width, height, speed_x):
        GameSprite.__init__(self, player_image=player_image, x=x, y=y, width=width, height=height)
        self.speed = speed_x
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()

class Enemy(GameSprite):
    side = 'left'
    def __init__ (self, player_image, x, y, width, height, speed_x):
        GameSprite.__init__(self, player_image=player_image, x=x, y=y, width=width, height=height)
        self.speed = speed_x
    
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= win_width - 80:
            self.side = 'left'
        
        if self.side == 'left':
            self.rect.x -= self.speed
        if self.side == 'right':
            self.rect.x += self.speed

bg = (119, 210, 223)
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Game Maze')


pacman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
w1 = GameSprite('platform2.png', 116, 250, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)
final_sprite = GameSprite('pac-1.png', win_width - 85, win_height - 100, 80, 80)
barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)

bullets = sprite.Group()
monsters = sprite.Group()
monster1 = Enemy('cyborg.png', win_width - 80, 150, 80, 80, 5)
monster2 = Enemy('cyborg.png', win_width - 80, 250, 80, 80, 5)
monsters.add(monster1)
monsters.add(monster2)

run = True
finish = False

while run:
    time.delay(50)
    

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                pacman.speed_x = -5
            elif e.key == K_RIGHT:
                pacman.speed_x = 5
            elif e.key == K_UP:
                pacman.speed_y = -5
            elif e.key == K_DOWN:
                pacman.speed_y = 5
            elif e.key == K_SPACE:
                pacman.fire()
        
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                pacman.speed_x = 0
            elif e.key == K_RIGHT:
                pacman.speed_x = 0
            elif e.key == K_UP:
                pacman.speed_y = 0
            elif e.key == K_DOWN:
                pacman.speed_y = 0

    if not finish:
        window.fill(bg) #masukin warna background

        bullets.update()
        bullets.draw(window) 
        barriers.draw(window)
        monsters.update()
        monsters.draw(window)

        pacman.update() #pacman bergerak
        pacman.reset() #pacman muncul
        

        final_sprite.reset()

        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, monsters, True, True)

        if sprite.spritecollide(pacman, monsters, False):
            finish = True
            img = image.load('game-over_1.png')
            rasio = img.get_width() // img.get_height()
            window.fill((255, 255, 255)) #warna putih
            window.blit(transform.scale(img, (win_height * rasio, win_height)), (100,0))
       
        if sprite.collide_rect(pacman, final_sprite):
            finish = True
            window.fill((255, 255, 255)) #warna putih
            img = image.load('thumb.jpg')
            window.blit(transform.scale(img, (win_width, win_height)), (0,0))

    display.update()