from collections import namedtuple

def timerange(start, stop, delta):
    while start <= stop:
        yield start
        start += delta

class Model:
    def __init__(self, name, physics):
        self.name = name
        self.physics = physics
        self.states = { }
        self.inputs = { }
        self.funcs = { }
        self.params = { }
        self.Parameters = namedtuple('Parameters', ['setter' , 'getter'] )

    def bind(self):
        self.physics.bind(self)

    def init(self):
        self.current = self.physics.init()
        return self.current

    def stepcalc(self, delta):
        self.next = { }
        for state, trans in self.states.items():
            self.next[state] =  trans(self.physics, delta)

    def stepswitch(self):
        self.current = self.next
        return self.current

    def getstate(self):
        return self.current

    def addstate(self, state, func):
        self.states[state] = func

    def addinput(self, name):
        self.inputs[name] = stub

    def addfunction(self, name, func):
        self.funcs[name] = func

    def addparameter(self, name, setter, getter):
        self.params[name] = self.Parameters(setter, getter)

    def get(self, name):
        return lambda : self.getbyname(name)

    def getbyname(self, name):
        if name in self.states:
            return self.current[name]
        elif name in self.funcs:
            return self.funcs[name](self.physics)
        else:
            return self.inputs[name]()

    def connect(self, name, val):
        self.inputs[name] = val

    def setparam(self, name, value):
        if name in self.params:
            self.params[name].setter(self.physics, value)
        else:
            self.current[name] = value

    def getparam(self, name):
        if name in self.params:
            return self.params[name].getter(self.physics)
        else:
            return self.current[name]

    def getallparams(self):
        params = self.current.copy()
        for name, accessor in self.params.items():
            params[name] = accessor.getter(self.physics)
        return params

class Compound:
    def __init__(self, name, subs):
        self.name = name
        self.subs = { }
        for s in subs:
            self.subs[s.name] = s

    def map(self, func):
        for s in self.subs.values():
            func(s)

    def bind(self):
        self.map( lambda x: x.bind() )

    def setparam(self, name, value):
        isep = name.find('.')
        if isep < 0: raise NameError(name)
        self.subs[name[0:isep]].setparam(name[isep+1:],value)

    def getparam(self, name):
        isep = name.find('.')
        if isep < 0: raise NameError(name)
        return self.subs[name[0:isep]].getparam(name[isep+1:])

    def init(self):
        self.map( lambda x: x.init() )

    def stepcalc(self, delta):
        self.map( lambda x: x.stepcalc(delta) )

    def stepswitch(self):
        self.map( lambda x: x.stepswitch() )

    def getstate(self):
        state = {}
        for s in self.subs.values():
            for name,value in s.getstate().items():
                state[s.name+name] = value
        return state;

    def step(self, delta):
        self.stepcalc(delta)
        self.stepswitch()

    def simulate(self, start, end, delta):
        history = []
        for t in timerange(start, end, delta):
            state = {'t' : t}
            state.update(self.getstate())
            history.append(state)
            self.step(delta)
        return history

    def getallparams(self):
        params = {}
        for sub in self.subs.values():
            children = sub.getallparams()
            if len(children) > 0:
                params[sub.name] = children
        return params

def stub():
    return 0.0