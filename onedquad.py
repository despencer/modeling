import onedphysics as phy
import simulation as sim

class OldModel:
    def __init__(self):
        self.quad = phy.Body()
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

def createball():
    frame = sim.Model("frame", phy.Body(1.0) )
    ground = sim.Model("ground", phy.Surface(0.0, 1.0) )
    gravity = sim.Model("gravity", phy.Gravity() )
    ball = sim.Compound ("ball", [ frame, ground, gravity ] )
    ball.bind()
    gravity.connect("m", frame.get("m"))
    ground.connect("x", frame.get("x"))
    frame.connect("f", phy.NetForce( [ gravity.get("f"), ground.get("f") ] ).force() )
    ball.init()
    return ball