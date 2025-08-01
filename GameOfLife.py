import pygame
import time
import numpy as np

from numba import njit

# Parameters
CELLS_SIZE = 2
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

def rectangularBoundary(radius):
    coordinates = [(x,y) for x in range(-radius,radius+1) for y in range(-radius,radius+1)]
    return np.array(coordinates, dtype=np.int32)

def circularBoundary(radius1, radius2=0):
    radius1, radius2 = max(radius1, radius2), min(radius1, radius2)
    coordinates = [(x,y) for x in range(-radius1,radius1+1) for y in range(-radius1,radius1+1) if (x**2 + y**2 <= radius1**2) and (x**2 + y**2 >= radius2**2)]
    return np.array(coordinates, dtype = np.int32)


# circular = circularBoundary(RADIUS)
circularClick = circularBoundary(5)

### An attepmt to make cell-like pattern
circular1 = circularBoundary(7, 4)
circular2 = circularBoundary(4)
# print(circular1)
print(circular2)


### Othet boundaries
circular3 = np.concatenate((circularBoundary(8,7),circularBoundary(5,3),circularBoundary(1)))
circular4 = np.concatenate((circularBoundary(7,6), circularBoundary(3,1)))

rectangular = rectangularBoundary(4)


@njit
def nextStage(cells): 
    height, width = cells.shape
    next_stage = np.zeros((height, width), dtype = np.uint8) 
    # count1Values = []
    # count2Values = [] 



    for y in range(1, height - 1):
        for x in range(1, width - 1):
            ### Classical Game of Life ----------------------------------------------------------------- ###

            # count = sum([cells[y+i][x+j] for j,i in NEIGHBOURHOOD_CLASSIC])      
            # if (count == 3 and cells[y,x] == 0) or (count in (2,3) and cells[y][x] == 1):
            #     next_stage[y][x] = 1

            # if count >= 34 and count <= 45:
            #     next_stage[y][x] = 1


            ### Attepmt to make a bug pattern ---------------------------------------------------------- ###

            # count = sum([cells[y+i][x+j] for j,i in NEIGHBOURHOOD_BUG])      

            # if count >= 30 and count <= 45:  # Stars ?
            #     next_stage[y][x] = 1

            # if count >= 0 and count <= 33:
            #     next_stage[y,x] = 0
            # if count >= 30 and count <= 45:  
            #     next_stage[y][x] = 1
            # if count >= 58 and count <= 121:
            #     next_stage[y,x] = 0
            


            ### Attempt to make a cell-like pattern ---------------------------------------------------- ###

            count1 = sum([cells[y+i][x+j] for j,i in circular1]) 
            count2 = sum([cells[y+i][x+j] for j,i in circular2]) 

            # count1Values.append(count1)
            # count2Values.append(count2)

            # if count1 >= 19  and count1 <= 21:           # cells_like 1
            #     next_stage[y,x] = 1
            # elif count2 >= 22  and count2 <= 33:
            #     next_stage[y,x] = 1
        

            # if count1 >= 17  and count1 <= 19:           # cells_like 2
            #     next_stage[y,x] = 1
            # elif count2 >= 21  and count2 <= 40:
            #     next_stage[y,x] = 1


            # if count1 >= 19  and count1 <= 21:           # cells_like 3  !!!
            #     next_stage[y,x] = 1
            # elif count2 >= 23  and count2 <= 40:
            #     next_stage[y,x] = 1

            # if count1 >= 15  and count1 <= 17:           # cells_like 4
            #     next_stage[y,x] = 1
            # elif count2 >= 19  and count2 <= 35:
            #     next_stage[y,x] = 1

            # -------------------------------------------------------------------------------------
            '''
            It would be usefull to calculate the distribuition of values for count1 and count2
            '''

            # if count1 >= 23 and count1 <= 26:           # cells_like 5 ???
            #     next_stage[y,x] = 1
            # elif count2 >= 18 and count2 <= 21:
            #     next_stage[y,x] = 1


            if count1 >= 25 and count1 <= 28:           
                next_stage[y,x] = 1
            elif count2 >= 17 and count2 <= 21:
                next_stage[y,x] = 1
            
            
            # if count1 >= 37 and count1 <= 50:    # ?????
            #     next_stage[y,x] = 1
            # elif count2 >= 34 and count2 <= 35:  # the range should be kept at 1. The higher this variable is the lower the rate of growth.
            #     next_stage[y,x] = 1
            # elif count1 >= 27 and count1 <= 31:           
            #     next_stage[y,x] = 1


            # -------------------------------------------------------------------------------------

            # if count1 >= 19  and count1 <= 21:           # cells_like 6
            #     next_stage[y,x] = 1
            # elif count2 >= 22  and count2 <= 40:
            #     next_stage[y,x] = 1

            # if count1 >= 18  and count1 <= 21:           # cells_like 7
            #     next_stage[y,x] = 1 
            # elif count2 >= 21  and count2 <= 36:
            #     next_stage[y,x] = 1

            # if count1 >= 19  and count1 <= 21:             # an example of a stable solution
            #     next_stage[y,x] = 1
            # elif count2 >= 23  and count2 <= 49:
            #     next_stage[y,x] = 1


            # if count1 >= 19  and count1 <= 21:             
            #     next_stage[y,x] = 1
            # elif count2 >= 22  and count2 <= 40:
            #     next_stage[y,x] = 1


            
            # if count1 >= 19  and count1 <= 24:             
            #     next_stage[y,x] = 1
            # elif count2 >= 19  and count2 <= 27:
            #     next_stage[y,x] = 1


            # if count1 >= 16  and count1 <= 18:             
            #     next_stage[y,x] = 1
            # elif count2 >= 21  and count2 <= 40:
            #     next_stage[y,x] = 1


            # if count1 >= 19  and count1 <= 21:          
            #     next_stage[y,x] = 1
            # elif count2 >= 18  and count2 <= 35:
            #     next_stage[y,x] = 1
    

            ### ---------------------------------------------------------------------------------------- ###

            ### Trying other boundary ------------------------------------------------------------------ ###
            # count3 = sum([cells[y+i][x+j] for j,i in circular3])
            # count4 = sum([cells[y+i][x+j] for j,i in circular4])

            # if count3 >= 22 and count3 <= 29:                             # ???
            #     next_stage[y,x] = 1 
            # elif count4 >= 37 and count4 <= 38:
            #     next_stage[y,x] = 1


            # if count3 >= 21 and count3 <= 28:                                # ???
            #     next_stage[y,x] = 1 
            # elif count4 >= 38 and count4 <= 38:
            #     next_stage[y,x] = 1


            ### Rectangular boundary ------------------------------------------------------------------- ###
            # count5 = sum([cells[y+i][x+j] for j,i in rectangular])
            # count1 = sum([cells[y+i][x+j] for j,i in circular1]) 

            # if count5 >= 25 and count5 <= 40:                                   # ???
            #     next_stage[y,x] = 1
            # elif count1 >= 13 and count1 <= 14:
            #     next_stage[y,x] = 1
            

            ### ---------------------------------------------------------------------------------------- ###



    return next_stage #, count1Values, count2Values


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
    icon = pygame.image.load("image.png")
    pygame.display.set_icon(icon)
    
    clock = pygame.time.Clock()

    cells = np.random.choice([0, 1], size=(GRID_WIDTH -1, GRID_HEIGHT -1), p=[.8, .2])

    offset_x = 0 
    offset_y = 0
    
    # print(f"--- {cells.size * cells[0].size} cells ---")
    running = False
    pygame.key.set_repeat(10,50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # distribuitionOfCount1 = sum(count1Values) / len(count1Values)
                # distribuitionOfCount2 = sum(count2Values) / len(count2Values)
                # print(f"{distribuitionOfCount1:.2f} is an average value for count1")
                # print(f"{distribuitionOfCount2:.2f} is an average value for count2")
                return 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    # distribuitionOfCount1 = sum(count1Values) / len(count1Values)
                    # distribuitionOfCount2 = sum(count2Values) / len(count2Values)
                    # print(f"{distribuitionOfCount1:.2} is an average value for count1")
                    # print(f"{distribuitionOfCount2:.2} is an average value for count2")
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
                for x,y in circularClick:
                    try:
                        cells[(pos[0] // CELLS_SIZE) + y][(pos[1] // CELLS_SIZE) + x] ^= 1   # toggle between 0 and 1
                    except IndexError:
                        pass
                draw_grid(screen, cells, offset_x, offset_y)
            
                         

        if running:
            cells = nextStage(cells)
        
        draw_grid(screen, cells, offset_x, offset_y)
        clock.tick(FPS)
        time.sleep(0.001)
    







if __name__ == "__main__":
    main()