import onedphysics as phy
import simulation as sim

class Model:
    def __init__(self):
        self.quad = phy.OnedPoint()
        self.quad.m = 1.0
        self.quad.xvel = 0.0
        self.quad.xpos = 20.0
        self.ground = phy.Surface(0.0, 1.0)
        self.quad.forces = [ lambda : phy.gravity(self.quad.m),
                             lambda : self.ground.force(self.quad.xpos) ]

    def step(self, delta):
        self.quad.step(delta)

    def simulate(self, start, end, delta):
        history = []
        for t in sim.timerange(start, end, delta):
            state = {'t' : t}
            state.update(self.quad.state())
            history.append(state)
            self.step(delta)
        return history