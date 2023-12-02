import pygame
import random

WIDTH = 600
HEIGHT = 600
BLOCK_SIZE = 30
FONT_SIZE = 26
BLOCK_AMOUNT = int(HEIGHT // BLOCK_SIZE)
MINE_PROBABILITY = 0.2

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
        self.check_list = [(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]
        self.mine_arround = 0

    def check_mine_around(self):
        for index in self.check_list:
            if 0 <= index[0] <= BLOCK_AMOUNT - 1 and 0 <= index[1] <= BLOCK_AMOUNT - 1:
                if map[index[0]][index[1]].mine == True:
                    self.mine_arround += 1
    
    def draw_number(self):
        text = font.render(str(self.mine_arround), True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        pygame.draw.rect(screen, (255, 255, 255),(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        screen.blit(text, text_rect)

class Map():
    pass

map = [[0 for x in range(BLOCK_AMOUNT)] for y in range(BLOCK_AMOUNT)]
def create_map(i_, j_):
    count_mine = 0
    for i in range(HEIGHT // BLOCK_SIZE):
        for j in range(WIDTH // BLOCK_SIZE):
            block = Block(j * BLOCK_SIZE + BLOCK_SIZE//2, i * BLOCK_SIZE + BLOCK_SIZE//2, i, j)
            if random.random() < MINE_PROBABILITY:
                block.mine = True
                count_mine += 1
            if i == i_ and j == j_:
                block.mine = False
            map[i][j] = block
    return count_mine

def show_all_mine():
    for i in range(BLOCK_AMOUNT):
        for j in range(BLOCK_AMOUNT):
            if map[i][j].mine == True:
                pygame.draw.rect(screen, (255, 0, 0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_frame():
    for i in range(BLOCK_AMOUNT):
        for j in range(BLOCK_AMOUNT):
            rect = pygame.Rect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

def draw_game_over(result):
    rect_surface = pygame.Surface((120, 60))
    rect = pygame.Rect(0, 0, 120, 60)
    pygame.draw.rect(rect_surface, (255, 255, 255), rect)
    screen.blit(rect_surface, (240, 270))
    if result == "Lose":
        game_over_text = font.render("Game Over", True, (0, 0, 255))
    elif result == "Win":
        game_over_text = font.render("You Win!", True, (0, 0, 255))
    game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(game_over_text, game_over_rect)

mine = 0
space = 0
count_lift_up = 0
first_click = False
game_over = False
result = 'None'
running = True
while running:
    if first_click == False:
        screen.fill((192, 192, 192))
        draw_frame()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                y = y // BLOCK_SIZE
                x = x // BLOCK_SIZE
                if event.button == 1:
                    mine = create_map(y,x)
                    space = BLOCK_AMOUNT ** 2 - mine
                    map[y][x].check_mine_around()
                    map[y][x].lift_up = True
                    count_lift_up += 1
                first_click = True
        continue

    if game_over == True:
        show_all_mine()
        draw_frame()
        draw_game_over(result)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_over = False
                first_click = False
                result = 'None'
                mine = 0
                space = 0
                count_lift_up = 0
        continue

    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            i = y // BLOCK_SIZE
            j = x // BLOCK_SIZE
            if event.button == 1 and map[i][j].lift_up == False:
                map[i][j].check_mine_around()
                map[i][j].lift_up = True
                count_lift_up += 1
                if count_lift_up == space:
                    game_over = True
                    result = "Win"
            if event.button == 3 and map[i][j].lift_up == False:
                if map[i][j].flag == False:
                    map[i][j].flag = True
                else:
                    map[i][j].flag = False

    # 更新畫面
    screen.fill((192, 192, 192))
    for i in range(BLOCK_AMOUNT):
        for j in range(BLOCK_AMOUNT):
            if map[i][j].lift_up == True:
                if map[i][j].mine == True:
                    game_over = True
                    result = "Lose"
                else:
                    map[i][j].draw_number()
            elif map[i][j].flag == True:
                pygame.draw.rect(screen, (0, 0, 0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif map[i][j].flag == False:
                pygame.draw.rect(screen, (192, 192, 192),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    draw_frame()
    pygame.display.update()

pygame.quit()