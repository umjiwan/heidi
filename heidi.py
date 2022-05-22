import numpy as np
import pygame

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
    def __init__(self, title="heidi", fps=60, size=68):
        pygame.init()
        pygame.display.set_caption(title)

        self.size = size
        self.screen = pygame.display.set_mode((16*size, 9*size))
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.mapCode = 1
        self.running = False

    def getEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def getMap(self, path="data/map"):
        with open(f"{path}/{self.mapCode}.csv", "r") as file:
            self.mapData = np.loadtxt(file, delimiter=",")

    def drawMap(self):
        self.getMap(self)
        
        for i in range(self.mapData):
            print(i)
        

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(self.fps)
            self.getEvent()
            self.drawMap()

if __name__ == "__main__":
    rg = runGame()
    rg.run()