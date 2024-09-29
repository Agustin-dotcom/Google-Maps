class State:
    def __init__(self,current,acumulatedCost):
        self.current = current
        self.acumulatedCost = acumulatedCost
class Node:
    def __init__(self,parent,state):
        self.parent = parent
        self.state = state # we want it to be type State
class Problem: # TODO
    pass
class Action: # Maybe we can receive a state and return a new one 
    pass # TODO
def main():
    print("Hello World!")
main()