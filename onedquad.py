import onedphysics as phy
import simulation as sim
import control

def createball():
    frame = sim.Model("frame", phy.Body(1.0) )
    ground = sim.Model("ground", phy.Surface(0.0, 1.0) )
    gravity = sim.Model("gravity", phy.Gravity() )
    ball = sim.Compound ("ball", [ frame, ground, gravity ] )
    gravity.connect("m", frame.get("m"))
    ground.connect("x", frame.get("x"))
    ground.connect("v", frame.get("v"))
    frame.connect("f", phy.NetForce( [ gravity.get("f"), ground.get("f") ] ).force() )
    return ball

def createquad():
    frame = sim.Model("frame", phy.Body(1.0) )
    ground = sim.Model("ground", phy.Surface(0.0, 1.0) )
    gravity = sim.Model("gravity", phy.Gravity() )
    motor = sim.Model("motor", Motor(1.0) )
    quad = sim.Compound ("quad", [ frame, motor, ground, gravity ] )
    gravity.connect("m", frame.get("m"))
    ground.connect("x", frame.get("x"))
    ground.connect("v", frame.get("v"))
    frame.connect("f", phy.NetForce( [ gravity.get("f"), motor.get("thrust"), ground.get("f") ] ).force() )
    motor.connect("target", quad.getio("motor"))
    return quad

class Motor:
    def __init__ (self, xnorm):
        self.elasticity = 5.0 # Newtons per second, analog to the KV rating
        self.xnorm = 1.0 if xnorm >= 0.0 else -1.0 # up or down

    def sete(self, e):
        self.elasticity = e

    def stepfc(self, delta, current, target):
        return self.stepc(delta, current(), target() )

    def stepc(self, delta, current, target):
        if (self.xnorm > 0 and target < 0) or (self.xnorm < 0 and target > 0):
              target = 0.0
        if self.elasticity * delta >= abs(current - target):
            return target
        if abs(target) > abs(current):
            return current + self.xnorm * ( self.elasticity * delta )
        else:
            return current - self.xnorm * ( self.elasticity * delta )

    def bind(self, model):
        model.addparameter("e", lambda s, e: s.sete(e) , lambda s: s.elasticity )
        model.addstate("thrust", lambda s, d: s.stepfc(d, model.get("thrust"), model.get("target") ) )

    def init(self):
        return { 'thrust' : 0.0 }     # current force (Newtons)
