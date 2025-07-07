import pygame
import time
import numpy as np

from numba import njit

# Parameters
CELLS_SIZE = 3
GRID_WIDTH = 300
GRID_HEIGHT = 200
FPS = 10

# Game of Life rules

NEIGHBOURHOOD_CLASSIC = np.array([(-1,  1), (0, 1), (1, 1),
                         (-1,  0)        , (1, 0),
                         (-1, -1), (0,-1), (1,-1)], dtype=np.int32)

NEIGHBOURHOOD_BUG = np.array([(-5,  5), (-4, 5), (-3, 5), (-2, 5), (-1, 5), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),
                     (-5,  4), (-4, 4), (-3, 4), (-2, 4), (-1, 4), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
                     (-5,  3), (-4, 3), (-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
                     (-5,  2), (-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
                     (-5,  1), (-4, 1), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
                     (-5,  0), (-4, 0), (-3, 0), (-2, 0), (-1, 0)        , (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
                     (-5,  -1), (-4, -1), (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1), (5, -1),
                     (-5,  -2), (-4, -2), (-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2), (4, -2), (5, -2),
                     (-5,  -3), (-4, -3), (-3, -3), (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3), (4, -3), (5, -3),
                     (-5,  -4), (-4, -4), (-3, -4), (-2, -4), (-1, -4), (0, -4), (1, -4), (2, -4), (3, -4), (4, -4), (5, -4),
                     (-5,  -5), (-4, -5), (-3, -5), (-2, -5), (-1, -5), (0, -5), (1, -5), (2, -5), (3, -5), (4, -5), (5, -5)], dtype = np.int32)

RADIUS = 5


def circularBoundary(radius):
    coordinates = [(x,y) for x in range(-radius,radius+1) for y in range(-radius,radius+1) if (x**2 + y**2 <= radius**2) == True]
    return np.array(coordinates, dtype = np.int32)

circular = circularBoundary(RADIUS)
 

@njit
def nextStage(cells): 
    height, width = cells.shape
    next_stage = np.zeros((height, width), dtype = np.uint8)  

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            count = sum([cells[y+i][x+j] for j,i in NEIGHBOURHOOD_BUG])      
            # if (count == 3 and cells[y,x] == 0) or (count in (2,3) and cells[y][x] == 1):
            #     next_stage[y][x] = 1

            if count >= 34 and count <= 45:
                next_stage[y][x] = 1

    return next_stage


# Grid

def draw_grid(screen, cells, offset_x, offset_y):
    screen.fill((10,10,10))
    width, heigth = cells.shape

    for y in range(heigth):
        for x in range(width):
            if cells[x, y]:
                px = (x - offset_x) * CELLS_SIZE
                py = (y - offset_y) * CELLS_SIZE
                if 0 <= px < screen.get_width() and 0 <= py < screen.get_height():
                    pygame.draw.rect(screen, (255,255,255), (px, py, CELLS_SIZE - 1, CELLS_SIZE - 1))

    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * CELLS_SIZE, GRID_HEIGHT * CELLS_SIZE))
    pygame.display.set_caption("Game Of Life")
    
    clock = pygame.time.Clock()

    cells = np.random.choice([0, 1], size=(GRID_WIDTH -1, GRID_HEIGHT -1), p=[.8, .2])

    offset_x = 0 
    offset_y = 0

    running = False
    pygame.key.set_repeat(10,50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                elif event.key == pygame.K_UP:
                    offset_y -= 0.5
                elif event.key == pygame.K_DOWN:
                    offset_y += 0.5
                elif event.key == pygame.K_RIGHT:
                    offset_x += 0.5
                elif event.key == pygame.K_LEFT:
                    offset_x -= 0.5
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[0] // CELLS_SIZE][pos[1] // CELLS_SIZE] ^= 1   # toggle between 0 and 1
                draw_grid(screen, cells, offset_x, offset_y)
            
                         


        if running:
            cells = nextStage(cells)
        
        draw_grid(screen, cells, offset_x, offset_y)
        clock.tick(FPS)
        time.sleep(0.001)


if __name__ == "__main__":
    main()