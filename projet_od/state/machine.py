class StateMachine:
    """[summary]
    """
    def __init__(self):
        """[summary]
        """
        self._state = None
        self._states = {}
        self._transitions = {}
    
    def change_state(self, state):
        if self._state != None:
            self._state.exit()
        
        self._state = state
        state.enter()
    
    def set_state(self, name):
        self.change_state(self._states[name])
    
    def update(self, *args, **kwargs):
        _state = self._state
        if _state != None:
            _state.execute(args, kwargs)
            
    def add_state(self, state, name):
        self._states[name] = state
    
    def make_transition(self, name, from_state_name, to_state_name):
        transition = Transition(name, from_state_name, to_state_name, self)
        self._states[from_state_name]._transition_exit[name] = transition
        self._states[to_state_name]._transition_enter[name] = transition
        self._transitions[name] = transition
        return transition
    
    def make_state(self, name, state_class=None, *args, **kwargs):
        if state_class == None:
            State(self, name, args, kwargs)
        else:
            state_class(self, name, args, kwargs)
    
    def make_states(self, names, state_class=None, *args, **kwargs):
        for name in names:
            self.make_state(name, state_class, args, kwargs)

    def transit(self, name):
        self._transitions[name]()

    def __repr__(self):
        rp = "State Machine\n"
        rp += "Current state = {}\n".format(self._state)
        rp += "States :\n"
        rp += "\n".join(["\t" + repr(states) for states in self._states.values()])
        rp += "\nTransitions :\n"
        rp += "\n".join(["\t" + repr(states) for states in self._transitions.values()])
        return rp
    
    def __str__(self):
        return self.__repr__()
    
    def set_state_enter(self, name):
        return self._states[name].set_enter
    
    def set_state_exit(self, name):
        return self._states[name].set_exit
    
    def set_state_execute(self, name):
        return self._states[name].set_execute
    
class State:
    """[summary]
    """
    def __init__(self, state_machine, name):
        """[summary]

        Args:
            state_machine ([type]): [description]
            name ([type]): [description]
        """
        self._transition_enter = {}
        self._transition_exit = {}
        self.name = name
        state_machine.add_state(self, name)
        self._sm = state_machine

    def __repr__(self):
        return self.name

    def enter(self):
        pass
    
    def execute(self, *args, **kwargs):
        pass
    
    def exit(self):
        pass
    
    def set_exit(self, f):
        self.exit = f
        return f
    
    def set_enter(self, f):
        self.enter = f
        return f
    
    def set_execute(self, f):
        self.execute = f
        return f
    

class Transition:
    """[summary]
    """
    def __init__(self, name, from_state, to_state, state_machine):
        """[summary]

        Args:
            name ([type]): [description]
            from_state ([type]): [description]
            to_state ([type]): [description]
            state_machine ([type]): [description]
        """
        self._init_state = from_state
        self._end_state = to_state
        self.name = name
        self._sm = state_machine
    
    def __repr__(self):
        return self.name
    
    def __call__(self):
        """Make the transition
        """
        _sm = self._sm
        if _sm._state == None:
            raise AttributeError("StateMachine has no state")
        if self._init_state == _sm._state.name:
            _sm.set_state(self._end_state)

