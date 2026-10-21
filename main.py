import pygame
import numpy as np
import math
import random
import os
pygame.init()
pygame.display.set_caption("TC")
clock = pygame.time.Clock()
game_on = True
title = True #dictates if title screen is on
turn_enable = False #dictates if player can turn the pointer
down = False #dictates if the squares will fall
gen = False #dictates if another square layer will be generated
fire = False #dictates if and when pellets are being fired
lost = False #dictates if the player lost
high_score_record = False #dictates if the layer is recorded as high score
black = (0, 0, 0) #RGB
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (157, 0, 255)
pink = (255, 100, 237)
fake_purple = (255, 0, 255)
width = 420
height = 660
angle_p = 90 #angle of pointer
ac = (math.pi / 180) #to convert degrees into radians
l_p = 60
temp_ammo = 0
end_x = (l_p*math.cos(angle_p * ac)) + 210
end_y = (-l_p*math.sin(angle_p * ac)) + (660 - 12)
layer = 0 # the amount of square layers that have been created thus far
pellet = 0 # the amount of "balls" on the screen at the moment
ammo = 1 # the amount of pellet you have left to shoot
if not os.path.exists("TC_high_score"):
    with open("TC_high_score", "w") as f:
        f.write("0")
with open('TC_high_score', "r") as file:
    high_score = int(file.read())
if not os.path.exists("TC_save_file"):
    with open("TC_save_file", "w") as file:
        file.write("-1")
    # os.mkdir("TC_save_files")
angle_pel = np.zeros(ammo)#angle of pellet[i] remember to reinitialize values once pellet==0
def collision(cir_cen_x, cir_cen_y, radius, rect):
    nearest_x=max(rect.left, min(rect.right, cir_cen_x))
    nearest_y=max(rect.top, min(rect.bottom, cir_cen_y))
    delta_x=cir_cen_x - nearest_x
    delta_y=cir_cen_y - nearest_y
    return (pow(delta_x, 2) + pow(delta_y, 2)) <= (radius*radius)
fps = 120
temp_fps = fps #im going to be manipulating fps later but need it returned to inital value
p_speed=300/fps #pellet speed, 2.5 when fps==120
temp_p_speed = p_speed
mode_sum2 = 0
corner_sq = np.zeros((2, 77)) # the top-left corner cord for each 77 squares
square_mode = np.zeros(77) #dictates if a square is on or not
square_color = np.zeros((3,77)) #square_color[R=0,G=1,B=2][square-1]
square_health = np.zeros(77)
for i in range (1,78): #range = 1-77
    if (i <= 7):
        corner_sq[0][i-1] = (i-1)*60
        corner_sq[1][i-1] = 660-60+15
    if (i <= 14 and i > 7):
        corner_sq[0][i-1] = ((i-7)-1)*60
        corner_sq[1][i-1] = 660-(60*2)+15
    if (i <= 21 and i > 14):
        corner_sq[0][i-1] = ((i-14)-1)*60
        corner_sq[1][i-1] = 660-(60*3)+15
    if (i <= 28 and i > 21):
        corner_sq[0][i-1] = ((i-21)-1)*60
        corner_sq[1][i-1] = 660-(60*4)+15
    if (i <= 35 and i > 28):
        corner_sq[0][i-1] = ((i-28)-1)*60
        corner_sq[1][i-1] = 660-(60*5)+15
    if (i <= 42 and i > 35):
        corner_sq[0][i-1] = ((i-35)-1)*60
        corner_sq[1][i-1] = 660-(60*6)+15
    if (i <= 49 and i > 42):
        corner_sq[0][i-1] = ((i-42)-1)*60
        corner_sq[1][i-1] = 660-(60*7)+15
    if (i <= 56 and i > 49):
        corner_sq[0][i-1] = ((i-49)-1)*60
        corner_sq[1][i-1] = 660-(60*8)+15
    if (i <= 63 and i > 56):
        corner_sq[0][i-1] = ((i-56)-1)*60
        corner_sq[1][i-1] = 660-(60*9)+15
    if (i <= 70 and i > 63):
        corner_sq[0][i-1] = ((i-63)-1)*60
        corner_sq[1][i-1] = 660-(60*10)+15
    if (i <= 77 and i > 70):
        corner_sq[0][i-1] = ((i-70)-1)*60
        corner_sq[1][i-1] = 660-(60*11)+15
