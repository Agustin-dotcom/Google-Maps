import json
import os
from collections import deque
class State:
    def __init__(self,state):
        self.state = state
class Node:
    def __init__(self,parent,state,action,depth):
        self.parent = parent
        self.state = state # we want it to be type State
        self.action = action # the same with action is going to be a class
        self.depth = depth
    def __str__(self):
        print("parent --> "+ str(self.parent))
        print("state --> "+ str(self.state))
        print("action --> (origin, destination,cost) --> "+ str(self.action.origin)+", "+str(self.action.destination)+", "+str(self.action.cost))
        print("depth --> "+ str(self.depth))
class Problem: # TODO # yo pondria "current" y "accumulatedCost" aqui en la clase Problem
    listOfActionsForRecoverPath = [] # lista a construir bottom-up
    def __init__(self,file_name):
        with open(file_name,'r') as file:
            new_dictionary = json.load(file)
        for i in new_dictionary['intersections']:
            i['whereto'] = [{"id":j['destination'],"cost":j['distance']/j['speed']} for j in new_dictionary['segments'] if j['origin'] == i['identifier']]
        self.dictionary = new_dictionary    
        # and here I guess we are ready to start the problem
        self.initializeOpen(self.dictionary['initial']) # inicializo nodo raiz
    def initializeOpen(self,initial):
        self.root = Node(None,initial,Action(None,initial,0),0) # no estoy seguro si para llegar al nodo raiz action == None
    def testGoal(self,Node):
        return self.dictionary['final'] == Node.state
    def search(self,Search): # Search asumimos que es o BreadthFirst o DepthFirst
        open = Search.insert(self.root)
        explored = []
        while open is not None:
            #Search.insert()
            node = Search.extract()
            if node.state.state not in explored:
                if(self.testGoal(node.state.state)):
                    return recoverPath(node)
    def expand(self,Search):
        open = []
        thisSet = self.dictionary['intersections']['whereto'] # we get a dictionary of dictionaries
        for each in thisSet:# we iterate through dictionaries with attributes {"id":x,"cost":y}
            Search.insert(each["id"],open) # we insert into our open list the next nodes
        return open

class Action: # Maybe we can receive a state and return a new one 
    def __init__(self,origin,destination,cost):
        self.origin = origin
        self.destination = destination
        self.cost = cost
class Search: # this is where we use inheritance
    recoverPath = [] # yo lo pondría en problema
    def insert():
        pass
    def extract():
        pass
class BreadthFirst(Search):# FIFO queue
    def insert(self,succesor,open):
        open.append(succesor)
    def extract(self,open):
        return open.popleft() # extrae por la izquierda (el primero en llegar)
class DepthFirst(Search): # LIFO queue
    def insert(self,sucessor,open):
        open.append(sucessor)
    def extract(self,open):
        return open.pop() # lo del return tiene sentido yo creo
def main():
    #os.chdir("C:\googleMapsVS\Google-Maps")
    problem = Problem("paseo_simón_abril_albacete_250_1.json")
    #print(problem.root)
    clase1 = BreadthFirst()
    cola = deque()
    cola.append('a')
    cola.append('g')
    #print(clase1.extract(cola))
    print(cola)
    print(clase1.extract(cola))
    print(cola)
main()