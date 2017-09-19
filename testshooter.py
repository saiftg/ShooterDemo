
import pygame
import random
# from Player import Player
# from Alien import Alien
# from Bullet import Bullet


WIDTH = 600
HEIGHT = 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AMERICA!!")
clock = pygame.time.Clock()
pygame.mixer.music.load('Flaming Soul Loop.ogg')
pygame.mixer.music.set_volume(0.5)
hit_fx = pygame.mixer.Sound('tribe_g.wav')

font_name = pygame.font.match_font('serif')



# def newAlien():
# 	x = Alien()
# 	all_sprites.add(x)
# 	aliens.add(x)


def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((60, 40))
		self.image = player_img
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0

	def update(self):
		self.speedx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -8
		if keystate[pygame.K_RIGHT]:
			self.speedx = 8
		self.rect.x += self.speedx
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		hit_fx.play()


class Alien(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((30, 40))
		self.image = alien_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 2)
		self.speedx = random.randrange(-3, 3)

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10, 20))
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10


	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

# class Explosion(pygame.sprite.Sprite):
# 	def __init__(self, center, size):
# 		pygame.sprite.Sprite.__init__(self)
# 		self.size = size
# 		self.image = explosions_anim[self.size][0]
# 		self.rect = self.image.get_rect()
# 		self.rect.center = center
# 		self.frame = 0
# 		self.last_update = pygame.time.get_ticks()
# 		self.frame_rate = 50

# 	def update(self):
# 		now = pygame.time.get_ticks()
# 		if now - self.last_update > self.frame_rate:
# 				self.last_update = now
# 				self.frame += 1
# 				if self.frame == len(explosion_anim[self.size]):
# 					 self.kill()
# 				else:
# 					 center = self.rect.center
# 					 self.image = explosion_anim[self.size][self.frame]
# 					 self.rect = self.image.get_rect()
# 					 self.rect.center = center



background_img = pygame.image.load('night.jpg')
background_rect = background_img.get_rect()
player_img = pygame.image.load('jim2.png')
alien_img = pygame.image.load('alien.png')
bullet_img = pygame.image.load('bullet.png')


# explosion_anim = {}
# for i in range(9):
# 	 filename = 'regularExplosion{}.png'.format(i)
# 	 img = pygame.image.load('regularExplosion00.png').convert()
# 	 img.set_colorkey(BLACK)



all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)



for i in range(8):
	x = Alien()
	all_sprites.add(x)
	Alien.add(x)
	
score = 0
# 	#newAlien()

pygame.mixer.music.play(loops=-1)

# Game loop
shootout = True
while shootout:
 
	clock.tick(FPS)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			shootout = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()

	
	all_sprites.update()

	hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
	for hit in hits:
		score += 10
		#exp =Explosion(hit.rect.center, 50 )
		n = Alien()
		all_sprites.add(n)
		#newAlien()
		aliens.add(n)

	hits = pygame.sprite.spritecollide(player, aliens, False)
	if hits:
		shootout = False

	screen.fill(BLACK)
	screen.blit(background_img, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 30, WIDTH / 2, 10)


	pygame.display.flip()

pygame.quit()