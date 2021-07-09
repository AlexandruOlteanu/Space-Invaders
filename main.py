import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Logo.png')
pygame.display.set_icon(icon)

fundal = pygame.image.load('Background.png')

valoare_scor = 0
font = pygame.font.Font('freesansbold.ttf',32)
over_font = pygame.font.Font('freesansbold.ttf',64)
highscore_font = pygame.font.Font('freesansbold.ttf',32)
play_font = pygame.font.Font('freesansbold.ttf',25)
highscore = 0

textX = 10
textY = 10

def play_again():
	play_again = font.render("Press Enter to play again!",True,(255,255,255))
	screen.blit(play_again, (200, 340))

def show_score(x,y):
	score = font.render("Score :" + str(valoare_scor),True,(255,255,255))
	screen.blit(score, (x,y))
def game_over_text():
	over_text = over_font.render("GAME OVER", True, (255,255,255))
	screen.blit(over_text, (200,250))
def show_highscore():
	highscore_text = highscore_font.render("Highscore :" + str(highscore),True,(255,255,255))
	screen.blit(highscore_text, (550,10))
	


player_img = pygame.image.load('Player.png')
player_x = 370
player_y = 480


enemy_img = [] 
enemy_x = []
enemy_y = []
enemy_change_x = []
height_enemy = 40


enemy_bullet = []
enemy_bullet_x = []
enemy_bullet_y = []
state_bullet_2 = []

for i in range (5):
	enemy_img.append(pygame.image.load('Enemy.png'))
	enemy_x.append(random.randint(0,736))
	enemy_y.append(height_enemy)
	height_enemy += 80
	enemy_change_x.append(random.randint(1,10))
	if enemy_change_x[i] <=5:
		enemy_change_x[i] = -0.6
	elif enemy_change_x[i] > 5:
		enemy_change_x[i] = 0.6
for i in range(5):
	enemy_bullet.append(pygame.image.load('Enemy_Bullets.png'))
	enemy_bullet_x.append(enemy_x[i])
	enemy_bullet_y.append(enemy_y[i])
	state_bullet_2.append("ready")

	
glontimg = pygame.image.load('Bullets.png')
glontX = 370
glontY = 480
glont_schimbY = -10
statut_glont = "ready"

def shoot_bullet(x,y):
	global statut_glont
	statut_glont = "fire"
	screen.blit(glontimg, (x+16, y+10))
def shoot_bullet2(x,y):
	screen.blit(enemy_bullet[0], (x+16, y-10))
			
scor = 0;

def jucator(x,y):
	screen.blit(player_img, (x, y)) 
def inamic(x,y):
	screen.blit(enemy_img[i], (x,y))
def intersectcheck(x1,y1,x2,y2):
	distance = math.sqrt((math.pow(x1-x2,2))+(math.pow(y1-y2,2)))
	if distance < 27:
		return True
	else:
		return False

jucator_schimbX = 0
jucator_schimbY = 0
conditie_inamic = "True"
finish = 1
finish2 = 0

running = True
while running:
	screen.blit(fundal, (0,0))
	for eveniment in pygame.event.get():
		if eveniment.type == pygame.QUIT:
			running = False
		if eveniment.type == pygame.KEYDOWN:
			if eveniment.key == pygame.K_RIGHT or eveniment.key == ord('d'):
				jucator_schimbX = 0.5
			if eveniment.key == pygame.K_LEFT or eveniment.key == ord('a'):
				jucator_schimbX = -0.5
			if eveniment.key == pygame.K_SPACE:
				if statut_glont == "ready":
					glontY = player_y
					glontX = player_x
					shoot_bullet(player_x, glontY)
			if eveniment.key == pygame.K_RETURN or eveniment.key == pygame.K_KP_ENTER:
				finish2 = 1		
		if eveniment.type == pygame.KEYUP:
			if eveniment.key == pygame.K_LEFT or eveniment.key == pygame.K_RIGHT or eveniment.key == ord('d') or eveniment.key == ord('a'):
				jucator_schimbX = 0
	player_x += jucator_schimbX
	if player_x < 0:
		player_x = 0
	if player_x >= 736:
		player_x = 736
	for i in range(5):
		enemy_x[i] += enemy_change_x[i]
		if enemy_x[i] >=736:
			enemy_x[i] = 736
			enemy_change_x[i] = -enemy_change_x[i]
		if enemy_x[i] <=0:
			enemy_x[i] = 0
			enemy_change_x[i] = -enemy_change_x[i]
	if statut_glont == "fire":
		shoot_bullet(glontX, glontY)
		glontY -= 0.75
	if glontY <= -70:
		statut_glont = "ready"
		glontY = player_y
	for i in range(5):
		intersect = intersectcheck(enemy_x[i], enemy_y[i], glontX, glontY)
		if intersect:
			glontY = player_y
			enemy_y[i] = -100
			statut_glont = "ready"
			valoare_scor += 1

	for i in range(5):
		inamic(enemy_x[i], enemy_y[i])
	verificare = 0
	for i in range(5):
		if enemy_y[i] == -100:
			verificare += 1
	if verificare == 5 and finish == 1:
		treapta =40
		for i in range(5):
			enemy_y[i] = treapta
			treapta += 80
	for i in range(5):
		if state_bullet_2[i] == "ready":
			enemy_bullet_x[i] = enemy_x[i]
	for i in range(5):
		distance = abs(player_x-enemy_x[i])
		if distance <= 25:
			state_bullet_2[i] = "fire"
	for i in range(5):
		if state_bullet_2[i] == "fire" and enemy_y[i] != -100:
			shoot_bullet2(enemy_bullet_x[i], enemy_bullet_y[i])
			enemy_bullet_y[i] += 0.3
	for i in range(5):
		if enemy_bullet_y[i] >= 870:
			state_bullet_2[i] = "ready"
			enemy_bullet_y[i] = enemy_y[i]
	for i in range(5):
		intersect = intersectcheck(enemy_bullet_x[i], enemy_bullet_y[i], player_x, player_y)
		if intersect:
			for i in range(5):
				enemy_y[i] = -100
			finish = 0
			break
	if finish2 == 1:
		treapta =40
		for i in range(5):
			enemy_y[i] = treapta
			treapta += 80
		for i in range(5):
			enemy_bullet_y[i] = enemy_y[i]
		finish2 = 0
		finish = 1
			
			
	if finish == 0:
		game_over_text()
		finish2 = 0
		play_again()
		if valoare_scor > highscore:
			highscore = valoare_scor
		valoare_scor = 0
			
	jucator(player_x, player_y)
	show_score(textX, textY) 
	show_highscore()	
	pygame.display.flip()
			
	
	
	

			

