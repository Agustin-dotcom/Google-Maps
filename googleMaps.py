import json
import os
from collections import deque
class Search: # this is where we use inheritance
    def __init__(self,openDS):
        if not isinstance(openDS,deque):
            raise TypeError(f" There has been an error, please introduce a deque object, not a {type(openDS).__name__}.")
        self.openDS = openDS
    def insert(self,successor):
        self.openDS.append(successor)
    def extract():
        pass
class BreadthFirst(Search):# FIFO queue    
    def extract(self):
        return self.openDS.popleft() # extrae por la izquierda (el primero en llegar)
class DepthFirst(Search): # LIFO queue
    def extract(self):
        return self.openDS.pop() # lo del return tiene sentido yo creo
class State:
    def __init__(self,state):
        if not isinstance(state,int):
            raise TypeError(f"Introduce an int, not a {type(state).__name__}")
        self.state = state
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
        print("parent --> "+ str(self.parent))
        print("state --> "+ str(self.state))
        print("action --> (origin, destination,cost) --> "+ str(self.action.origin)+", "+str(self.action.destination)+", "+str(self.action.cost))
        print("depth --> "+ str(self.depth))
class Problem:
    def __init__(self,file_name,listOfActionsForRecoverPath):
        # Here, I read the dictionary
        self.listOfActionsForRecoverPath = listOfActionsForRecoverPath
        with open(file_name,'r') as file:
            self.dictionary = json.load(file)
        for i in self.dictionary.get('intersections'):
            i['whereto'] = [{"id":j.get('destination'),"cost":j.get('distance')/j.get('speed')} for j in self.dictionary.get('segments') if j.get('origin') == i.get('identifier')]
        # and here I guess we are ready to start the problem
        self.initializeOpen(self.dictionary.get('initial')) # inicializo nodo raiz
        
    def initializeOpen(self,initial):
        if not isinstance(initial,int):
            raise TypeError(f"Introduce an int, not a {type(initial).__name__}")
        self.root = Node(None,State(initial),Action(None,initial,0),0) # no estoy seguro si para llegar al nodo raiz action == None
        self.listOfActionsForRecoverPath.append(self.root.action)
    #################################################################################
    ####################             testGoal              ############################
    #################################################################################
    def testGoal(self,node):
        if not isinstance(node,Node):
            raise TypeError(f"Introduce a Node, not a {type(node).__name__}")
        return self.dictionary.get('final') == node.state.state
    #################################################################################
    ####################             search              ############################
    #################################################################################
    def search(self,search_param): # Search asumimos que es o BreadthFirst o DepthFirst
        """:param search_param: o BFS o DPS
        
        :returns: o fallo o una lista de acciones"""
        if not isinstance(search_param,(Search,BreadthFirst,DepthFirst)):
            raise TypeError(f"Introduce a Search object, not a {type(search_param).__name__}")
        open = []
        search_param.insert(self.root)
        explored = []
        while open is not None:
            #Search.insert()
            node = search_param.extract()
            if node.state.state not in explored:
                if(self.testGoal(node)):
                    return self.recoverPath(node)
                successors = self.expand(node)
                for  successor in successors:
                    #search_param.insert(successor,successors)
                    search_param.insert(successor)
                explored.append(node.state.state) #  node.state es el objeto y node.state.state es la variable en el objeto state
        return -1
    #################################################################################
    ####################             applyAction              ############################
    #################################################################################
    def applyAction(self,state,action):
        """Given a state, we apply an action and return a new state.
        Imagine we have a current state, for example, and then we apply an action.
        Importante decir que recibe objetos, no atributos

        :return: the new state"""
        if not isinstance(state,State):
            raise TypeError(f"Introduce a State object, not a {type(state).__name__}")
        if not isinstance(action,Action):
            raise TypeError(f"Introduce an Action object, not a {type(action).__name__}")
        if (action.origin == state.state) :
            self.listOfActionsForRecoverPath.append(action)
            return State(action.destination)
        raise RuntimeError(f"No se puede aplicar la siguiente acción")
        

    def recoverPath(self):
        return self.listOfActionsForRecoverPath
     #################################################################################
    ####################             expand             ############################
    #################################################################################
    def expand(self,Node_param):
        """ 
        :param Node_param: nodo al que apuntamos 
        
        :returns: list of nodes """
        if not isinstance(Node_param,Node):
            raise TypeError(f"Introduce a Node object, not a {type(Node_param).__name__}")
        successors = []
        possibleActions = []
        dictionaryOfDictionaries = self.dictionary['intersections']['identifier' == Node_param.state.state]['whereto'] # we get a dictionary of dictionaries
        for dictionary in dictionaryOfDictionaries:# we iterate through dictionaries with attributes {"id":x,"cost":y}
            possibleActions.append(Action(Node_param.state.state,dictionary.get("id"),dictionary.get("cost"))) # we insert into our open list the next nodes
        for action in possibleActions:
            newState = self.applyAction(Node_param.state,action) # Node.state es un objeto de tipo state
            newNode = Node(Node_param,newState,action,Node_param.depth+1)
            successors.append(newNode)
        return successors

class Action: # Maybe we can receive a state and return a new one 
    def __init__(self,origin,destination,cost):
        if not isinstance(origin,(int,type(None))):
            raise TypeError(f"Introduce an int, not a {type(origin).__name__}")
        if not isinstance(destination,int):
            raise TypeError(f"Introduce an int, not a {type(destination).__name__}")
        if not isinstance(cost,(int,float)):
            raise TypeError(f"Introduce an int or a float, not a {type(cost).__name__}")
        self.origin = origin
        self.destination = destination
        self.cost = cost

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
    problem.search(DepthFirst())

main()