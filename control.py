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
