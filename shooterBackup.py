import pygame
import random
from os import path

#img_dir = path.join(path.dirname(__file__), 'img')



WIDTH = 600
HEIGHT = 700
FPS = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AMERICA!!!!!!")
clock = pygame.time.Clock()
pygame.mixer.music.load('Flaming Soul Loop.ogg')
pygame.mixer.music.set_volume(0.5)
hit_fx = pygame.mixer.Sound('tribe_g.wav')

font_name = pygame.font.match_font('Comic Sans')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

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
		#self.image_orig = random.choice(monster_images)
		#self.image_orig.set_colorkey(BLACK)
		#self.image = self.image_orig.copy()
		self.image = alien_img
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 8)
		self.speedx = random.randrange(-3, 3)
		self.rot = 0
		self.rot_speed = random.randrange(-8, 8)
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
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()



background_img = pygame.image.load('night.jpg')
background_rect = background_img.get_rect()
player_img = pygame.image.load('jim2.png')
#player_img = pygame.image.load(path.join(img_dir, "jim2.png")).convert()
alien_img = pygame.image.load('alien.png')
bullet_img = pygame.image.load('bullet.png')

monster_images = []
monsters_list = ['alien.png', 'predator.png']
#for img in monsters_list:
	#monster_images.append(pygame.image.load(path.join(img_dir, img)).convert())

all_sprites = pygame.sprite.Group()
player = Player()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites.add(player)




for i in range(8):
	a = Alien()
	all_sprites.add(a)
	aliens.add(a)

score = 0
pygame.mixer.music.play(loops=-1)
running = True

while running:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()	
	
	all_sprites.update()

	
	hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
	for hit in hits:
		score += 25
		m = Alien()
		all_sprites.add(m)
		aliens.add(m)

	hits = pygame.sprite.spritecollide(player, aliens, False)
	if hits:
		running = False


	screen.fill(BLACK)
	screen.blit(background_img, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 18, WIDTH / 2, 35)

	pygame.display.flip()

pygame.quit()


