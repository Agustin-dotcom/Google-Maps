class Node:
    def __init__(self,parent,state,action,depth,accumulatedCost):
        self.parent = parent
        self.state = state # we want it to be type State
        self.action = action # the same with action is going to be a class
        self.depth = depth
        self.accumulatedCost = accumulatedCost # this way it's easier to compute g(n) on f(n) = g(n)+h(n)
        self.momento = 0
    def __str__(self):
        stringToReturn = (
        f'parent --> { self.parent}\n'
        f'state --> { self.state.state}\n'
        f'action --> (origin, destination,cost) --> ({self.action.origin} , {self.action.destination}, {self.action.cost})\n'
        f'depth -->  {self.depth}'
        )
        return stringToReturn
    def __lt__(self,obj):
        return self.momento < obj.momento