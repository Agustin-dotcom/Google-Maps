import json
import os
class State:
    def __init__(self,state):
        self.state = state
class Node:
    def __init__(self,parent,state,action):
        self.parent = parent
        self.state = state # we want it to be type State
        self.action = action # the same with action is going to be a class
    def __str__(self):
        print("parent --> "+ str(self.parent))
        print("state --> "+ str(self.state))
        print("action --> "+ str(self.action))
class Problem: # TODO # yo pondria "current" y "accumulatedCost" aqui en la clase Problem
    def __init__(self,file_name):
        with open(file_name,'r') as file:
            new_dictionary = json.load(file)
        for i in new_dictionary['intersections']:
            i['whereto'] = [{"id":j['destination'],"cost":j['distance']/j['speed']} for j in new_dictionary['segments'] if j['origin'] == i['identifier']]
        self.dictionary = new_dictionary    
        # and here I guess we are ready to start the problem

    def initializeOpen(self,initial):
        self.root = Node(None,initial,None) # no estoy seguro si para llegar al nodo raiz action == None
class Action: # Maybe we can receive a state and return a new one 
    def __init__(self,action):
        self.action = action
    pass # TODO
def main():
    #os.chdir("C:\googleMapsVS\Google-Maps")
    problem = Problem("paseo_simón_abril_albacete_250_1.json")
    problem.initializeOpen(problem.dictionary['initial'])
    print(problem.root)
main()