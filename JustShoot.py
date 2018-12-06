import pygame
import random
import sys
import os
import time
from pygame.locals import *
from sys import exit


SCREEN_WIDTH=640
SCREEN_HEIGHT=480
SCREEN_SIZE=(SCREEN_WIDTH,SCREEN_HEIGHT)


center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
pos1=[SCREEN_WIDTH/2-5,SCREEN_HEIGHT/2-5]

clock=pygame.time.Clock()

bullet_speed=500
enemy_speed=150

class Bullet(pygame.sprite.Sprite):
    def __init__(self,bullet_img,aim_pos,start_pos=center,damage=1):
        pygame.sprite.Sprite.__init__(self)
        self.speed_x=0.
        self.speed_y=0.
        self.speed_x=(aim_pos[0]-start_pos[0])/(((aim_pos[0]-start_pos[0])**2+(aim_pos[1]-start_pos[1])**2)**0.5)*bullet_speed
        self.speed_y=(aim_pos[1]-start_pos[1])/(((aim_pos[0]-start_pos[0])**2+(aim_pos[1]-start_pos[1])**2)**0.5)*bullet_speed 
        self.image=bullet_img
        self.rect=self.image.get_rect()
        self.rect.top=start_pos[1]-self.image.get_height()/2
        self.rect.left=start_pos[0]-self.image.get_width()/2
        self.damage=damage

    def move(self):
        self.rect.top+=self.speed_y*time_passed_seconds
        self.rect.left+=self.speed_x*time_passed_seconds

class Player(pygame.sprite.Sprite):
    def __init__(self,player_img,player_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=player_img
        self.rect=self.image.get_rect()
        self.rect.top=player_pos[1]-self.image.get_height()/2+1
        self.rect.left=player_pos[0]-self.image.get_width()/2+1
        self.is_hit=False
        self.bullets=pygame.sprite.Group()
    
    def shoot(self,bullet_img,aim_pos):
        bullet=Bullet(bullet_img,aim_pos)
        self.bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,enemy_img,enemy_pos,aim_pos=center,hp=50):
        pygame.sprite.Sprite.__init__(self)
        self.image=enemy_img
        self.rect=self.image.get_rect()
        self.speed_x=(aim_pos[0]-enemy_pos[0])/(((aim_pos[0]-enemy_pos[0])**2+(aim_pos[1]-enemy_pos[1])**2)**0.5)*enemy_speed
        self.speed_y=(aim_pos[1]-enemy_pos[1])/(((aim_pos[0]-enemy_pos[0])**2+(aim_pos[1]-enemy_pos[1])**2)**0.5)*enemy_speed  
        self.rect.top=enemy_pos[1]-self.image.get_height()/2+1
        self.rect.left=enemy_pos[0]-self.image.get_width()/2+1
        self.hp=hp

    def move(self):
        self.rect.top+=self.speed_y*time_passed_seconds
        self.rect.left+=self.speed_x*time_passed_seconds

        



pygame.init()
screen=pygame.display.set_mode(SCREEN_SIZE,0,32)
pygame.display.set_caption("Just Shoot")

speed_x=0.
speed_y=0.

cube=pygame.Surface((11,11))
cube2=pygame.Surface((8,8))
bullet_size=8
cube3=pygame.Surface((20,20))
cube.fill((255,0,0))
cube2.fill((240,240,240))
cube3.fill((10,10,10))
r,g,b=(240,240,240)

enemies=pygame.sprite.Group()
enemy_frequency=0
enemy_frequency2=50

player=Player(cube,center)

score=0

run=False

font=pygame.font.Font(None,48)
text=font.render("Just Shoot",True,(255,255,255))
text_rect=text.get_rect()
text_rect.centerx = screen.get_rect().centerx-2
text_rect.centery = screen.get_rect().centery-10

font2=pygame.font.Font(None,24)
text2=font2.render("Press any key to play",True,(145,145,145))
text2_rect=text2.get_rect()
text2_rect.centerx = screen.get_rect().centerx
text2_rect.centery = screen.get_rect().centery+150

