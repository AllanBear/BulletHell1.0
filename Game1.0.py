import pygame
import random
import os 
import math
from pygame.locals import *

#Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
#art by my friend Chris because he's a gud boye
width=600
height=600
fps=60
vec=pygame.math.Vector2
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
delay=6
bosshealth=10000
spreadnice=0
lives=2
ik=1
k=0
touchboss=0
bossgoright=0
power=25
bossdelay=0
bossshouldshoot=1
bossshouldshoot2=1
enemyspawn=1
q2=q=0
qb=0
q3=q1=3.14
delayb=0
bombs=10
bombtime=pygame.time.get_ticks()
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
		self.pos=vec(width/2,height-30)
		self.speedx=0
		self.speedy=0
		self.shield=100
		self.speed=vec(0,0)
		self.acc=vec(0,0)
	def update(self):
		self.acc=vec(0,0)
		self.accc=0.5
		self.friction=0.12
		global k,delay
		keystate=pygame.key.get_pressed()
		if keystate[pygame.K_z]:
			self.accc=0.3
		if keystate[pygame.K_LEFT]:
			self.acc.x=-self.accc
		if keystate[pygame.K_RIGHT]:
			self.acc.x=self.accc
		if keystate[pygame.K_UP]:
			self.acc.y=-self.accc
		if keystate[pygame.K_DOWN]:
			self.acc.y=self.accc
		if keystate[pygame.K_x]:
			self.boom()

		if keystate[pygame.K_SPACE]:
			if k%delay==0:
				self.shoot()
			k+=1
		else:
			k=0	

		#friction
		self.acc+=self.speed*-self.friction
		self.speed+=self.acc
		self.pos+=self.speed+self.acc/2
		self.rect.center=self.pos
		if self.rect.right>width:
			self.rect.right=width
		if self.rect.top<0:
			self.rect.top=0
		if self.rect.bottom>height:
			self.rect.bottom=height
		if self.rect.left<0:
			self.rect.left=0
	def shoot(self):
		global rsp, delay,spreadnice,q,q1,q2,q3
		if power<=3:
			bullet=Bullet(self.rect.center,self.rect.top,10,0)
			all_sprites.add(bullet)
			bullets.add(bullet)
		elif power<=10:
			
			bullet=Bullet(self.rect.center,self.rect.top,6,0)
			all_sprites.add(bullet)
			bullets.add(bullet)
			bullet1=Bullet(self.rect.center,self.rect.top,6,-1)
			all_sprites.add(bullet1)
			bullets.add(bullet1)
			bullet2=Bullet(self.rect.center,self.rect.top,6,1)
			all_sprites.add(bullet2)
			bullets.add(bullet2)
		elif power<=15:
			
			bullet=Bullet(self.rect.center,self.rect.top,8,0)
			all_sprites.add(bullet)
			bullets.add(bullet)
			bullet1=Bullet(self.rect.center,self.rect.top,8,-rsp)
			all_sprites.add(bullet1)
			bullets.add(bullet1)
			bullet2=Bullet(self.rect.center,self.rect.top,8,rsp)
			all_sprites.add(bullet2)
			bullets.add(bullet2)
		elif power<25:
			delay=1
			angb=Anglebullet(self.rect.x,self.rect.y,q,10,1)
			all_sprites.add(angb)
			bullets.add(angb)
			q-=0.3
			angb1=Anglebullet(self.rect.x,self.rect.y,q1,10,1)
			all_sprites.add(angb1)
			bullets.add(angb1)
			q1-=0.3
		else:
			delay=1
			angb=Anglebullet(self.rect.x,self.rect.y,q,3,1)
			all_sprites.add(angb)
			bullets.add(angb)
			q-=0.2
			angb1=Anglebullet(self.rect.x,self.rect.y,q1,3,1)
			all_sprites.add(angb1)
			bullets.add(angb1)
			q1-=0.2
			#angb2=Anglebullet(self.rect.x,self.rect.y,q2,4,1)
			#all_sprites.add(angb2)
			#bullets.add(angb2)
			#q2+=0.5
			#angb3=Anglebullet(self.rect.x,self.rect.y,q3,4,1)
			#all_sprites.add(angb3)
			#bullets.add(angb3)
			#q3+=0.5
			bullet1=Specialbullet(width/3,height,self.rect.x,self.rect.y,20,1,0)
			all_sprites.add(bullet1)
			bullets.add(bullet1)
			bullet2=Specialbullet(width/3*2,height,self.rect.x,self.rect.y,20,1,0)
			all_sprites.add(bullet2)
			bullets.add(bullet2)
			#bullet3=Bullet(self.rect.center,self.rect.top,15,-abs(rsp))
			#all_sprites.add(bullet3)
			#bullets.add(bullet3)
			#bullet4=Bullet(self.rect.center,self.rect.top,15,abs(rsp))
			#all_sprites.add(bullet4)
			#bullets.add(bullet4)
		if spreadnice:
			rsp-=1
		else:
			rsp+=1
		if rsp>1:
			spreadnice=1
		if rsp<=0:
			spreadnice=0
	def boom(self):
		global bombtime,bosshealth,bombs
		now=pygame.time.get_ticks()
		if now-bombtime>3000 and bombs!=0:
			boom=Explosion(player.rect.center,'bomb',30)
			all_sprites.add(boom)
			for b in bossbullets:
				b.kill()
				tinyboom=Explosion(b.rect.center,'regexp',30)
				all_sprites.add(tinyboom)
				angbtrap=Specialbullet(b.rect.x,b.rect.y,self.rect.x,self.rect.y,-10,3,0)
				all_sprites.add(angbtrap)
				bullets.add(angbtrap)
			for i in mobs:
				smolboom=Explosion(i.rect.center,'playerexp',25)
				all_sprites.add(smolboom)
				i.kill()
				spawn()
			for i in bullets:
				i.kill()
				#angb1=Specialbullet(i.rect.x,i.rect.y,self.rect.x,self.rect.y,3,1,4.5)
				#all_sprites.add(angb1)
				#bullets.add(angb1)
				#angb2=Specialbullet(i.rect.x,i.rect.y,self.rect.x,self.rect.y,3,1,1.5)
				#all_sprites.add(angb2)
				#bullets.add(angb2)
				angb3=Specialbullet(i.rect.x,i.rect.y,self.rect.x,self.rect.y,-5,3,0)
				all_sprites.add(angb3)
				bullets.add(angb3)
				#angb4=Specialbullet(i.rect.x,i.rect.y,self.rect.x,self.rect.y,-3,1,0)
				#all_sprites.add(angb4)
				#bullets.add(angb4)

			bombtime=now
			bosshealth-=int(bosshealth/10)
			bombs-=1
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
lastshot=pygame.time.get_ticks()
class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y,speed,bspread):
		pygame.sprite.Sprite.__init__(self)
		self.image=laser
		self.image.set_colorkey(white)
		self.rect=self.image.get_rect()
		self.rect.bottom=y
		self.rect.center=x
		self.speed=-speed
		self.spread=bspread
	def update(self):
		self.rect.y+=self.speed
		self.rect.x+=self.spread
		if self.rect.bottom<0:
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
		global bossgoright,bossdelay,power,bossshouldshoot
		if not bossgoright:
			self.rect.centerx-=speed
			if self.rect.x<20:
				bossgoright=1
		else:
			self.rect.x+=speed
			if self.rect.centerx>width-40:
				bossgoright=0
		if bossshouldshoot:
			if bossdelay==max(60-(power//10),40):
				self.shoot()
				bossdelay=0
			bossdelay+=1
		if bossshouldshoot2:
			global qb,delayb
			if delayb==max(10-(power//3),2):
				angb=Anglebullet(self.rect.x,self.rect.y,qb,1,3)
				all_sprites.add(angb)
				bossbullets.add(angb)
				qb+=0.4
				delayb=0
			else:
				delayb=delayb+1
	def shoot(self):
		bossbullet=Specialbullet(self.rect.x,self.rect.y,player.rect.x,player.rect.y,1,2,0)
		all_sprites.add(bossbullet)
		bossbullets.add(bossbullet)
class Explosion(pygame.sprite.Sprite):
	def __init__(self,center,size,time):
		pygame.sprite.Sprite.__init__(self)
		self.size=size
		self.time=time
		self.image=explosionanimation[self.size][0]
		self.rect=self.image.get_rect()
		self.rect.center=center
		self.frame=0
		self.lastupdate=pygame.time.get_ticks()
		self.framerate=time
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
	if enemyspawn:
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
		self.radius=15
	def update(self):
		self.rect.y+=self.speedy
		if self.rect.top>height:
			self.kill()
class Specialbullet(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y, dest_x, dest_y,speed,typeob,additionalangle):
		pygame.sprite.Sprite.__init__(self)
		self.type=typeob
		self.aa=additionalangle
		if self.type==1:
			self.image=laser
		elif self.type==2:
			self.image=bigbb
		else:
			self.image=blueb
		self.image.set_colorkey(white)
		self.rect = self.image.get_rect()
		self.rect.x = start_x
		self.rect.y = start_y
		self.floating_point_x = start_x
		self.floating_point_y = start_y
		x_diff = dest_x - start_x
		y_diff = dest_y - start_y
		angle = math.atan2(y_diff, x_diff)+self.aa;
		self.speed=speed
		self.change_x = math.cos(angle) *self.speed
		self.change_y = math.sin(angle) *self.speed
		self.radius=3
	def update(self):
		self.floating_point_y += self.change_y
		self.floating_point_x += self.change_x
		self.rect.y = int(self.floating_point_y)
		self.rect.x = int(self.floating_point_x)
		if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
			self.kill()
class Anglebullet(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y,angle,speed,typeob):
		pygame.sprite.Sprite.__init__(self)
		bt=typeob
		if bt==1:
			self.image=laser
		elif bt==2:
			self.image=bbsprite
		else:
			self.image=bigbb
		self.image.set_colorkey(white)
		self.rect = self.image.get_rect()
		self.rect.x = start_x
		self.rect.y = start_y
		self.floating_point_x = start_x
		self.floating_point_y = start_y
		self.speed=speed
		a=angle
		self.change_x = math.cos(a) *self.speed
		self.change_y = math.sin(a) *self.speed
		self.radius=3
	def update(self):
		self.floating_point_y += self.change_y
		self.floating_point_x += self.change_x
		self.rect.y = int(self.floating_point_y)
		self.rect.x = int(self.floating_point_x)
		if self.rect.right < 0 or self.rect.left > width or self.rect.bottom < 0 or self.rect.top > height:
			self.kill()
bbsprite=pygame.image.load('bossbulletsprite.png')
bigbb=pygame.image.load('enbu.png')
blueb=pygame.image.load('blueb.png')
background=pygame.image.load('starfield.png')
playerimg=pygame.image.load('ship.png')
iplayerimg=pygame.image.load('shipifr.png')
enemyimg=pygame.image.load('alien.png')
laser=pygame.image.load('bulletnice.png')
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
explosionanimation['bomb']=[]
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
for i in range(11):
	forbomb='ee{}.png'.format(i)
	bombimg=pygame.image.load(forbomb)
	bombimg.set_colorkey((48,48,48))
	nbi=pygame.transform.scale(bombimg,(1000,1000))
	explosionanimation['bomb'].append(nbi)
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
if enemyspawn:
	for i in range(10):
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
		dexpl=Explosion(player.rect.center,'playerexp',60)
		all_sprites.add(dexpl)
		player.kill()
		yourhp.kill()
		touchboss=1
		lives=-1
	hits=pygame.sprite.spritecollide(player,bossbullets,True,pygame.sprite.collide_circle)
	for hit in hits:
		player.shield-=10
		expl=Explosion(hit.rect.center,'regexp',60)
		all_sprites.add(expl)
		gothit.play()
		spawn()
	hits=pygame.sprite.groupcollide(mobs,bullets,True,True)
	for hit in hits:
		expl=Explosion(hit.rect.center,'regexp',60)
		all_sprites.add(expl)
		if power <=25:
			chance=random.randrange(1,100)
			if chance<=22:
				pup=Powerup(hit.rect.center)
				pwrups.add(pup)
				all_sprites.add(pup)
		spawn()
	pickedup=pygame.sprite.spritecollide(player,pwrups,True,pygame.sprite.collide_circle)
	for yay in pickedup:
		power+=random.randrange(1,2)
	hits=pygame.sprite.spritecollide(boss,bullets,True,pygame.sprite.collide_circle)
	for hit in hits:
		bosshealth-=power//5
		expl=Explosion(hit.rect.center,'regexp',60)
		all_sprites.add(expl)
	if bosshealth<0:
		running=False
		won=1
	now=pygame.time.get_ticks()
	if now-lastshot>3000:
		bosshealth-=power*10
		for monsters in mobs:
			if monsters.rect.y<height/2:
				ebullet=Specialbullet(monsters.rect.x,monsters.rect.y,player.rect.x,player.rect.y,1,2,0)
				all_sprites.add(ebullet)
				bossbullets.add(ebullet)
		lastshot=now
	#hitss=pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
	#for hit in hitss:
	#	player.shield-=40
	#	expl=Explosion(hit.rect.center,'regexp')
	#	all_sprites.add(expl)
	#	gothit.play()
	#	spawn()
	if player.shield<=0:
		dexpl=Explosion(hit.rect.center,'playerexp',60)
		all_sprites.add(dexpl)
		if lives<0:
			yourhp.kill()
			player.kill()
			dexpl=Explosion(hit.rect.center,'playerexp',60)
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