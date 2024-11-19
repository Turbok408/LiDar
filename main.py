import numpy as np
import pygame
# timestep = 1/60
# 1 pixel = 0.05 m

class Laser:
    def __init__(self,position,movingObjects):
        self.position = position
        self.rays = np.array([])
        self.movingObjects = movingObjects
        for i  in range (0,16):
            self.rays = np.append(self.rays,LightRay(self.position[0],self.position[1],np.pi/2-0.44505915+i*0.0523599))


    def draw(self,screen):
        pygame.draw.circle(screen,(255,0,0),self.position,5)
        for i in self.rays:
            i.draw(screen)
        self.update()

    def update(self):
        for i in range(len(self.rays)):
            for j in self.movingObjects:
                if j.position[0]*self.rays[i].m+self.rays[i].c >= -j.position[1]:
                    print("yep",j.position[0]*self.rays[i].m+self.rays[i].c,i,self.rays[i].m,self.rays[i].c,i,-j.position[1])
                else:
                    print("nop",j.position[0]*self.rays[i].m+self.rays[i].c,i,self.rays[i].m,self.rays[i].c,i,-j.position[1])
                """
                if object between i , i+1:
                    return distance of min distance point of object
                """
            self.rays[i].update()


class LightRay:
    def __init__(self,x,y,theta): # will bug if theta = 0
        self.m = np.sin(theta)/np.cos(theta)
        self.c = y-self.m*x
        self.theta = theta

    def draw(self,screen):
        #this might bug if outside screen?
        ysize = 800
        pygame.draw.line(screen,(0,0,255),(-self.c/self.m,0),((ysize-self.c)/self.m,ysize))

    def collisionDetection(self):
        pass

    def update(self):
        pass

class Object:

    # this is a square i cba doing any other shapes
    # loaction is top left square
    def __init__(self,initialPosition,initialVelocity):
        self.width = 10
        self.position = initialPosition
        self.velocity = initialVelocity

    def update(self):
        self.position=np.add(self.position,self.velocity*1/60)

    def draw(self,screen):
        pygame.draw.rect(screen,(255,255,255),(self.position[0],self.position[1],self.width,self.width))
        self.update()



if __name__ == "__main__":
    width =800
    height =800
    pygame.init()
    screen = pygame.display.set_mode((width,800))
    offset = 200
    movingobjects = [Object((0,400),np.array([50,0]))]
    drawObjects = [Laser(((width - 100) / 2, 0), movingobjects)]
    drawObjects.extend(movingobjects)
    clock = pygame.time.Clock()
    running = True
    while running:
        drawObject = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0,0,0))
        for i in drawObjects:
            i.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
