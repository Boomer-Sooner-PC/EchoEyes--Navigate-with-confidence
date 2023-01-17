import pygame
import math
from colour import Color
SIZE = 500

coords = lambda x,y: [int(x+SIZE/2), int(SIZE/2-y)]
angle_dist_to_coords = lambda angle, dist: [int(dist*math.cos(angle)+SIZE/2), int(SIZE/2-dist*math.sin(angle))]
color = lambda dist: [x*255 for x in list(Color("red").range_to(Color("green"), int(SIZE/2)))[dist].rgb]


pygame.init()
screen = pygame.display.set_mode([SIZE, SIZE])
pygame.display.set_caption("Lidar")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill([0,0,0])
    #draw the x axis
    pygame.draw.line(screen, [255,255,255], coords(-SIZE/2,0), coords(SIZE/2,0), 2)
    #draw the y axis
    pygame.draw.line(screen, [255,255,255], coords(0,-SIZE/2), coords(0,SIZE/2), 2)
    #draw the origin
    pygame.draw.circle(screen, [20,40,255], coords(0,0), 8)

    try:
        rcv = open("./data/dist_and_angles.txt", "r").readlines()[0]
        if rcv == 'q': 
            with open("./data/dist_and_angles.txt", "w") as f:
                f.write("")
            break
        for pair in rcv.split(","):
            pair = pair.strip()
            angle = int(pair.split(" ")[0])
            distance = int(pair.split(" ")[1])
            pygame.draw.circle(screen, color(distance), angle_dist_to_coords(math.radians(angle), distance), 4)
    except Exception as e:
        print(e)
        pass

    pygame.display.flip()

    

pygame.quit()