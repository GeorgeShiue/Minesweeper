import pygame
import random

# 定義一些常數
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20
MINE_PROBABILITY = 0.2
FONT_SIZE = 24

# 初始化Pygame
pygame.init()

# 建立遊戲視窗
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("踩地雷遊戲")

# 載入字體
font = pygame.font.SysFont("Arial", FONT_SIZE)

# 生成地圖
map_data = []
for i in range(SCREEN_HEIGHT // BLOCK_SIZE):
    row = []
    for j in range(SCREEN_WIDTH // BLOCK_SIZE):
        if random.random() < MINE_PROBABILITY:
            row.append(9)  # 9 代表地雷
        else:
            row.append(0)
    map_data.append(row)

# 計算每個方塊周圍地雷的數量
for i in range(len(map_data)):
    for j in range(len(map_data[i])):
        if map_data[i][j] == 9:
            continue
        count = 0
        for ii in range(max(0, i-1), min(len(map_data), i+2)):
            for jj in range(max(0, j-1), min(len(map_data[i]), j+2)):
                if map_data[ii][jj] == 9:
                    count += 1
        map_data[i][j] = count

# 遊戲主迴圈
game_over = False
while not game_over:
    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            i = y // BLOCK_SIZE
            j = x // BLOCK_SIZE
            if map_data[i][j] == 9:
                game_over = True
            else:
                map_data[i][j] = -1

    # 更新畫面
    screen.fill((255, 255, 255))
    for i in range(len(map_data)):
        for j in range(len(map_data[i])):
            if map_data[i][j] == -1:
                pygame.draw.rect(screen, (200, 200, 200),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif map_data[i][j] == 9:
                pygame.draw.rect(screen, (255, 0, 0),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif map_data[i][j] > 0:
                text = font.render(str(map_data[i][j]), True, (0, 0, 0))
                text_rect = text.get_rect(center=(j*BLOCK_SIZE + BLOCK_SIZE//2, i*BLOCK_SIZE + BLOCK_SIZE//2))
                pygame.draw.rect(screen, (200, 200, 200),(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                screen.blit(text, text_rect)
    pygame.display.update()

# 顯示結束畫面
if game_over:
    screen.fill((255, 255, 255))
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.update()

pygame.quit()