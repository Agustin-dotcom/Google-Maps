import math
from BestFirst import BestFirst
from AStar import AStar
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
        self.exploredNodes = 0
        self.expandedNodes = 0
        self.depth = 0
        self.totalCost = 0.0
        with open(file_name,'r') as file:
            self.dictionary = json.load(file)
            # Conversión de velocidad de km/h a m/s y cálculo del coste
       # Convert the list of intersections to a dictionary of dictionaries
        self.dictionary['intersections'] = {inter['identifier']: inter for inter in self.dictionary.get('intersections')}

        # Add the 'whereto' attribute to each intersection
        for inter in self.dictionary['intersections'].values():
            inter['whereto'] = []

        # Populate the 'whereto' attribute based on the segments
        for segment in self.dictionary.get('segments'):
            origin = segment['origin']
            destination = segment['destination']
            distance = segment['distance']
            speed_kmh = segment['speed']

            # Convert speed from km/h to m/s
            speed_ms = speed_kmh * (1000 / 3600)
    
            # Calculate the cost
            cost = distance / speed_ms
    
            # Add the destination and cost to the 'whereto' attribute of the origin intersection
            if origin in self.dictionary.get('intersections'):
                self.dictionary.get('intersections').get(origin).get('whereto').append({'id': destination, 'cost': cost})
                # Convertir la lista de intersecciones a un diccionario donde la clave sea el 'identifier'
                #self.dictionary['intersections'] = {intersection['identifier']: {**intersection, 'whereto': set()} for intersection in self.dictionary.get('intersections')}
        self.initializeOpen(self.dictionary.get('initial')) # inicializo nodo raiz
        
    def initializeOpen(self,initial):
        #if not isinstance(initial,int):
        #    raise TypeError(f"Introduce an int, not a {type(initial).__name__}")
        longitudeInitialNode = self.dictionary.get('intersections').get(initial).get('longitude')
        latitudeInitialNode = self.dictionary.get('intersections').get(initial).get('latitude')
        self.root = Node(None,State(initial,longitudeInitialNode,latitudeInitialNode),Action(None,initial,0),0,0) # no estoy seguro si para llegar al nodo raiz action == None
        self.nodesGenerated+=1
    #################################################################################
    ####################             search              ############################
    #################################################################################
    def search(self,search_param): # Search asumimos que es o BreadthFirst o DepthFirst
        """:param search_param: strategy to use
        
        :returns: empty list of list of actions"""
        #expandedNodes = 0
        #exploredNodes = 0
        #if not isinstance(search_param,Search) and not isinstance(search_param,BreadthFirst) and not isinstance(search_param,DepthFirst) and not isinstance(search_param,BestFirst) and not isinstance(search_param,AStar):
        #    raise TypeError(f"Introduce a Search object, not a {type(search_param).__name__}")
        explored = set()
        search_param.insert(self.root)
        while len(search_param.openDS)!=0:
            #if  isinstance(search_param,DepthFirst):# solo si estamos con LIFO #“Notes: The order of the actions is determined by the destination state whose identifier is the lowest, that is, if different (partial) destinations can be reached at a given point (intersection), they will be visited in increasing numerical order”.
                #temp = deque(search_param.openDS)
                #search_param.openDS = []
                #while len(temp)!=0:
                    #search_param.openDS.append(temp.pop())
                #search_param.openDS = np.array(search_param.openDS) #dando la vuelta el array para coger con el id mas peque;o    
            node = search_param.extract()
            self.exploredNodes +=1
            if node.state.state not in explored: #node[1] bc is a tuple (heuristic,node)
                if(self.testGoal(node)): # remember that node is a tuple
                    #print(f'Generated nodes ; expandedNodes ; depthOfSolution ; cost ; exploredNodes)')
                    #print(f'{self.nodesGenerated};{self.expandedNodes};{node.depth};{node.accumulatedCost};{self.exploredNodes}')
                    self.depth = node.depth
                    self.totalCost = node.accumulatedCost
                    return self.recoverPath(node,[],0)
                successors = self.expand(node)
                if (len(successors)>0):
                    self.expandedNodes+=1
                for  successor in successors:
                    #search_param.insert(successor,successors)
                    search_param.insert(successor)
                explored.add(node.state.state) #  node.state es el objeto y node.state.state es la variable en el objeto state
        print("Solución no encontrada y hemos recorrido todo el árbol")
        return search_param.openDS

     #################################################################################
    ####################             testGoal              ############################
    #################################################################################
    def testGoal(self,node):
        #if not isinstance(node,Node):
        #    raise TypeError(f"Introduce a Node, not a {type(node).__name__}")
        return self.dictionary.get('final') == node.state.state# node.state es de tipo State y node.state.state es de tipo int
    #################################################################################
    ####################             expand             ############################
    #################################################################################
    def expand(self,Node_param):
        """ 
        :param Node_param: nodo al que apuntamos 
        :returns: list of nodes """
        #if not isinstance(Node_param,Node):
        #    raise TypeError(f"Introduce a Node object, not a {type(Node_param).__name__}")
        successors = []
        currentIntersection = self.dictionary.get('intersections').get(Node_param.state.state)

        #if not currentIntersection:
        #    return []
        #possibleActions = []
        #dictionaryOfDictionaries = {d['identifier']: d for d in self.dictionary['intersections']}# Node_param.state.state # we get a dictionary of dictionaries
        for destination in currentIntersection.get("whereto"):
            """currentIntersection.get("whereto")
            [{'id': 1256026663, 'cost': 1.7331}, {'id': 1531659796, 'cost': 2.346}]"""
            newAction = Action(
                    Node_param.state.state, #origen
                    destination.get("id"), # destino
                    destination.get("cost") #coste
                )
            #successors.append(newAction) # we insert into our open list the next nodes
            # REMEMBER THAT destination is A DICTIONARY {"id":,"cost":}
            newState = State(newAction.destination,self.dictionary.get('intersections').get(destination.get('id')).get('longitude'),self.dictionary.get('intersections').get(destination.get('id')).get('latitude')) #self.applyAction(Node_param.state,action) # Node.state es un objeto de tipo state
            newNode = Node(Node_param,newState,newAction,Node_param.depth+1,Node_param.accumulatedCost+newAction.cost)
            #newNode.heuristic = self.straightLineDistanceToTheGoal(newNode)
            self.nodesGenerated+=1
            #h = self.decideWhetherAStarOrBestFirst(newNode,search_param2)#Also known as f(n)
            successors.append(newNode)
        return successors

    #################################################################################
    ####################             applyAction              #######################
    #################################################################################
    # def applyAction(self,state,action):
    #     """Given a state, we apply an action and return a new state.
    #     Imagine we have a current state, for example, and then we apply an action.
    #     Importante decir que recibe objetos, no atributos

    #     :return: the new state"""
    #     if not isinstance(state,State):
    #         raise TypeError(f"Introduce a State object, not a {type(state).__name__}")
    #     if not isinstance(action,Action):
    #         raise TypeError(f"Introduce an Action object, not a {type(action).__name__}")
    #     if (action.origin == state.state) :
    #         #self.listOfActionsForRecoverPath.append(action) # si hacemos esto estariamos introduciendo todos los nodos
    #         return State(action.destination)
    #     raise Exception(f"No se puede aplicar la siguiente acción")
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
        
