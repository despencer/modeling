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
    motor = sim.Model("motor", phy.Motor(1.0) )
    quad = sim.Compound ("quad", [ frame, motor, ground, gravity ] )
    gravity.connect("m", frame.get("m"))
    ground.connect("x", frame.get("x"))
    ground.connect("v", frame.get("v"))
    frame.connect("f", phy.NetForce( [ gravity.get("f"), motor.get("thrust"), ground.get("f") ] ).force() )
    motor.connect("target", quad.getio("motor"))
    return quad