# 1D simple physics modelling

class Gravity:
    def __init__(self):
        self.g = 9.8

    def forcef(self, m):
        return self.force( m() )

    def force(self, m):
        return -self.g * m

    def bind(self, model):
        model.addfunction("f", lambda s: s.forcef(model.get("m") ) )

    def init(self):
        return { }

class NetForce:
    def __init__(self, forces):
        self.forces = forces

    def force(self):
        return self.forcefunction

    def forcefunction(self):
        return sum( map (lambda x: x(), self.forces) )

class Body:
    def __init__(self, m):
        self.m = m   # in kilogramms

    def setm(self, m):
        self.m = m

    def bind(self, model):
        model.addfunction("m", lambda s: s.m )
        model.addparameter("m", lambda s, m: s.setm(m) , lambda s: s.m )
        model.addstate("x", lambda s, d: s.stepfx(d, model.get("x"), model.get("v") ) )
        model.addstate("v", lambda s, d: s.stepfv(d, model.get("v"), model.get("f") ) )

    def init(self):
        return { 'x' : 20.0, 'v' : 0.0 }     # meters and meters per second

    def stepfx(self, delta, x, v):
        return self.stepx(delta, x(), v())

    def stepfv(self, delta, v, f):
        return self.stepv(delta, v(), f())

    def stepx(self, delta, x, v):
        return x + (v * delta)

    def stepv(self, delta, v, f):
        return v + ( (f / self.m) * delta )

class Surface:
    def __init__(self, xpos, xnorm):
        self.xpos = xpos
        self.xnorm = 1.0 if xnorm >= 0.0 else -1.0
        self.elasticity = 100.0
        self.friction = 0.0

    def sete(self, e):
        self.elasticity = e

    def setf(self, f):
        self.friction = f

    def forcef(self, x, v):
        return self.force( x() , v() )

    def force(self, xpoint, v):
        if (xpoint >= self.xpos and self.xnorm >= 0) or (xpoint < self.xpos and self.xnorm < 0) :
            return 0       # outside of the surface
        return ( (self.xpos - xpoint) * self.elasticity ) + ( (-v) * self.friction )

    def bind(self, model):
        model.addparameter("e", lambda s, e: s.sete(e) , lambda s: s.elasticity )
        model.addparameter("fr", lambda s, f: s.setf(f) , lambda s: s.friction )
        model.addfunction("f", lambda s: s.forcef(model.get("x"), model.get("v") ) )

    def init(self):
        return { }
