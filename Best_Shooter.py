import pygame
import random
import os 
import math
from pygame.locals import *
#Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
#art by cristi because he's a gud guy
width=600
height=600
fps=60
pygame.init()
pygame.mixer.init()
screen =pygame.display.set_mode((width,height))
pygame.display.set_caption("Game")
clock=pygame.time.Clock()
black=(0,0,0)
blue=(0,0,255)
white=(255,255,255)
red=(255,0,0)
yellow=(255,255,0)
purple=(200,0,255)
bulletwidth=10
bulletspeed=15
bulletspread=2
dead=0
won=0
rsp=1
delay=1
bosshealth=2000
spreadnice=0
lives=2
ik=1
k=0
rsp1=10
rsp2=-10
touchboss=0
bossgoright=0
power=30
bossdelay=0

font = pygame.font.SysFont("comicsansms", 50)
dead_text = font.render("you died",True,white)
won_text=font.render("gg",True,white)
class Player(pygame.sprite.Sprite):
	def __init__(self):
		global lives
		pygame.sprite.Sprite.__init__(self)
		self.image=playerimg
		self.image.set_colorkey(white)
		self.rect=self.image.get_rect()
		self.radius=5
		self.rect.centerx=width/2
		self.rect.bottom=height-30
		self.speedx=0
		self.speedy=0
		self.shield=100
	def update(self):
		self.speedx=0
		self.speedy=0
		speed=6
		global k,delay
		keystate=pygame.key.get_pressed()
		if keystate[pygame.K_z]:
			speed=3
		if keystate[pygame.K_LEFT]:
			self.speedx=-speed
		if keystate[pygame.K_RIGHT]:
			self.speedx=speed
		if keystate[pygame.K_UP]:
			self.speedy=-speed
		if keystate[pygame.K_DOWN]:
			self.speedy=speed

		if keystate[pygame.K_SPACE]:
			if k%delay==0:
				self.shoot()
			k+=1
		else:
			k=0		
		self.rect.x+=self.speedx
		self.rect.y+=self.speedy
		if self.rect.right>width:
			self.rect.right=width
		if self.rect.top<0:
			self.rect.top=0
		if self.rect.bottom>height:
			self.rect.bottom=height
		if self.rect.left<0:
			self.rect.left=0
	def shoot(self):
		pos = pygame.mouse.get_pos()
		mouse_x = pos[0]
		mouse_y = pos[1]
		bullet = Bullet(self.rect.x,self.rect.y, mouse_x, mouse_y)
		all_sprites.add(bullet)
		bullets.add(bullet)
class hp(pygame.sprite.Sprite):
	def __init__(self,center,size):
		pygame.sprite.Sprite.__init__(self)
		self.size=size
		self.image=bubbles[self.size]
		self.image.set_colorkey(white)
		self.rect=self.image.get_rect()
		self.rect.center=center
	def update(self):
		self.speedx=0
		self.speedy=0
		speed=6
		keystate=pygame.key.get_pressed()
		if keystate[pygame.K_z]:
			speed=3
		if keystate[pygame.K_LEFT]:
			self.speedx=-speed
		if keystate[pygame.K_RIGHT]:
			self.speedx=speed
		if keystate[pygame.K_UP]:
			self.speedy=-speed
		if keystate[pygame.K_DOWN]:
			self.speedy=speed
		self.rect.x+=self.speedx
		self.rect.y+=self.speedy
class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.imageo=enemyimg
		self.imageo.set_colorkey(white)
		self.image=self.imageo.copy()
		self.radius=10
		self.rect=self.image.get_rect()
		self.rect.x=random.randrange(30,width-30)
		self.rect.y=random.randrange(-600,-30)
		self.speedy=random.randrange(2,4)
		self.spinpos=0
		self.spinspeed=random.randrange(-8,8)
		self.rotation=pygame.time.get_ticks()
		
	#def rotate(self):
	#	now=pygame.time.get_ticks()
	#	if now-self.rotation>50:
	#		self.rotation=now
	#		self.spinpos=(self.spinpos+self.spinspeed)%360
	#		newimage=pygame.transform.rotate(self.imageo,self.spinpos)
	#		oldcenter=self.rect.center
	#		self.image=newimage
	#		self.rect=self.image.get_rect()
	#		self.rect.center=oldcenter
	def update(self):
		#self.rotate()
		self.rect.y+=self.speedy
		if self.rect.top>height:	
			self.rect.x=random.randrange(30,width-30)
			self.rect.y=random.randrange(-600,-30)
			self.speedy=random.randrange(2,4)
