from Scripts.Action import Action
from Scripts.State import State
class Node:
    def __init__(self,parent,state,action,depth):
        if not isinstance(parent,(Node,type(None))):
            raise TypeError(f"Introduce a Node, not a {type(parent).__name__}")
        if not isinstance(action,Action):
            raise TypeError(f"Introduce an Action, not a {type(action).__name__}")
        if not isinstance(state,State):
            raise TypeError(f"Introduce a State, not a {type(state).__name__}")
        self.parent = parent
        self.state = state # we want it to be type State
        self.action = action # the same with action is going to be a class
        self.depth = depth
    def __str__(self):
        stringToReturn = (
        f'parent --> { self.parent}\n'
        f'state --> { self.state.state}\n'
        f'action --> (origin, destination,cost) --> ({self.action.origin} , {self.action.destination}, {self.action.cost})\n'
        f'depth -->  {self.depth}'
        )
        return stringToReturn
