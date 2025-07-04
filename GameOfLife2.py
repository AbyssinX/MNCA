import pygame
import sys
import numpy as np

# Parameters
CELLS_SIZE = 3
GRID_WIDTH = 300
GRID_HEIGHT = 220
FPS = 10

# Game of Life rules

NEIGHBOURHOOD = [(-1,  1), (0, 1), (1, 1),
                 (-1,  0)        , (1, 0),
                 (-1, -1), (0,-1), (1,-1)]


def nextGeneration(live_cells):
    neighbours = {}

    for (x, y) in live_cells:
        for dx, dy in NEIGHBOURHOOD:
            neighbour = (x + dx, y + dy) 
            try:
                neighbours[neighbour] += 1 
            except KeyError:
                neighbours[neighbour] = 1
    
    new_live_cells = set()
    for cell, count in neighbours.items():
        if count == 3 or (count == 2 and cell in live_cells):
            new_live_cells.add(cell)

    return new_live_cells


# Grid

def draw_grid(screen, live_cells, offset_x, offset_y):
    screen.fill((10,10,10))
    for (x, y) in live_cells:
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



    cells = np.random.choice([0, 1], size=(GRID_WIDTH-1, GRID_HEIGHT-1), p=[.9, .1])

    live_cells = set()
    for row,col in np.ndindex(cells.shape):
        if cells[row,col] == 1:
            live_cells.add((row,col))


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
                         


        if running:
            live_cells = nextGeneration(live_cells)
        
        draw_grid(screen, live_cells, offset_x, offset_y)
        clock.tick(FPS)


if __name__ == "__main__":
    main()