import numpy as np
import pygame
import os

class heidi:
    def __init__(self, name="heidi", hp=20, spd=5, pos=[0, 0], atk=5, jumping=False):
        self.name = name
        self.hp = hp
        self.spd = spd
        self.pos = pos
        self.atk = atk
        self.jumping = jumping

    def move(self, x=0, y=0):
        self.pos[0] += x
        self.pos[1] += y

    def jump(self):
        if not self.jumping:
            pass

class runGame:
    def __init__(self, title="heidi", fps=60, size=68, path="data/img"):
        pygame.init()
        pygame.display.set_caption(title)

        self.size = size
        self.screen = pygame.display.set_mode((16*size, 9*size))
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.mapCode = 1
        self.running = False
        self.mapChange = True

        blockList = []
        blockList.append(None)

        for i in range(1, len(os.listdir(f"{path}/block"))+1):
            img = pygame.image.load(f"{path}/block/{i}.jpg")
            img = pygame.transform.scale(img, (size/2, size/2))
            blockList.append(img)

        self.blockList = blockList

        self.hd = heidi()

    def getEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.hd.move(x=self.hd.spd)
                if event.key == pygame.K_LEFT:
                    self.hd.move(x=-self.hd.spd)

    def getMap(self, path="data/map"):
        with open(f"{path}/{self.mapCode}.csv", "r") as file:
            self.mapData = np.loadtxt(file, delimiter=",")

    def drawMap(self):
        self.getMap()
        for y in range(np.shape(self.mapData)[0]):
            for x in range(np.shape(self.mapData)[1]):
                for block in range(1, len(self.blockList)+1):
                    if self.mapData[y][x] == block:
                        self.screen.blit(self.blockList[block], (x*(self.size/2), y*(self.size/2)))

    def drawHeidi(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.hd.pos, self.size)

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(self.fps)
            self.getEvent()

            if self.mapChange:
                self.drawMap()
                self.mapChange = False

            self.drawHeidi()


            pygame.display.update()

if __name__ == "__main__":
    rg = runGame()
    rg.run()