import json
from collections import deque
from Action import Action
from State import State
from Node import Node
from Search import Search
from DepthFirst import DepthFirst
from BreadthFirst import BreadthFirst
#import numpy as np # requiere de 'pip install numpy' in cmd line
class Problem:
    def __init__(self,file_name):
        # Here, I read the dictionary
        self.nodesGenerated = 0
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
        self.nodesGenerated+=1
    #################################################################################
    ####################             search              ############################
    #################################################################################
    def search(self,search_param): # Search asumimos que es o BreadthFirst o DepthFirst
        """:param search_param: o BFS o DPS
        
        :returns: o fallo o una lista de acciones"""
        expandedNodes = 0
        exploredNodes = 0
        if not isinstance(search_param,(Search,BreadthFirst,DepthFirst)):
            raise TypeError(f"Introduce a Search object, not a {type(search_param).__name__}")
        explored = []
        search_param.insert(self.root)
        while search_param.openDS is not []:
            if  isinstance(search_param,DepthFirst):# solo si estamos con LIFO
                temp = deque(search_param.openDS)
                search_param.openDS = []
                while len(temp)!=0:
                    search_param.openDS.append(temp.pop())
                #search_param.openDS = np.array(search_param.openDS) #dando la vuelta el array para coger con el id mas peque;o    
            node = search_param.extract()
            exploredNodes +=1
            if node.state.state not in explored:
                if(self.testGoal(node)):
                    print(f'(Expanded nodes, explored nodes) --> ({expandedNodes},{exploredNodes})')
                    print(f'Depth of the solution --> {node.depth}')
                    print(f'Nodes generated --> {self.nodesGenerated}')
                    return self.recoverPath(node,[],0)
                successors = self.expand(node)
                if (len(successors>0)):
                    expandedNodes+=1
                for  successor in successors:
                    #search_param.insert(successor,successors)
                    search_param.insert(successor)
                explored.append(node.state.state) #  node.state es el objeto y node.state.state es la variable en el objeto state
        raise Exception("Solucion no encontrada y hemos recorrido todo el arbol :[")

     #################################################################################
    ####################             testGoal              ############################
    #################################################################################
    def testGoal(self,node):
        if not isinstance(node,Node):
            raise TypeError(f"Introduce a Node, not a {type(node).__name__}")
        return self.dictionary.get('final') == node.state.state
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
        dictionaryOfDictionaries = [d['whereto'] for d in self.dictionary['intersections'] if d['identifier'] == Node_param.state.state][0] # we get a dictionary of dictionaries
        for dictionary in dictionaryOfDictionaries:# we iterate through dictionaries with attributes {"id":x,"cost":y}
            possibleActions.append(
                Action(
                    Node_param.state.state, #origen
                    dictionary.get("id"), # destino
                    dictionary.get("cost") #coste
                )
            ) # we insert into our open list the next nodes
        for action in possibleActions:
            newState = self.applyAction(Node_param.state,action) # Node.state es un objeto de tipo state
            newNode = Node(Node_param,newState,action,Node_param.depth+1)
            self.nodesGenerated+=1
            successors.append(newNode)
        return successors
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
            #self.listOfActionsForRecoverPath.append(action) # si hacemos esto estariamos introduciendo todos los nodos
            return State(action.destination)
        raise Exception(f"No se puede aplicar la siguiente acción")
         #################################################################################
    ####################             recoverPath              ############################
    #################################################################################
    def recoverPath(self,node,list_param,total_cost):# n <- len(list_param)
        if node.parent is None:# O(1)
            temp = []# O(1)
            i = deque(list_param)
            while  len(i) != 0:# O(n)
                temp.append(i.pop())# O(1)
            print(f'total cost -->{total_cost}')# O(1)
            return temp
        else:
            list_param.append(node.action)# O(1)
            total_cost = total_cost + node.action.cost
            return self.recoverPath(node.parent,list_param=list_param,total_cost=total_cost) # O(T) # not that expensive it could be worse
