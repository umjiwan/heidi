class heidi:
    def __init__(self, name="heidi", hp=20, spd=5, pos=[0, 0], atk=5, jumping=False):
        self.name = name
        self.hp = hp
        self.spd = spd
        self.pos = pos
        self.atk = atk
        self.jumping = jumping

    def move(self, x):
        self.pos[0] += x

    def jump(self):
        if not self.jumping:
            pass 


if __name__ == "__main__":
    pass