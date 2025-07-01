import time
import numpy as np 
import pygame

COLOUR_BG = (10,10,10)
COLOUR_GRID = (40,40,40)
COLOUR_DIE_NEXT = (170,170,170)
COLOUR_ALIVE_NEXT = (255,255,255)

def update(screen, cells, size, with_progress=False):
    updated_cells = np.empty((cells.shape[0], cells.shape[1])) # empty initiates the array of arbitrary value

    for row, col in np.ndindex(cells.shape): # ndiindex iterates through an array
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row,col] # this controls the rule of summation of alive cells. This way, the game considers areas of the size of a circle
        colour = COLOUR_BG if cells[row,col] == 0 else COLOUR_ALIVE_NEXT


        if cells[row, col] == 1: # implementation of rules
            if alive < 2 or alive > 3:
                if with_progress:
                    colour = COLOUR_DIE_NEXT
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    colour = COLOUR_ALIVE_NEXT
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    colour = COLOUR_ALIVE_NEXT

        pygame.draw.rect(screen, colour, (col * size, row * size, size - 1, size - 1)) # question to the parameters passed to rect

    return updated_cells   


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    cells = np.zeros((60,80))
    screen.fill(COLOUR_GRID)
    update(screen, cells, 10)

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
                    update(screen, cells, 10)
                    pygame.display.update()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()
            
            screen.fill(COLOUR_GRID)

            if running:
                cells = update(screen, cells, 10, with_progress=True)
                pygame.display.update()

            time.sleep(0.001)


if __name__ == "__name__":
    main()