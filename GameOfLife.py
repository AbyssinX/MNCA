import time
import numpy as np 
import pygame

COLOUR_BG = (10,10,10)
COLOUR_GRID = (0,0,0)
COLOUR_DIE_NEXT = (170,170,170)
COLOUR_ALIVE_NEXT = (255,255,255)

SIZE = 10
RADIUS = 1



NEIGHBOURHOOD = [(-1,  1), (0, 1), (1, 1),
                 (-1,  0), (0, 0), (1, 0),
                 (-1, -1), (0,-1), (1,-1)]

# def generateRandom():


def update(screen, cells, alive_cells, size, with_progress=False):
    # next_gen = []
    

    for row,col in alive_cells:
        colour = COLOUR_BG if cells[row,col] == 0 else COLOUR_ALIVE_NEXT
        for dx, dy in NEIGHBOURHOOD:
            row,col = row + dx, col + dy
            
            alive = np.sum(cells[row-1:row+2, col-1:col+2]) - 1

            if alive < 2 or alive > 3:
                    if with_progress:
                        colour = COLOUR_DIE_NEXT
            elif 2 <= alive <= 3:
                # next_gen[row, col] = 1
                if with_progress:
                    colour = COLOUR_ALIVE_NEXT
    
    pygame.draw.rect(screen, colour, (col * size, row * size, size - 1, size - 1))




    # for row, col in np.ndindex(cells.shape): # ndiindex iterates through an array
    #     colour = COLOUR_BG if cells[row,col] == 0 else COLOUR_ALIVE_NEXT
    #     alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row,col] 

    #     # alive = circularBoundary(cells[row-1:row+2, col-1:col+2], row, col) - cells[row,col] 

    #     if cells[row, col] == 1: # implementation of rules of The Game of Life
    #         if alive < 2 or alive > 3:
    #             if with_progress:
    #                 colour = COLOUR_DIE_NEXT
    #         elif 2 <= alive <= 3:
    #             updated_cells[row, col] = 1
    #             if with_progress:
    #                 colour = COLOUR_ALIVE_NEXT
    #     else:
    #         if alive == 3:
    #             updated_cells[row, col] = 1
    #             if with_progress:
    #                 colour = COLOUR_ALIVE_NEXT

    #     pygame.draw.rect(screen, colour, (col * size, row * size, size - 1, size - 1)) # question to the parameters passed to rect

    # return updated_cells


































def main():
    pygame.init()
    
    screen = pygame.display.set_mode((1000, 700))

    

    cells = np.random.choice([0, 1], size=(120,160), p=[.9, .1])

    alive_cells = set()
    for row,col in np.ndindex(cells.shape):
        if cells[row,col] == 1:
            alive_cells.add((row,col))

   
    screen.fill(COLOUR_GRID)
    update(screen, cells, alive_cells, SIZE)

    pygame.display.flip()   
    pygame.display.update() 

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, alive_cells, SIZE)
                    pygame.display.update()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, alive_cells, SIZE)
                pygame.display.update()
        

        if running:
            cells = update(screen, cells, alive_cells, SIZE, with_progress=True)
            pygame.display.update()

        time.sleep(0.01)
















main()





























# def getRows(matrix):
#     return matrix.size

# def getCols(matrix):
#     return matrix[0].size


# def circularBoundary(matrix, row, col):
#     counter = 0
#     for r in range(getRows(matrix)):
#         for c in range(getCols(matrix)):
#             if (r-row)^2 + (c-col)^2 <= RADIUS^2:
#                 counter += 1
#     return counter