font1 = pygame.font.SysFont(None, 45)
font_sq = pygame.font.SysFont(None, 30)
font_high = pygame.font.SysFont(None, 15)
font_title=pygame.font.SysFont(None, 60)
font_title2=pygame.font.SysFont(None, 25)
def save_func():
    global layer, ammo, end_x, end_y, angle_p, square_mode, square_health, square_color
    with open("TC_save_file", "w") as file_save:
        file_save.write(f"{layer}\n")
        file_save.write(f'{ammo}\n')
        file_save.write(f'{end_x}\n')
        file_save.write(f'{end_y}\n')
        file_save.write(f'{angle_p}\n')
        for i in range(1,78):
            file_save.write(f'{int(square_mode[i-1])}\n')
        for i in range(1,78):
            file_save.write(f'{int(square_health[i-1])}\n')
        for i in range(1,78):
            file_save.write(f'{int(square_color[0][i-1])},{int(square_color[1][i-1])},{int(square_color[2][i-1])}\n')
def load_func():
    global layer, ammo, end_x, end_y, angle_p, square_mode, square_health, square_color
    if not os.path.exists("TC_save_file"):
        return False
        # pass
    else:
        with open("TC_save_file", "r") as file_save:
            lines = file_save.readlines()
            if lines[0].strip() == "-1":
                return False
                # pass
            else:
                index = 0
                layer = int(lines[index].strip()); index += 1
                ammo = int(lines[index].strip()); index += 1
                end_x = float(lines[index].strip()); index += 1
                end_y = float(lines[index].strip()); index += 1
                angle_p = float(lines[index].strip()); index += 1
                square_mode = [int(lines[i].strip()) for i in range(index, index + 77)]
                index += 77
                square_health = [int(lines[i].strip()) for i in range(index, index + 77)]
                index += 77
                r_value, g_value, b_value = [],[],[]
                for i in range(index, index+77):
                    r,g,b = map(int, lines[i].strip().split(','))
                    r_value.append(r)
                    g_value.append(g)
                    b_value.append(b)
                square_color = [r_value, g_value, b_value]
