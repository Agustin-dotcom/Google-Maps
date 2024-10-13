class State:
    def __init__(self,state):
        if not isinstance(state,int):
            raise TypeError(f"Introduce an int, not a {type(state).__name__}")
        self.state = state
