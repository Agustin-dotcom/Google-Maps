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
        self.dictionary = new_dictionary   #!!!!!! 
        # and here I guess we are ready to start the problem
        self.initializeOpen(self.dictionary['initial']) # inicializo nodo raiz
    def initializeOpen(self,initial):
        self.root = Node(None,State(initial),Action(None,initial,0),0) # no estoy seguro si para llegar al nodo raiz action == None
        self.listOfActionsForRecoverPath.append(self.root.action)
    def testGoal(self,Node):
        return self.dictionary['final'] == Node.state.state
    def search(self,Search): # Search asumimos que es o BreadthFirst o DepthFirst
        """:param Search: o BFS o DPS
        
        :returns: o fallo o una lista de acciones"""
        open = []
        Search.insert(self.root,open)
        explored = []
        while open is not None:
            #Search.insert()
            node = Search.extract()
            if node.state.state not in explored:
                if(self.testGoal(node.state.state)):
                    return self.recoverPath(node)
                if (node.depth < 1):
                    successors = self.expand(node)
                for  successor in successors:
                    Search.insert(successor,successors)
                explored.append(node.state.state) #  node.state es el objeto y node.state.state es la variable en el objeto state
        return -1
    def applyAction(self,State,Action):
        """Given a state, we apply an action and return a new state.
        Imagine we have a current state, for example, and then we apply an action.\
        Importante decir que recibe objetos, no atributos

        :return: the new state"""
        if (Action.origin == State.state) :
            self.listOfActionsForRecoverPath.append(Action)
            return State(Action.destination)
        print("No se puede aplicar la siguiente acción")
        raise RuntimeError
        

    def recoverPath(self):
        return self.listOfActionsForRecoverPath
    def expand(self,Node_param):
        """ 
        :param Node_param: nodo al que apuntamos 
        
        :returns: list of nodes """
        successors = []
        possibleActions = []
        dictionaryOfDictionaries = self.dictionary['intersections']['identifier' == Node_param.state.state]['whereto'] # we get a dictionary of dictionaries
        for dictionary in dictionaryOfDictionaries:# we iterate through dictionaries with attributes {"id":x,"cost":y}
            possibleActions.append(Action(Node_param.state.state,dictionary["id"],dictionary["cost"])) # we insert into our open list the next nodes
        for action in possibleActions:
            newState = self.applyAction(Node_param.state,action) # Node.state es un objeto de tipo state
            newNode = Node(Node_param,newState,action,Node_param.depth+1)
            successors.append(newNode)
        return successors


class Action: # Maybe we can receive a state and return a new one 
    def __init__(self,origin,destination,cost):
        self.origin = origin
        self.destination = destination
        self.cost = cost
class Search: # this is where we use inheritance
    recoverPath = [] # yo lo pondría en problema
    def insert(self,successor,open):
        open.append(successor)
    def extract():
        pass
    def order():
        pass
class BreadthFirst(Search):# FIFO queue    
    def extract(self,open):
        return open.popleft() # extrae por la izquierda (el primero en llegar)
    def order():
        pass
class DepthFirst(Search): # LIFO queue
    def extract(self,open):
        return open.pop() # lo del return tiene sentido yo creo
    def order():
        pass
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
    agus = Node(None,State(12),Action(None,12,0),0)
    print(agus.state.state)

main()