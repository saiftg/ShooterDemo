import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')



WIDTH = 600
HEIGHT = 700
FPS = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MUCH EXPLOSIONS!!!!")
clock = pygame.time.Clock()
pygame.mixer.music.load('Flaming Soul Loop.ogg')
pygame.mixer.music.set_volume(0.5)
hit_fx = pygame.mixer.Sound('tribe_g.wav')
win_fx = pygame.mixer.Sound('outstand.wav')
lose_fx = pygame.mixer.Sound('kahn.wav')
death_fx = pygame.mixer.Sound('playerDeath.wav')



font_name = pygame.font.match_font('Comic Sans')


def intro():
	smallfont = pygame.font.SysFont(None, 30)
	while intro == True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				intro = False
		gameDisplay.fill(white)
		text = smallfont.render("press any key to continue",True , (0, 0, 0))
		gameDisplay.blit(text, [320,240])
		pygame.display.update()
		clock.tick(15)


def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

def newAlien():
	m = Alien()
	all_sprites.add(m)
	aliens.add(m)


class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50, 40))
		self.image = player_img
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0

	def update(self):
		self.rect.x += self.speedx
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -4
		if keystate[pygame.K_RIGHT]:
			self.speedx = 4
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
		self.image_orig = random.choice(monster_images)
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()
		#self.image = alien_img
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 4)
		self.speedx = random.randrange(-3, 3)
		self.last_update = pygame.time.get_ticks()

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
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()


class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		pygame.sprite.Sprite.__init__(self)
		#self.size = size
		self.image = explosion_img_a[0]
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_img_a):
				self.kill()

			elif self.frame == len(explosion_img_p):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_img_a[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center



background_img = pygame.image.load('night.jpg')
background_rect = background_img.get_rect()
#player_img = pygame.image.load('jim2.png')
player_img = pygame.image.load(path.join(img_dir, "jim2.png")).convert()
#alien_img = pygame.image.load('alien.png')
bullet_img = pygame.image.load('bullet.png')

monster_images = []
monsters_list = ['alien.png', 'predator.png']
for img in monsters_list:
	monster_images.append(pygame.image.load(path.join(img_dir, img)).convert())

explosion_img_a = []
explosion_list_a = ['regularExplosion00.png', 'regularExplosion01.png', 'regularExplosion02.png',
					'regularExplosion03.png', 'regularExplosion04.png', 'regularExplosion05.png',
					'regularExplosion06.png', 'regularExplosion07.png', 'regularExplosion08.png']
for img in explosion_list_a:
	explosion_img_a.append(pygame.image.load(path.join(img_dir, img)).convert())


explosion_img_p = []
explosion_list_p = ['Death.png', 'skeleton.png']
for img in explosion_list_p:
	explosion_img_p.append(pygame.image.load(path.join(img_dir, img)).convert())


all_sprites = pygame.sprite.Group()
player = Player()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites.add(player)




for i in range(6):
	newAlien()


score = 0
pygame.mixer.music.play()

running = True
game_on = True



while running:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()	
	
	if game_on:
		all_sprites.update()

	
	hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
	for hit in hits:
		death_fx.play()
		score += 25
		x = Explosion(hit.rect.center)
		if game_on:
			all_sprites.add(x)
			newAlien()

	hits = pygame.sprite.spritecollide(player, aliens, False)
	for hit in hits:
		x = Explosion(hit.rect.center)
		all_sprites.add(x)
		newAlien()
	if hits:
		deathplosion = Explosion(player.rect.center)
		all_sprites.add(deathplosion)
		player.kill()
		#death_fx.play()

	if not player.alive() and not deathplosion.alive():
		if game_on == True:
			lose_fx.play()
		game_on = False
		background_img = pygame.image.load('kahn.png')
		all_sprites = pygame.sprite.Group()
		


	if score == 1000:
		if game_on == True:
			win_fx.play()

		game_on = False
		background_img = pygame.image.load('myhero.jpg')
		all_sprites = pygame.sprite.Group()


	
	screen.fill(BLACK)
	screen.blit(background_img, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 18, WIDTH / 2, 45)

	pygame.display.flip()


pygame.quit()


