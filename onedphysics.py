# 1D simple physics modelling

class Gravity:
    def __init__(self):
        self.g = 9.8

    def forcef(self, m):
        return self.force( m() )

    def force(self, m):
        return -self.g * m

    def bind(self, model):
        model.addinput("m")
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
        self.m = m

    def setm(self, m):
        self.m = m

    def bind(self, model):
        model.addinput("f")
        model.addfunction("m", lambda s: s.m )
        model.addparameter("m", lambda s, m: s.setm(m) , lambda s: s.m )
        model.addstate("x", lambda s, d: s.stepfx(d, model.get("x"), model.get("v") ) )
        model.addstate("v", lambda s, d: s.stepfv(d, model.get("v"), model.get("f") ) )

    def init(self):
        return { 'x' : 20.0, 'v' : 0.0 }

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
        self.xnorm = xnorm
        self.elasticity = 100.0

    def sete(self, e):
        self.elasticity = e

    def forcef(self, x):
        return self.force( x() )

    def force(self, xpoint):
        if (xpoint >= self.xpos and self.xnorm >= 0) or (xpoint < self.xpos and self.xnorm < 0) :
            return 0
        return abs(self.xpos - xpoint) * self.elasticity

    def bind(self, model):
        model.addinput("x")
        model.addparameter("e", lambda s, e: s.sete(e) , lambda s: s.elasticity )
        model.addfunction("f", lambda s: s.forcef(model.get("x") ) )

    def init(self):
        return { }
