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
    clock = sim.Model("clock", control.Clock())
    profile = sim.Controller("profile", control.ProfileRegulator())
    quad = sim.Compound ("quad", [ frame, motor, ground, gravity, clock, profile ] )
    gravity.connect("m", frame.get("m"))
    ground.connect("x", frame.get("x"))
    ground.connect("v", frame.get("v"))
    frame.connect("f", phy.NetForce( [ gravity.get("f"), motor.get("thrust"), ground.get("f") ] ).force() )
    clock.connect("time",quad.getio("time"))
    profile.connect("signal",clock.get("signal"))
    profile.connect("time", quad.getio("time"))
    motor.connect("target", profile.get("target"))
    return quad