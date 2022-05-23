import pygame
import numpy as np
import os
import math


class Heidi:
    def __init__(self, spd=3, pos=[0,0], moving=[False,False,False]):
        self.spd = spd
        self.pos = pos
        self.moving = moving
        self.walkCount = 1
        self.lookRight = True
        self.heidiSize = 1

    def move(self):
        if self.moving[0]:
            self.pos[0] -= self.spd
            self.lookRight = False
        if self.moving[1]:
            self.pos[0] += self.spd
            self.lookRight = True

        if self.moving[0] or self.moving[1]:
            self.walkCount += 1
            if self.walkCount > 16:
                self.walkCount = 1
        else:
            self.walkCount = 1

        if self.moving[2]:
            self.pos[1] += 5
        

        walk = math.ceil(self.walkCount / 4)

        self.walkImg = pygame.image.load(f"data/img/sprite/heidi/walk{walk}.png")
        self.walkImg = pygame.transform.scale(self.walkImg, (30*self.heidiSize, 42*self.heidiSize))

        if not self.lookRight:
            self.walkImg = pygame.transform.flip(self.walkImg, True, False)


class QueeenHeidisAdventure:
    def __init__(self, width=1280, height=720, fps=60, title="퀸턘의 모험"):
        pygame.init()
        pygame.display.set_caption(title)

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.mapCode = 1

        blockList = [None]
        for i in range(1, len(os.listdir(f"data/img/block"))+1):
            img = pygame.image.load(f"data/img/block/{i}.jpg")
            img = pygame.transform.scale(img, (20, 20))
            blockList.append(img)

        self.blockList = blockList

        self.hd = Heidi()

        self.getMap()
        self.getMapArray()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(self.fps)
            self.hd.move()
            self.eventCheck()
            self.gravity()
            self.draw()
            
    def eventCheck(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.hd.moving[0] = True
                if event.key == pygame.K_RIGHT:
                    self.hd.moving[1] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.hd.moving[0] = False
                if event.key == pygame.K_RIGHT:
                    self.hd.moving[1] = False

    def draw(self):
        self.screen.fill((255, 255, 255))

        for y in range(np.shape(self.mapData)[0]):
            for x in range(np.shape(self.mapData)[1]):
                for block in range(1, len(self.blockList)+1):
                    if self.mapData[y][x] == block:
                        self.screen.blit(self.blockList[block], [x*20, y*20])

        self.screen.blit(self.hd.walkImg, self.hd.pos)

        pygame.display.flip()
    
    def getMap(self):
        with open(f"data/map/{self.mapCode}.csv") as file:
            self.mapData = np.loadtxt(file, delimiter=",")

    def gravity(self):
        self.hd.moving[2] = True

    def getMapArray(self):
        mapArray = np.zeros((self.height, self.width))
        
        blockSize = int(self.height / np.shape(self.mapData)[1])
        blockArray = np.full((blockSize, blockSize), 2)

        for y in range(np.shape(self.mapData)[0]):
            for x in range(np.shape(self.mapData)[1]):
                if not (self.mapData[y][x] == 0):
                    mapArray[y*blockSize:(y+1)*blockSize, x*blockSize:(x+1)*blockSize] = blockArray

        self.mapArray = mapArray

        

        
                    

        
        
        

    


qha = QueeenHeidisAdventure()
qha.run()