font3=pygame.font.Font(None,12)
text3=font3.render("Code by Kanolin. 2018.11",True,(160,160,160))
text3_rect=text3.get_rect()
text3_rect.centerx = screen.get_rect().right-80
text3_rect.centery = screen.get_rect().bottom-20

firstrun=True;
while not run:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type==KEYDOWN:
            run=True

    screen.fill((125,125,125))
    screen.blit(text,text_rect)
    screen.blit(text2,text2_rect)
    screen.blit(text3,text3_rect)
    pygame.mouse.set_visible(False)
    x,y=pygame.mouse.get_pos()
    pygame.draw.circle(screen,(255,255,255),(x,y),3)
    pygame.display.update()     
    
    
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    time_passed = clock.tick(60)
    time_passed_seconds = time_passed/1000
    
    if enemy_frequency%enemy_frequency2==0:      
        direct=random.randint(0,3)
        if direct%2==0:
            enemy_pos_y=random.randint(0,SCREEN_HEIGHT)
            enemy_pos_x=0 if direct==0 else SCREEN_WIDTH;
        else:
            enemy_pos_x=random.randint(0,SCREEN_WIDTH)
            enemy_pos_y=0 if direct==1 else SCREEN_HEIGHT;
        enemy1=Enemy(cube3,(enemy_pos_x,enemy_pos_y))
        enemies.add(enemy1)
    enemy_frequency+=1;
    if enemy_frequency>=1000:
        enemy_frequency=0
        if enemy_frequency2/2>=1:
            enemy_frequency2/=2
        enemy_speed+=20
        if bullet_size<=50:
            bullet_size+=5 
        r=(r-20)%255
        g=(g-20)%255
        b=(b-20)%255   
   

    if not player.is_hit:
        if pygame.mouse.get_pressed()[0]:
            player.shoot(cube2,pygame.mouse.get_pos())
    
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.top<0 or bullet.rect.top>SCREEN_HEIGHT or bullet.rect.left<0 or bullet.rect.left>SCREEN_WIDTH:
            player.bullets.remove(bullet)
    
    enemies_collide=pygame.sprite.groupcollide(enemies,player.bullets,0,1)
    for enemy_collide in enemies_collide:
        enemy_collide.hp-=5

    for enemy in enemies:
        enemy.move()
        if pygame.sprite.collide_rect(enemy,player):
            player.is_hit=True
            run=False
            break
        if enemy.hp<=0:
            enemies.remove(enemy)
            score+=1
        if enemy.rect.top<-50 or enemy.rect.top>SCREEN_HEIGHT+50 or enemy.rect.left<-50 or enemy.rect.left>SCREEN_WIDTH+50:
            enemies.remove(enemy)

    if firstrun:
        enemies.empty()
        firstrun=False
    screen.fill((125,125,125))
    cube2=pygame.Surface((bullet_size,bullet_size))
    cube2.fill((abs(r),abs(g),abs(b)))

    pygame.mouse.set_visible(False)
    x,y=pygame.mouse.get_pos()
    pygame.draw.circle(screen,(255,255,255),(x,y),3)

    if not player.is_hit:
        screen.blit(player.image,player.rect)
    player.bullets.draw(screen)
    
    enemies.draw(screen)
    
    score_font=pygame.font.Font(None,36)
    score_text=score_font.render(str(score),True,(146,158,168))
    text_rect=score_text.get_rect()
    text_rect.topleft=[10,10]
    screen.blit(score_text,text_rect)

    pygame.display.update()

end_font=pygame.font.Font(None,48)
end_text=end_font.render("DESTORY:"+str(score),True,(255,255,255))
text_rect=end_text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery 

text2=font2.render("Press any key to restart",True,(145,145,145))

screen.fill((125,125,125))
screen.blit(end_text,text_rect)
screen.blit(text2,text2_rect)


while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type==KEYDOWN:
            python = sys.executable
            os.execl(python, python, * sys.argv)
    pygame.display.update()