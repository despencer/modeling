import simulation as sim

class Clock:
    def __init__ (self):
        self.setfq(100)               # controller frequency in Hz

    def setfq(self, fq):
        self.frequency = fq
        self.period = 1 / fq

    def clockf(self, delta, time, clock):
        return self.clock(delta, time(), clock() )

    def clock(self, delta, time, clock):
        if time < clock:
             return clock
        return clock + self.period

    def signalf(self,  time, clock):
        return self.signal( time() , clock() )

    def signal(self, time, clock):
        if time < clock:
            return False
        return True

    def bind(self, model):
        model.addinput("time")
        model.addparameter("frequency", lambda s, fq: s.setfq(fq), lambda s: s.frequency )
        model.addstate("clock", lambda s, d: s.clockf(d, model.get("time"), model.get("clock") ) )
        model.addfunction("signal", lambda s: s.signalf( model.get("time"), model.get("clock") ) )

    def init(self):
        return { 'clock' : 0.0 }

class Counter:
    def __init__(self):
        self.setsz(10)

    def setsz(self, sz):
        self.size = sz

    def value(self):
        return self.value()

    def valuef(self, value):
        return self.value( value() )

    def value(self, value):
        value = value - 1
        if value < 0:
            value = self.size-1
        return value

    def bind(self, controller):
        controller.addparameter("size", lambda s, sz: s.setsz(sz), lambda s: s.size )
        controller.addstate("value", lambda s: s.valuef( controller.get("value") ) )

    def init(self):
        return { 'value' : self.size-1 }
