class State:
    def __init__(self,current,acumulatedCost):
        self.current = current
        self.acumulatedCost = acumulatedCost
class Node:
    def __init__(self,parent,state):
        self.parent = parent
        self.state = state # we want it to be type State
class Problem: # TODO
    def __init__(self):
        self = self
def main():
    print("Hello World!")
main()