screen = pygame.display.set_mode((width, height))
screen.fill(black)
while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_on = False
            if event.key == pygame.K_SPACE:
                title = False
                # down = True
                # gen = True
            if event.key == pygame.K_f and (pellet == 0):
                fire = True
            if event.key == pygame.K_r:
                if layer > high_score:
                    with open('TC_high_score', "w") as file:
                        file.write(str(layer))
                    high_score = layer
            if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL and (pellet==0):
                save_func()
            if event.key == pygame.K_l and event.mod & pygame.KMOD_CTRL and (pellet==0):
                load_func()
            if event.key == pygame.K_g:
                mode_sum2=0
                lost=False
                layer=0
                pellet=0
                ammo=1
                square_mode = np.zeros(77)  # dictates if a square is on or not
                square_color = np.zeros((3, 77))
                square_health = np.zeros(77)
                angle_p=90
                end_x = (l_p * math.cos(angle_p * ac)) + 210
                end_y = (-l_p * math.sin(angle_p * ac)) + (660 - 12)
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_a]) and (angle_p <= 155) and (turn_enable):
        angle_p += 120/fps
        end_x = (l_p*math.cos(angle_p * ac)) + 210
        end_y = (-l_p*math.sin(angle_p * ac)) + (660 - 12)
    if (keys[pygame.K_d]) and (angle_p >= 25) and (turn_enable):
        angle_p -= 120/fps
        end_x = (l_p * math.cos(angle_p * ac)) + 210
        end_y = (-l_p*math.sin(angle_p * ac)) + (660 - 12)
    if layer == 0:
        mode_sum = 0
        green_choice1 = random.randint(71, 77)
        for i in range(71, 78):
            square_mode[i - 1] = random.randint(0, 1)
            square_color[0][i-1] = 255
            square_color[1][i-1] = 255
            square_color[2][i-1] = 255
            square_health[i-1] = random.randint(1, 2)
        for i in range (71, 78):
            if square_mode[i-1] == 1:
                mode_sum = mode_sum + square_mode[i-1]
        if mode_sum <= 0:
            layer = 0
        elif mode_sum == 7:
            layer = 0
        else:
            layer = 1
        for i in range (71, 78):
            if i == green_choice1:
                square_mode[i - 1] = -1  #-1 means it is a green square
                square_color[0][i - 1] = 0
                square_color[1][i - 1] = 255
                square_color[2][i - 1] = 0
                square_health[i - 1]=0
        turn_enable = True
    if down == True:
        turn_enable = False
        for i in range (1, 78):
            if square_mode[i-1] == 1:
                square_mode[(i-1)-7] = 1
                square_health[(i-1)-7] = square_health[i-1]
                square_color[0][(i-1)-7] = square_color[0][i-1]
                square_color[1][(i-1)-7] = square_color[1][i-1]
                square_color[2][(i-1)-7] = square_color[2][i-1]
                square_mode[i-1] = 0
                square_health[i-1] = 0
            if square_mode[i-1] == -1:
                square_mode[(i-1)-7] = -1
                square_health[(i-1)-7] = square_health[i-1]
                square_color[0][(i-1)-7] = square_color[0][i-1]
                square_color[1][(i-1)-7] = square_color[1][i-1]
                square_color[2][(i-1)-7] = square_color[2][i-1]
                square_mode[i-1] = 0
                square_health[i-1] = 0
        down = False
        turn_enable = True
    for i in range (1,8):
        if square_mode[i-1] == 1:
            mode_sum2 = mode_sum2 + square_mode[i-1]
    if mode_sum2 > 0: #lost condition
        lost = True
        high_score_record = True
    if gen == True:
        layer += 1
        turn_enable = False
        mode_sum3 = 0
        green_choice2 = random.randint(71, 77)
        for i in range(71, 78):
            square_mode[i - 1] = random.randint(0, 1)
            square_color[0][i-1] = 255
            square_color[1][i-1] = 255
            square_color[2][i-1] = 255
            square_health[i-1] = random.randint(1, 20)
            if square_health[i-1] <= 13:
                square_health[i-1] = layer
            if square_health[i-1] > 13:
                square_health[i-1] = (2*layer)
        for i in range(71, 78):
            if square_mode[i-1] == 1:
                mode_sum3 = mode_sum3 + square_mode[i - 1]
        if mode_sum3 <= 0:
            gen = True
        elif mode_sum3 == 7:
            gen = True
        else:
            turn_enable = True
            gen = False
        for i in range(71,78):
            if i == green_choice2:
                square_mode[i - 1] = -1  #-1 means it is a green square
                square_color[0][i - 1] = 0
                square_color[1][i - 1] = 255
                square_color[2][i - 1] = 0
                square_health[i - 1]=0
    if fire == True and (pellet == 0) and not title:
        turn_enable = False
        gen = False
        down = False
        pellet_center = np.zeros((2, ammo))  # pellet_center[x=0,y=1][ammo-1=max]
        angle_pel = np.zeros(ammo)
        move_pel = np.zeros(ammo)
        frame_count=0
        for i in range(ammo):
            pellet_center[0][i] = width / 2
            pellet_center[1][i] = height - 12
            angle_pel[i] = angle_p
            move_pel[i] = False
            pellet = pellet + 1
        fire = False
    if title:
        title_text = font_title.render("Pinball-Like Game", True, blue)
        #title_text2 = font_title2.render("Thank You for playing my game", True, blue)
        title_text3 = font_title.render("By Robert Geer", True, red)
        title_text4 = font_sq.render("Space == continue", True, white)
        title_text5 = font_sq.render("A == point left", True, white)
        title_text6 = font_sq.render("D == point right", True, white)
        title_text7 = font_sq.render("F == fire", True, white)
        title_text8 = font_sq.render("Ctrl + S == save", True, white)
        title_text9 = font_sq.render("Ctrl + L == load", True, white)
        title_text10 = font_sq.render("H == display highscore", True, white)
        title_text11 = font_sq.render("R == record new highscore", True, white)
        title_text12 = font_sq.render("G == restart", True, white)
        title_text13 = font_sq.render("ESC == exit", True, white)
        title_text14 = font_title.render("Thank You", True, purple)
        title_text15 = font_title.render("For Playing!", True, purple)
        screen.blit(title_text, (30,30))
        #screen.blit(title_text2, (30,90))
        screen.blit(title_text3, (50,120))
        screen.blit(title_text4, (30,170))
        screen.blit(title_text5, (30,190))
        screen.blit(title_text6, (30,210))
        screen.blit(title_text7, (30,230))
        screen.blit(title_text8, (30,250))
        screen.blit(title_text9, (30,270))
        screen.blit(title_text10, (30,290))
        screen.blit(title_text11, (30,310))
        screen.blit(title_text12, (30,330))
        screen.blit(title_text13, (30,350))
        screen.blit(title_text14, (90,400))
        screen.blit(title_text15, (80,450))
    if lost:
        square_mode = np.zeros(77)
        mode_sum2 = 0
        fire = False
        if high_score_record:
            with open('TC_high_score', "r") as file:
                high_score = int(file.read())
            if (layer-1) == high_score:
                text_lost4 = font1.render('High score == ' + str(high_score), False, white)
                high_score_record = False
            elif (layer-1) < high_score:
                text_lost4 = font1.render('High score == ' + str(high_score), False, white)
                high_score_record = False
            elif (layer-1) > high_score:
                with open('high_score', "w") as file:
                    file.write(str(layer-1))
                text_lost4 = font1.render('NEW HIGHSCORE!', False, green)
                high_score_record = False
                # print(high_score_record)
        screen.fill(black)
        text_lost = font1.render('You LOST!', False, red)
        text_lost2 = font1.render("Press g to restart", False, red)
        text_lost3 = font1.render('You got to layer ' + str(layer-1), False, white)
        screen.blit(text_lost, (corner_sq[0][38-1], corner_sq[1][38-1]))
        screen.blit(text_lost2, (corner_sq[0][38-1], corner_sq[1][32-1]))
        screen.blit(text_lost3, (corner_sq[0][38-1], corner_sq[1][26-1]))
        screen.blit(text_lost4, (corner_sq[0][38 - 1], corner_sq[1][20 - 1]))
    if not lost and not title:
        screen.fill(black)
        #pygame.draw.rect(screen, color, (cordx, cordy, horizontal, vertical)
        # pygame.draw.rect(screen, red, (0, 660, 420, 10)) #bottom
        # pygame.draw.rect(screen, red, (-10, 0, 10, 660)) #left
        # pygame.draw.rect(screen, red, (420, 0, 10, 660)) #right
        # pygame.draw.rect(screen, red, (0, -10, 420, 10)) #top
        for i in range(1, 78):
            if square_mode[i-1] == 1:
                pygame.draw.rect(screen, (square_color[0][i-1],square_color[1][i-1],square_color[2][i-1]), (corner_sq[0][i -1], corner_sq[1][i - 1], 60, 60))
            if square_mode[i-1] == -1:
                pygame.draw.rect(screen, (square_color[0][i - 1], square_color[1][i - 1], square_color[2][i - 1]),(corner_sq[0][i - 1], corner_sq[1][i - 1], 60, 60))
        for i in range(1, 78):
            if square_health[i-1] > 0:
                square_t = font_sq.render(str(round(square_health[i-1])), True, black)
                screen.blit(square_t, (corner_sq[0][i-1]+20, corner_sq[1][i-1]+20))
        if turn_enable == True:
            pygame.draw.line(screen, red, (width / 2, height - 12), (end_x, end_y), 3)
        if pellet != 0:
            for i in range(ammo):
                if (fps/6)*i==frame_count:
                    move_pel[i] = True
                # for k in range(1,11):
                #     if frame_count == 120*k:
                #         p_speed += p_speed
                if move_pel[i] == True:
                    pellet_center[0][i] += p_speed * math.cos(angle_pel[i] * ac)  # xcord
                    pellet_center[1][i] -= p_speed * math.sin(angle_pel[i] * ac)  # ycord
                    pygame.draw.circle(screen, red, (pellet_center[0][i], pellet_center[1][i]), 5)
                if collision(pellet_center[0][i], pellet_center[1][i], 5, pygame.Rect(420, 0, 10, 660)):
                    angle_pel[i] = 180 - angle_pel[i]
                if collision(pellet_center[0][i], pellet_center[1][i], 5, pygame.Rect(-10, 0, 10, 660)):
                    angle_pel[i] = 180 - angle_pel[i]
                if collision(pellet_center[0][i], pellet_center[1][i], 5, pygame.Rect(0, -10, 420, 10)):
                    angle_pel[i] = -angle_pel[i]
                if collision(pellet_center[0][i], pellet_center[1][i], 5, pygame.Rect(0, 660, 420, 10)) and move_pel[i] == True:
                    move_pel[i]=False
                    pellet -= 1
                for j in range(1,78):
                    def side_detect(cir_cen_x, cir_cen_y, radius, rect):
                        global angle_pel, i
                        rect_cen_x, rect_cen_y = rect.center
                        ex = (rect.width / 2) + radius
                        ey = (rect.height / 2) + radius
                        #normalize
                        nx = (cir_cen_x - rect_cen_x) / ex
                        ny = (cir_cen_y - rect_cen_y) / ey
                        if abs(nx) > abs(ny):
                            angle_pel[i] = 180 - angle_pel[i]
                        elif abs(nx) < abs(ny):
                            angle_pel[i] = -angle_pel[i]
                        # else:
                        #     angle_pel[i] = 180 - angle_pel[i]
                    if square_mode[j-1] == 1:
                        if collision(pellet_center[0][i], pellet_center[1][i], 5, pygame.Rect(corner_sq[0][j-1], corner_sq[1][j-1], 60, 60)):
                            side_detect(pellet_center[0][i], pellet_center[1][i], 5, pygame.Rect(corner_sq[0][j-1], corner_sq[1][j-1], 60, 60))
                            square_health[j-1]-=1
                            if square_health[j-1] == 0:
                                square_mode[j-1]=0
                    if square_mode[j-1] == -1:
                        if collision(pellet_center[0][i], pellet_center[1][i], 5,pygame.Rect(corner_sq[0][j - 1], corner_sq[1][j - 1], 60, 60)):
                            temp_ammo += 1
                            square_mode[j-1]=0
            if pellet == 0:
                turn_enable = True
                #ammo+=1
                fps = temp_fps
                p_speed = temp_p_speed
                ammo += temp_ammo
                temp_ammo = 0
                down=True
                gen=True
            frame_count += 1
            # text_fps = font_sq.render("frame == " + str(frame_count), True, purple)
            # screen.blit(text_fps, (corner_sq[0][1], corner_sq[1][15]))
            #pygame.draw.circle(screen, white, (pellet_center[0][i], pellet_center[1][i]), 5)
        pygame.draw.circle(screen, red, (width / 2, height - 12), 8)
        text_ammo = font_sq.render("ammo == " + str(ammo), True, green)
        text_layer= font_sq.render("layer == " + str(layer), True, white)
        screen.blit(text_ammo, (corner_sq[0][1 - 1]+5, corner_sq[1][2 - 1]))
        screen.blit(text_layer, (corner_sq[0][5 - 1]+40, corner_sq[1][2 - 1]))
        if keys[pygame.K_h]:
            text_high_score_display = font_high.render("high score == " + str(high_score), True, white)
            screen.blit(text_high_score_display, (corner_sq[0][39 - 1]-20, corner_sq[1][74 - 1]-10))
    pygame.display.update()
    clock.tick(fps)
if not game_on:
    if layer > high_score:
        with open('TC_high_score', "w") as file:
            file.write(str(layer))
pygame.quit()