import pygame
import time
import numpy as np

# Parameters
CELLS_SIZE = 2
GRID_WIDTH = 300
GRID_HEIGHT = 200
FPS = 10

# Game of Life rules

NEIGHBOURHOOD_CLASSIC = [(-1,  1), (0, 1), (1, 1),
                         (-1,  0)        , (1, 0),
                         (-1, -1), (0,-1), (1,-1)]

NEIGHBOURHOOD_BUG = [(-5,  5), (-4, 5), (-3, 5), (-2, 5), (-1, 5), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),
                     (-5,  4), (-4, 4), (-3, 4), (-2, 4), (-1, 4), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
                     (-5,  3), (-4, 3), (-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
                     (-5,  2), (-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
                     (-5,  1), (-4, 1), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
                     (-5,  0), (-4, 0), (-3, 0), (-2, 0), (-1, 0)        , (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
                     (-5,  -1), (-4, -1), (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1), (5, -1),
                     (-5,  -2), (-4, -2), (-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2), (4, -2), (5, -2),
                     (-5,  -3), (-4, -3), (-3, -3), (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3), (4, -3), (5, -3),
                     (-5,  -4), (-4, -4), (-3, -4), (-2, -4), (-1, -4), (0, -4), (1, -4), (2, -4), (3, -4), (4, -4), (5, -4),
                     (-5,  -5), (-4, -5), (-3, -5), (-2, -5), (-1, -5), (0, -5), (1, -5), (2, -5), (3, -5), (4, -5), (5, -5)]  

RADIUS = 5


def circularBoundary(radius):
    coordinates = [(x,y) for x in range(-radius,radius+1) for y in range(-radius,radius+1) if (x**2 + y**2 <= radius**2) == True]
    return coordinates


 



def nextGeneration(live_cells):
    neighbours = {}

    for (x, y) in live_cells:
        for dx, dy in circularBoundary(8):
            neighbour = (x + dx, y + dy) 
            try:
                neighbours[neighbour] += 1 
            except KeyError:
                neighbours[neighbour] = 1
    
    new_live_cells = set()
    # for cell, count in neighbours.items():  # Classic
    #     if count == 3 or (count == 2 and cell in live_cells):
    #         new_live_cells.add(cell)

    # for cell, count in neighbours.items():  # Bug
    #     if count >= 17 and count <= 22: 
    #         new_live_cells.add(cell)

    for cell, count in neighbours.items():  # Circular
        if count >= 2 and count <= 5: 
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



    cells = np.random.choice([0, 1], size=(GRID_WIDTH-1, GRID_HEIGHT-1), p=[.8, .2])

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
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                print(pos)
                live_cells.add((pos[1] // 15, pos[0] // 15))         # doesn't work properly
                draw_grid(screen,live_cells, offset_x, offset_y)
            
                         


        if running:
            live_cells = nextGeneration(live_cells)
        
        draw_grid(screen, live_cells, offset_x, offset_y)
        clock.tick(FPS)
        time.sleep(0.0001)


if __name__ == "__main__":
    main()