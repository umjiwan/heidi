import pygame
import numpy as np
import os
import math

class Heidi:
    def __init__(self):
        self.speed = 3
        self.countWalk = 1
        self.countJump = 0
        self.lookRight = True
        self.jumping = False

        self.heidiSize = 1
        self.heidiSize = {
            "width": self.heidiSize * 30,
            "height": self.heidiSize * 42
        }

        self.pos = {
            "x": 0,
            "y": 0
        }

        self.direction = { # bool, weight
            "left": [False, 1],
            "right": [False, 1],
            "up": [False, 1],
            "down": [False, 1]
        }

    def moveHeidi(self):
        if self.direction["left"][0] == True:
            self.pos["x"] -= self.speed * self.direction["left"][1]
            self.lookRight = False

        if self.direction["right"][0] == True:
            self.pos["x"] += self.speed * self.direction["right"][1]
            self.lookRight = True

        if self.direction["up"][0] == True:
            self.pos["y"] -= self.speed * self.direction["up"][1]

        if self.direction["down"][0] == True:
            self.pos["y"] += self.speed * self.direction["down"][1]

        if self.direction["left"][0] or self.direction["right"][0]:
            self.countWalk += 1
            if self.countWalk > 4 * 4:
                self.countWalk = 1
        else:
            self.countWalk = 1

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
        self.hd = Heidi()


        self.blockList = self.loadBlockList()

        self.mapData = self.loadMap()
        self.mapDetailData = self.loadDetailMap()

    def loadBlockList(self):
        blockList = [None]

        for i in range(1, len(os.listdir(f"data/img/block"))+1):
            img = pygame.image.load(f"data/img/block/{i}.jpg")
            img = pygame.transform.scale(img, (20, 20))
            blockList.append(img)

        return blockList

    def loadMap(self):
        with open(f"data/map/{self.mapCode}.csv") as file:
            return np.loadtxt(file, delimiter=",")

    def loadDetailMap(self):
        mapArray = np.zeros((self.height, self.width))
        
        blockSize = int(self.width / np.shape(self.mapData)[1])
        blockArray = np.full((blockSize, blockSize), 2)

        for y in range(np.shape(self.mapData)[0]):
            for x in range(np.shape(self.mapData)[1]):
                if not (self.mapData[y][x] == 0):
                    mapArray[y*blockSize:(y+1)*blockSize, x*blockSize:(x+1)*blockSize] = blockArray

        return mapArray

    def eventCheck(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.hd.direction["left"][0] = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.hd.direction["right"][0] = True

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.jumpHeidi()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.hd.direction["left"][0] = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.hd.direction["right"][0] = False
            
    def checkFloorCrash(self):
        y = self.hd.pos["y"] + self.hd.heidiSize["height"]
        try:
            if np.all(self.mapDetailData[y+1][self.hd.pos["x"]:self.hd.pos["x"] + self.hd.heidiSize["width"] - 1] == 0):
                return False
            else:
                return True
        except:
            pass

    def checkWallLeftSide(self):
        x = self.hd.pos["x"]
        y = self.hd.pos["y"]

        try:
            if np.all(self.mapDetailData[y:y + self.hd.heidiSize["height"] - 1, x-1] == 0):
                pass
            else:
                self.hd.direction["left"][0] = False
        except:
            pass

    def checkWallRightSide(self):
        x = self.hd.pos["x"]
        y = self.hd.pos["y"]

        try:
            if np.all(self.mapDetailData[y:y + self.hd.heidiSize["height"] - 1, x + self.hd.heidiSize["width"] + 1] == 0):
                pass
            else:
                self.hd.direction["right"][0] = False
        except:
            pass

    def jumpHeidi(self):
        if self.checkFloorCrash():
            self.hd.pos["y"] = self.hd.pos["y"] - 50
            
    def gravity(self):
        self.hd.direction["down"][0] = not self.checkFloorCrash()

    def loadWalkImg(self, walkNumber):
        walkNumber = math.ceil(walkNumber / 4)
        walkImg = pygame.image.load(f"data/img/sprite/heidi/walk{walkNumber}.png")
        walkImg = pygame.transform.scale(walkImg, (self.hd.heidiSize["width"], self.hd.heidiSize["height"]))

        if not self.hd.lookRight:
            walkImg = pygame.transform.flip(walkImg, True, False)

        return walkImg
            
    def draw(self):
        self.screen.fill((255, 255, 255))

        for y in range(np.shape(self.mapData)[0]):
            for x in range(np.shape(self.mapData)[1]):
                for block in range(1, len(self.blockList) + 1):
                    if self.mapData[y][x] == block:
                        self.screen.blit(self.blockList[block], [x*20, y*20])

        self.screen.blit(self.loadWalkImg(self.hd.countWalk), [self.hd.pos["x"], self.hd.pos["y"]])

        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(self.fps)
            
            self.hd.moveHeidi()
            self.eventCheck()

            self.checkWallLeftSide()
            self.checkWallRightSide()
            self.gravity()
            self.draw()

qha = QueeenHeidisAdventure()
qha.run()