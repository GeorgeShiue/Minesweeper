import pygame
import random

WIDTH = 600
HEIGHT = 600
BLOCK_SIZE = 30
FONT_SIZE = 26
BLOCK_AMOUNT = int(HEIGHT // BLOCK_SIZE)
MINE_PROBABILITY = 0.15
SPECIAL_BLOCK_PROBABILITY = 0.05

# class Mine():
#     pass
# class Flag():
#     pass

# 初始化Pygame
pygame.init()
# 建立遊戲視窗
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("踩地雷")
# 載入字體
font = pygame.font.SysFont("Arial", FONT_SIZE)

class Block():
    def __init__(self, x, y, i, j):
        self.x = x
        self.y = y
        self.lift_up = False
        self.flag = False
        self.mine = False
        self.special_block = False
        self.hide_number = False
        self.check_list = [(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]
        self.mine_around = 0
        self.recurssion_time = 0
    
    def draw_number(self, background = "white"):
        text = font.render(str(self.mine_around), True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        if background == "white":
            pygame.draw.rect(screen, (255, 255, 255),(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        else:
            pygame.draw.rect(screen, (0, 255, 0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        screen.blit(text, text_rect)

class Map():
    def __init__(self, i_, j_):
        self.blocks = [[0 for x in range(BLOCK_AMOUNT)] for y in range(BLOCK_AMOUNT)]
        self.mines = self.create_map(i_, j_)
        self.spaces = BLOCK_AMOUNT ** 2 - self.mines
        print(self.mines, self.spaces)
        self.count_lift_up = 0

        self.check_mine_around(i_, j_)
        self.blocks[i_][j_].lift_up = True
        self.count_lift_up += 1
        if self.blocks[i_][j_].mine_around == 0:
            self.lift_0_around(i_, j_)

    def create_map(self, i_, j_):
        count_mine = 0
        check_list = [(i_-1, j_-1), (i_-1, j_), (i_-1, j_+1), (i_, j_-1), (i_, j_), (i_, j_+1), (i_+1, j_-1), (i_+1, j_), (i_+1, j_+1)]
        for i in range(HEIGHT // BLOCK_SIZE):
            for j in range(WIDTH // BLOCK_SIZE):
                block = Block(j * BLOCK_SIZE + BLOCK_SIZE//2, i * BLOCK_SIZE + BLOCK_SIZE//2, i, j)
                if random.random() < MINE_PROBABILITY:
                    no_mine = False
                    for index in check_list:
                        if i == index[0] and j == index[1]:
                            no_mine = True
                    if no_mine == False:
                        block.mine = True
                        count_mine += 1
                if random.random() < SPECIAL_BLOCK_PROBABILITY:
                    if (i_, j_) != (i, j) and block.mine == False:
                        block.special_block = True
                        #print(i, j)
                self.blocks[i][j] = block
        return count_mine
    
    def lift_0_around(self, i_, j_):
        for index in self.blocks[i_][j_].check_list:
            if 0 <= index[0] <= BLOCK_AMOUNT - 1 and 0 <= index[1] <= BLOCK_AMOUNT - 1:
                if self.blocks[index[0]][index[1]].lift_up == False and self.blocks[index[0]][index[1]].mine == False:
                    self.count_lift_up += 1
                    self.blocks[index[0]][index[1]].lift_up = True
                    self.check_mine_around(index[0], index[1])
                    if self.blocks[index[0]][index[1]].special_block == True:
                        self.hide_5_number()
                    if self.blocks[index[0]][index[1]].mine_around == 0:
                        self.lift_0_around(index[0], index[1])
    
    def check_mine_around(self, i_, j_):
        total = 0
        for index in self.blocks[i_][j_].check_list:
            if 0 <= index[0] <= BLOCK_AMOUNT - 1 and 0 <= index[1] <= BLOCK_AMOUNT - 1:
                if self.blocks[index[0]][index[1]].mine == True:
                    total += 1
        self.blocks[i_][j_].mine_around = total

    def show_all_mine(self):
        for i in range(BLOCK_AMOUNT):
            for j in range(BLOCK_AMOUNT):
                if self.blocks[i][j].mine == True:
                    pygame.draw.rect(screen, (255, 0, 0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def hide_5_number(self):
        count = 0
        #print("hide index: ")
        while (count < 5):
            number = random.randint(0, BLOCK_AMOUNT ** 2 - 1)
            i = number // BLOCK_AMOUNT
            j = number % BLOCK_AMOUNT
            if self.blocks[i][j].mine == False and self.blocks[i][j].special_block == False and self.blocks[i][j].hide_number == False and self.blocks[i][j].lift_up == True:
                #print(i,j)
                self.blocks[i][j].hide_number = True
                count += 1

def draw_frame():
    for i in range(BLOCK_AMOUNT):
        for j in range(BLOCK_AMOUNT):
            rect = pygame.Rect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, (0, 150, 200), rect, 1)

def draw_game_start():
    rect_surface = pygame.Surface((120, 60))
    rect = pygame.Rect(0, 0, 120, 60)
    pygame.draw.rect(rect_surface, (255, 255, 255), rect)
    screen.blit(rect_surface, (240, 270))
    game_start_text = font.render("Click to start", True, (0, 0, 255))
    game_start_rect = game_start_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(game_start_text, game_start_rect)

def draw_game_over(result):
    rect_surface = pygame.Surface((120, 60))
    rect = pygame.Rect(0, 0, 120, 60)
    pygame.draw.rect(rect_surface, (255, 255, 255), rect)
    screen.blit(rect_surface, (240, 270))
    if result == "Lose":
        game_over_text = font.render("You Lose", True, (0, 0, 255))
    elif result == "Win":
        game_over_text = font.render("You Win!", True, (0, 0, 255))
    game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(game_over_text, game_over_rect)

game_init = True
game_over = False
result = 'None'
running = True
while running:
    #遊戲初始化
    if game_init == True:
        screen.fill((192, 192, 192))
        draw_frame()
        draw_game_start()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                y = y // BLOCK_SIZE
                x = x // BLOCK_SIZE
                if event.button == 1:
                    map = Map(y,x)
                game_init = False
        continue
    
    #遊戲結束畫面
    if game_over == True:
        map.show_all_mine()
        draw_frame()
        draw_game_over(result)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_over = False
                game_init = True
                result = 'None'
        continue

    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            i = y // BLOCK_SIZE
            j = x // BLOCK_SIZE
            if event.button == 1 and map.blocks[i][j].lift_up == False:
                map.check_mine_around(i,j)
                map.blocks[i][j].lift_up = True
                map.count_lift_up += 1
                if map.count_lift_up == map.spaces:
                    game_over = True
                    result = 'Win'
                if map.blocks[i][j].mine_around == 0 and map.blocks[i][j].mine == False:
                    map.lift_0_around(i, j)
                if map.blocks[i][j].special_block == True:
                    map.hide_5_number()
            if event.button == 3 and map.blocks[i][j].lift_up == False:
                if map.blocks[i][j].flag == False:
                    map.blocks[i][j].flag = True
                else:
                    map.blocks[i][j].flag = False

    # 更新畫面
    screen.fill((192, 192, 192))
    for i in range(BLOCK_AMOUNT):
        for j in range(BLOCK_AMOUNT):
            if map.blocks[i][j].lift_up == True:
                if map.blocks[i][j].mine == True:
                    game_over = True
                    result = "Lose"
                elif map.blocks[i][j].special_block == True:
                    map.blocks[i][j].draw_number("green")
                elif map.blocks[i][j].hide_number == False:
                    map.blocks[i][j].draw_number()
                elif map.blocks[i][j].hide_number == True:
                    pygame.draw.rect(screen, (255, 255, 255),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif map.blocks[i][j].flag == True:
                pygame.draw.rect(screen, (0, 0, 0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif map.blocks[i][j].flag == False:
                pygame.draw.rect(screen, (192, 192, 192),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            
            # if map.blocks[i][j].special_block == True:
            #     pygame.draw.rect(screen, (0, 255, 0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            # if map.blocks[i][j].special_block == True:
            #     pygame.draw.rect(screen, (0, 255, 0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            #     map.check_mine_around(i,j)
            #     map.blocks[i][j].draw_number()
    draw_frame()
    pygame.display.update()

pygame.quit()