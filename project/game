import sys
import pygame
import math
import random
from pygame.locals import QUIT
from math import sin, cos
from copy import copy, deepcopy
import time
from threading import Timer

pygame.init()


class Balls(pygame.sprite.Sprite):
    def __init__(self, radius, pos_x, pos_y, round, group, ball_group, block_group, upgrade_group, game_status) -> None:
        super().__init__(group, ball_group)
        self.image = pygame.image.load("files/image/sphere1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.is_move = False
        self.x_speed = 0
        self.y_speed = 0
        self.speed = 10
        self.radius = radius
        self.block = block_group
        self.ball = ball_group
        self.upgrade = upgrade_group
        self.group = group
        self.round = round
        self.org_board = deepcopy(blk_weight)
        self.damage = 1
        self.game_status = game_status

    def collison(self):

        #collison with other rect
        overlap_sprites = pygame.sprite.spritecollide(self, self.block, False)
        if overlap_sprites:
            for sprite in overlap_sprites:
                if blk_weight[sprite.x//50][sprite.y//50] == self.org_board[sprite.x//50][sprite.y//50]:
                    blk_weight[sprite.x//50][sprite.y//50] -= self.damage
                    if blk_weight[sprite.x//50][sprite.y//50] < 1:
                        sprite.kill()
            # print("after collison")  
            # for i in blk_weight:
            #     print(i)
            # collision sound
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("files/audio/collide_1.ogg"))
        else:
            self.org_board = deepcopy(blk_weight)

        for i in pygame.sprite.spritecollide(self, self.ball, False):
            overlap_sprites.append(i)

        collision_tolerace = self.speed
        if overlap_sprites:
            for sprite in overlap_sprites:
                if abs(sprite.rect.top - self.rect.bottom) < collision_tolerace and self.y_speed < 0:
                    self.y_speed *= -1
                if abs(sprite.rect.bottom - self.rect.top) < collision_tolerace and self.y_speed > 0:
                    self.y_speed *= -1
                if abs(sprite.rect.left - self.rect.right) < collision_tolerace and self.x_speed > 0:
                    self.x_speed *= -1
                if abs(sprite.rect.right - self.rect.left) < collision_tolerace and self.x_speed < 0:
                    self.x_speed *= -1
          

        #collison with upgrade
        opverlap_upgrade = pygame.sprite.spritecollide(self, self.upgrade, True)
        if opverlap_upgrade:
            for upgrades in opverlap_upgrade:
                if upgrades.upgrade_type == "ball_split":
                    tmp_ball = Tmp_Balls(self.radius, self.rect.midright[0]-self.radius-1, self.rect.midright[1], self.round, self.group, self.ball, self.block, self.upgrade, self.damage, self.game_status)
                    tmp_ball.x_speed = self.x_speed * -1
                    tmp_ball.y_speed = self.y_speed * random.uniform(0.7, 1.5)
                    tmp_ball.speed = random.randint(10,13)
                    tmp_ball.is_move = True
                else: 
                    self.damage += 1
                blk_weight[upgrades.rect.topleft[0]//50][upgrades.rect.topleft[1]//50] = 0
                # collision sound
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("files/audio/collide_2.ogg"))

            
            


    def kill_all_block_and_upgrade(self):
        for sprite in self.block:
            sprite.kill()
        for sprite in self.upgrade:
            sprite.kill()

    def update(self):
        if self.is_move == True:
            pos_x = self.rect.center[0]
            pos_y = self.rect.center[1]
            pos_x += self.speed * self.x_speed
            pos_y -= self.speed * self.y_speed
            self.rect.center = (round(pos_x), round(pos_y))

            #change moving dir with hit the border
            if (self.rect.center[0] <= self.radius and self.x_speed <= 0)or (self.rect.center[0] >= WINDOW_WIDTH-self.radius and self.x_speed >= 0):
                self.x_speed *= -1
            if self.rect.center[1] <= self.radius and self.y_speed >= 0 :
                self.y_speed *= -1
            
            #check collison
            self.collison()

            #end the move when move to the bootom of the screen
            all_out = True
            if self.rect.center[1] > WINDOW_HEIGHT+40:
                self.is_move = False

            for sprite in self.ball:
                if sprite.rect.center[1] <= WINDOW_HEIGHT+40:
                    all_out = False
                    break
                    
            if all_out == True:
                if check_end(blk_weight) == False:
                    self.change_round()
                else:
                    self.game_status = 2

    def change_round(self):
        self.rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT-self.radius-1)
        self.kill_all_block_and_upgrade()
        round_update(blk_weight)
        create_blocks(blk_weight, self.round)
        generate_blocks(window_surface, blk_weight)
        self.org_board = deepcopy(blk_weight)
        self.round += 1


class Upgrade(pygame.sprite.Sprite):
    def __init__(self, pos, upgrade_type, upgrade_group, group) -> None:
        super().__init__(upgrade_group, group)
        self.upgrade_type = upgrade_type
        self.image = pygame.image.load("files/image/brickSpecial04.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(topleft = pos)

class Tmp_Balls(Balls):
    def __init__(self, radius, pos_x, pos_y, round, group, ball_group, block_group, upgrade_group, damage, game_status):
        super().__init__(radius, pos_x, pos_y, round ,group, ball_group, block_group, upgrade_group, game_status)
        self.image = pygame.image.load("files/image/sphere1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))
        self.damage = damage
    def update(self):
        if self.is_move == True:
            pos_x = self.rect.center[0]
            pos_y = self.rect.center[1]
            pos_x += self.speed * self.x_speed
            pos_y -= self.speed * self.y_speed
            self.rect.center = (round(pos_x), round(pos_y))

            #check collison
            self.collison()

            #change moving dir with hit the border
            if (self.rect.center[0] <= self.radius and self.x_speed <= 0)or (self.rect.center[0] >= WINDOW_WIDTH-self.radius and self.x_speed >= 0):
                self.x_speed *= -1
            if self.rect.center[1] <= self.radius and self.y_speed >= 0 :
                self.y_speed *= -1
                
            #end the move when move to the bootom of the screen
            all_out = True
            if self.rect.center[1] > WINDOW_HEIGHT+40:
                self.kill()
                
            for sprite in self.ball:
                if sprite.rect.center[1] <= WINDOW_HEIGHT+40:
                    all_out = False
                    break
                    
            if all_out == True:
                if check_end(blk_weight) == False:
                    ball.change_round()
                else:
                    ball.game_status = 2

        
class Barriers(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, score, block_group, group):
        super().__init__(group, block_group)
        self.x = x
        self.y = y
        self.width = 500 / 10  # Set maximum width of block = 1/10 of the window width
        self.height = self.width
        self.score = score
        self.color_pick()
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.block_group = block_group
        
    # Choose Different Texture at different score
    def color_pick(self):
        # color = (255, 255, 255)
        if (self.score < 5): # 1-10: Red
            # color = (255, 0, 0)
            self.image = pygame.image.load("files/image/red.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        elif (self.score < 10): # 11-20: Orange
            # color = (255, 128, 0)
            self.image = pygame.image.load("files/image/red2.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        elif (self.score < 15): # 21-30: Yellow
            # color = (255, 255, 0)
            self.image = pygame.image.load("files/image/orange.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        elif (self.score < 20): # 31-40: Green
            # color = (0, 255, 0)
            self.image = pygame.image.load("files/image/green.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        elif (self.score < 30): # 41-50: Cyan
            # color = (0, 255, 255)
            self.image = pygame.image.load("files/image/lightblue.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        elif (self.score < 40): #51-60: Blue
            # color = (0, 0, 255)
            self.image = pygame.image.load("files/image/blue.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        elif (self.score < 50): #61-70: Purple
            # color = (255, 0, 255)
            self.image = pygame.image.load("files/image/purple.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        else:
            # color = (0, 0, 0) # Otherwise: Black
            self.image = pygame.image.load("files/image/gray.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        return

# Generate Blocks on screen
def generate_blocks(window_surface, blk_weight):

    for i in range(len(blk_weight)):
        for j in range(len(blk_weight[i])):
            if blk_weight[i][j] == "X":
                Upgrade((i*50, j*50), random.choice(["add_damage", "ball_split"]), upgrade_group, all_sprites_gruop)
            elif (blk_weight[i][j] >= 1):
                Barriers(i * 50, j * 50, 50, 50, blk_weight[i][j], block_group, all_sprites_gruop)
    
    # for blocks in block_generate:
    #     Barriers.render(blocks, window_surface)



# Move blocks downward after each round ends
def round_update(blk_weight):
    for i in range(len(blk_weight)):
        for j in range(len(blk_weight[i])-1, -1, -1):
            if j == 0:
                blk_weight[i][j] = 0
            else:
                blk_weight[i][j] = blk_weight[i][j - 1]
                if isinstance(blk_weight[i][j], int):
                    if blk_weight[i][j] < 0:
                        blk_weight[i][j] = 0

# Random new blocks
def create_blocks(blk_weight, round):
    max_blk = 0
    # Avoid too many blocks in the beginning
    if round < 10:
        max_blk = 1
    elif round < 20:
        max_blk = 2
    elif round < 30:
        max_blk = 3
    elif round < 40:
        max_blk = 4
    elif round < 50:
        max_blk = 5
    elif round < 60:
        max_blk = 6
    elif round < 70:
        max_blk = 7
    elif round < 80:
        max_blk = 8
    else:
        max_blk = 9
    num_blk = random.randint(1, max_blk)

    # Avoid too high weighting on blocks at beginning
    max_weight = (round // 5) + 1

    copy_last = random.randint(0, 1) # 0: Not Copy Last Row, 1: Copy Pattern of Last Row
    has_upgrade = random.randint(0, 2)

    if (copy_last == 1 and round > 20):
        for i in range(len(blk_weight)):
            if isinstance(blk_weight[i][1], int):
                if (blk_weight[i][1] > 1):
                    blk_weight[i][0] = random.randint(1, max_weight)
    else:
        start_loc = random.randint(0, 9)
        if (start_loc + max_blk > 9):
            end_loc = 9
        else:
            end_loc = start_loc + max_blk
        for i in range(start_loc, end_loc + 1):
            blk_weight[i][0] = random.randint(1, max_weight)
    if has_upgrade == 1:
        upgrade_ypos = random.randint(0, len(blk_weight)-1)
        while blk_weight[upgrade_ypos][0] != 0:
            upgrade_ypos = random.randint(0, len(blk_weight)-1)
        blk_weight[upgrade_ypos][0] = "X"
    # print("before collison")   
    # for i in blk_weight:
    #     print(i)
    return blk_weight

def check_end(blk_weight):
    for a in range(len(blk_weight)):
        if blk_weight[a][9] > 0:
            return True
    
    return False

def bgm():
    pygame.mixer.init()
    # pygame.mixer.set_num_channels(2)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound("files/bgm/12 final battle.ogg"))

# calulate distance between two point
def distance(p1, p2):
    return ((abs(p1[0]-p2[0])**2 + abs(p1[1]-p2[1])**2)**1/2)



WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
FPS = 60
fi_pointer = "files/pointer.jpg"
degree = 90
radius = 20
clock = pygame.time.Clock()
round_ = 0
game_status = 0 # 0 = not yet start, 1 = start, 2 = end

# Define an array which store the block location and block weighting
blk_weight = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]

window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("GAME")
window_surface.fill(WHITE)



all_sprites_gruop = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
barriers_group = pygame.sprite.Group()
upgrade_group = pygame.sprite.Group()
tmp_ball_group = pygame.sprite.Group()

#ball
ball = Balls(radius, WINDOW_WIDTH/2, WINDOW_HEIGHT-26, round_, all_sprites_gruop, ball_group, block_group, upgrade_group, game_status)


# variable for change degree
is_degree_change = False
change_value = 0

# m_t = Timer(290, bgm)
# m_t.start()
start_time = time.time()
bgm()

#main game loop
while True:
    clock.tick(FPS)
    rad = degree/180 * math.pi

    # Background Music
    end_music = time.time()

    if end_music - start_time > 290:
        bgm()
        start_time = time.time()
        
    
    
    
    #move the pointer
    if is_degree_change == True:
        degree += change_value
        if degree > 150:
            degree = 150
        if degree < 30:
            degree = 30

    #to check if all the ball die
    all_end = True
    for sprite in ball_group:
        if sprite.is_move == True:
            all_end = False
            break

    
    # Detect Game Event
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Generate Blocks (TEST): Press Space Bar to move barriers downward
            if ball.game_status == 0:
                if event.key == pygame.K_SPACE:
                    round_update(blk_weight)
                    create_blocks(blk_weight, round_)
                    generate_blocks(window_surface, blk_weight)
                    ball.round += 1
                    ball.game_status = 1

            #change the angle 
            if ball.game_status == 1:
                if event.key == ord("a"):
                    if all_end == True:
                        is_degree_change = True
                        change_value = 2
                if event.key == ord("d"):
                    if all_end == True:
                        is_degree_change = True
                        change_value = -2
                #shoot
                if event.key == ord("w"):
                    if all_end == True:
                        ball.x_speed = cos(rad)
                        ball.y_speed = sin(rad)
                        ball.is_move = True

                #keyup to stop the pointer 
        if event.type == pygame.KEYUP:
            if ball.game_status == 1:
                is_degree_change = False
                change_value = 0

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Print Background
    bg = pygame.image.load("files/image/Full-Background.png").convert()
    bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    window_surface.blit(bg, (0, 0))

    if ball.game_status == 0:
        font = pygame.font.SysFont('Garamond', 35)
        message = font.render("Press Space to start the game!", False, (0, 0, 0))
        window_surface.blit(message, (40, WINDOW_HEIGHT // 2 - 50))
        pygame.display.update()

    if ball.game_status == 1:
        # Print Round Number
        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 20)
        text_gen = font.render('Round: ' + str(ball.round), False, (255, 255, 255))
        window_surface.blit(text_gen, (10, WINDOW_HEIGHT - 55))
        # Print ball damage
        text_dam = font.render("Damage:" + str(ball.damage), False, (255, 255, 255)) 
        window_surface.blit(text_dam, (10, WINDOW_HEIGHT - 30))

        all_sprites_gruop.update()
        all_sprites_gruop.draw(window_surface)

        if all_end == True:
            pygame.draw.line(window_surface, (255, 255, 255), (WINDOW_WIDTH/2, WINDOW_HEIGHT-radius), (WINDOW_WIDTH/2 + 100*cos(rad), (WINDOW_HEIGHT-radius)-100*sin(rad)), 3)

        # Print Block Number
        for i in range(len(blk_weight)):
            for j in range(len(blk_weight[i])):
                if isinstance(blk_weight[j][i], int):
                    if blk_weight[j][i] > 0:
                        block_score = font.render(str(blk_weight[j][i]), False, (255, 255, 255))
                        window_surface.blit(block_score, (j * 50 + 22.5, i * 50 + 10))
        
        if (check_end == True):
            break
        pygame.display.update()
    
    if ball.game_status == 2:
        font = pygame.font.SysFont('Garamond', 50)
        message = font.render("Game Over !", False, (0, 0, 0))
        round_end = font.render('Round: ' + str(ball.round), False, (0, 0, 0))
        window_surface.blit(message, (60, WINDOW_HEIGHT // 2 - 30))
        window_surface.blit(round_end, (60, WINDOW_HEIGHT // 2 + 10))
        pygame.display.update()


