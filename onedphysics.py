
def gravity(mass):
    return -9.8 * mass



class OnedPoint:
    def __init__(self):
        self.m = 1.0
        self.xvel = 0.0
        self.xpos = 0.0
        self.forces = []

    def state(self):
        return { 'x' : self.xpos, 'vx' : self.xvel }

    def step(self, delta):
        acc = sum( map (lambda x: x(), self.forces) ) / self.m
        self.xpos += self.xvel * delta
        self.xvel += acc * delta

class Surface:
    def __init__(self, xpos, xnorm):
        self.xpos = xpos
        self.xnorm = xnorm
        self.elasticity = 100.0

    def force(self, xpoint):
        if (xpoint >= self.xpos and self.xnorm >= 0) or (xpoint < self.xpos and self.xnorm < 0) :
            return 0
        return abs(self.xpos - xpoint) * self.elasticity