class Bullet(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y, dest_x, dest_y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([4, 10])
		self.image.fill(black)
		self.rect = self.image.get_rect()
		self.rect.x = start_x
		self.rect.y = start_y
		self.floating_point_x = start_x
		self.floating_point_y = start_y
		x_diff = dest_x - start_x
		y_diff = dest_y - start_y
		angle = math.atan2(y_diff, x_diff);
		self.change_x = math.cos(angle) * 10
		self.change_y = math.sin(angle) * 10
	def update(self):
		self.floating_point_y += self.change_y
		self.floating_point_x += self.change_x
		self.rect.y = int(self.floating_point_y)
		self.rect.x = int(self.floating_point_x)
		if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
			self.kill()
class Boss(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load('alienboss.png')
		self.image.set_colorkey(black)
		self.radius=30
		self.rect=self.image.get_rect()
		self.rect.centerx=width/2
		self.rect.top=10
	def update(self):
		speed=2
		global bossgoright,bossdelay
		if not bossgoright:
			self.rect.centerx-=speed
			if self.rect.x<20:
				bossgoright=1
		else:
			self.rect.x+=speed
			if self.rect.centerx>width-40:
				bossgoright=0
		if bossdelay%30==0:
			self.shoot()
			bossdelay=0
		bossdelay+=1
	def shoot(self):
		bossbullet=Enemybullet(self.rect.center,self.rect.bottom)
		all_sprites.add(bossbullet)
		bossbullets.add(bossbullet)
class Enemybullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=bbsprite
		self.image.set_colorkey(white)
		self.rect=self.image.get_rect()
		self.rect.top=y
		self.rect.center=x
		self.speedy=4
	def update(self):
		self.rect.y+=self.speedy
		if self.rect.bottom<0:
			self.kill()
class Explosion(pygame.sprite.Sprite):
	def __init__(self,center,size):
		pygame.sprite.Sprite.__init__(self)
		self.size=size
		self.image=explosionanimation[self.size][0]
		self.rect=self.image.get_rect()
		self.rect.center=center
		self.frame=0
		self.lastupdate=pygame.time.get_ticks()
		self.framerate=60
	def update(self):
		now=pygame.time.get_ticks()
		if now-self.lastupdate>self.framerate:
			self.lastupdate=now
			self.frame+=1
			if self.frame==len(explosionanimation[self.size]):
				self.kill()
			else:
				center=self.rect.center
				self.image=explosionanimation[self.size][self.frame]
				self.rect=self.image.get_rect()
				self.rect.center=center
def spawn():
	m=Mob()
	all_sprites.add(m)
	mobs.add(m)
class Powerup(pygame.sprite.Sprite):
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load('powerupp.png')
		self.rect=self.image.get_rect()
		self.rect.center=center
		self.speedy=5
		self.radius=10
	def update(self):
		self.rect.y+=self.speedy
		if self.rect.top>height:
			self.kill()

bbsprite=pygame.image.load('bossbulletsprite.png')
background=pygame.image.load('starfield.png')
playerimg=pygame.image.load('ship.png')
iplayerimg=pygame.image.load('shipifr.png')
enemyimg=pygame.image.load('alien.png')
laser=pygame.image.load('laser.png')
left=pygame.image.load('left.png')
right=pygame.image.load('right.png')
backgroundrect= background.get_rect()
pew=pygame.mixer.Sound('shoot.wav')
gothit=pygame.mixer.Sound('gothit.wav')
pygame.mixer.music.load('tgfcoder-FrozenJam-SeamlessLoop.ogg')
pygame.mixer.music.set_volume(0.4)
explosionanimation={}
explosionanimation['regexp']=[]
explosionanimation['playerexp']=[]
bubble3=pygame.image.load('Bubble3.png')
bubble2=pygame.image.load('Bubble2.png')
bubble1=pygame.image.load('Bubble1.png')
bubbles=[bubble1,bubble2,bubble3]
pew=pygame.mixer.Sound('Laser_Shoot16.wav')
for i in range(9):
	forregular='regularExplosion0{}.png'.format(i)
	regularimg=pygame.image.load(forregular)
	regularimg.set_colorkey(black)
	special='sonicExplosion0{}.png'.format(i)
	spimg=pygame.image.load(special)
	spimg.set_colorkey(black)
	imgreg=pygame.transform.scale(regularimg,(35,35))
	explosionanimation['regexp'].append(imgreg)
	imgsp=pygame.transform.scale(spimg,(150,150))
	explosionanimation['playerexp'].append(imgsp)
bossbullets=pygame.sprite.Group()
all_sprites=pygame.sprite.Group()
mobs=pygame.sprite.Group()
bullets=pygame.sprite.Group()
pwrups=pygame.sprite.Group()
boss=Boss()
player=Player()
all_sprites.add(player)
all_sprites.add(boss)
yourhp=hp(player.rect.center,lives)
all_sprites.add(yourhp)
for i in range(50):
	spawn()
running=True
pygame.mixer.music.play(loops=-1)
while running:
	#keep loop running
	clock.tick(fps)
	yourhp.rect.center=player.rect.center
	#input
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running=False
	#update
	all_sprites.update()
	#collision
	hit=pygame.sprite.collide_circle(player,boss)
	if hit and not touchboss:
		dexpl=Explosion(player.rect.center,'playerexp')
		all_sprites.add(dexpl)
		player.kill()
		yourhp.kill()
		touchboss=1
		lives=-1
	hits=pygame.sprite.spritecollide(player,bossbullets,True,pygame.sprite.collide_circle)
	for hit in hits:
		player.shield-=20
		expl=Explosion(hit.rect.center,'regexp')
		all_sprites.add(expl)
		gothit.play()
		spawn()
	hits=pygame.sprite.groupcollide(mobs,bullets,True,True)
	for hit in hits:
		expl=Explosion(hit.rect.center,'regexp')
		all_sprites.add(expl)
		if power <=20:
			chance=random.randrange(1,100)
			if chance<15:
				pup=Powerup(hit.rect.center)
				pwrups.add(pup)
				all_sprites.add(pup)
		spawn()
	pickedup=pygame.sprite.spritecollide(player,pwrups,True,pygame.sprite.collide_circle)
	for yay in pickedup:
		power+=1
	hits=pygame.sprite.spritecollide(boss,bullets,True,pygame.sprite.collide_circle)
	for hit in hits:
		bosshealth-=1
		expl=Explosion(hit.rect.center,'regexp')
		all_sprites.add(expl)
	if bosshealth<0:
		running=False
		won=1
	hits=pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
	for hit in hits:
		player.shield-=40
		expl=Explosion(hit.rect.center,'regexp')
		all_sprites.add(expl)
		gothit.play()
		spawn()
	if player.shield<=0:
		dexpl=Explosion(hit.rect.center,'playerexp')
		all_sprites.add(dexpl)
		if lives<0:
			yourhp.kill()
			player.kill()
			dexpl=Explosion(hit.rect.center,'playerexp')
			all_sprites.add(dexpl)
		else:
			lives=lives-1
			yourhp.kill()
			if lives>=0:
				yourhp=hp(player.rect.center,lives)
				all_sprites.add(yourhp)
			player.shield=100
	if lives<0 and not dexpl.alive():
		running=False
		dead=1
	#draw/render
	screen.fill(black)
	screen.blit(background,backgroundrect)
	all_sprites.draw(screen)
	boss_hp_text=font.render(str(bosshealth),True,white)
	screen.blit(boss_hp_text,(0,0))
	#flip
	pygame.display.flip()
while dead:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			dead=0
	screen.fill(black)
	screen.blit(background,backgroundrect)
	screen.blit(dead_text,(width/3,height/2))
	pygame.display.flip()
while won:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			won=0
	screen.fill(black)
	screen.blit(background,backgroundrect)
	screen.blit(won_text,(width/3,height/2))
	pygame.display.flip()
pygame.quit()