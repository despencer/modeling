import onedphysics as phy
import simulation as sim

def createball():
    frame = sim.Model("frame", phy.Body(1.0) )
    ground = sim.Model("ground", phy.Surface(0.0, 1.0) )
    gravity = sim.Model("gravity", phy.Gravity() )
    ball = sim.Compound ("ball", [ frame, ground, gravity ] )
    ball.bind()
    gravity.connect("m", frame.get("m"))
    ground.connect("x", frame.get("x"))
    ground.connect("v", frame.get("v"))
    frame.connect("f", phy.NetForce( [ gravity.get("f"), ground.get("f") ] ).force() )
    ball.init()
    return ball