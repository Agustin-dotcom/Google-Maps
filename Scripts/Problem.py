import statistics
from State import State
from Action import Action
from Node import Node
import json
from collections import deque
class Problem:
    def __init__(self,file_name):#O(n)
        # Here, I read the dictionary
        self.nodesGenerated = 0
        self.exploredNodes = 0
        self.expandedNodes = 0
        self.depth = 0
        self.totalCost = 0.0
        self.explored = set()
        with open(file_name,'r') as file:
            self.dictionary = json.load(file)
            # Conversión de velocidad de km/h a m/s y cálculo del coste
       # Convert the list of intersections to a dictionary of dictionaries
        self.dictionary['maxSpeedOfAllSpeeds'] = float('-inf') # definiendo la maxima velocida a menos infinito
        self.dictionary['mostRepeatedSpeed'] = []
        self.dictionary['intersections'] = {inter['identifier']: inter for inter in self.dictionary.get('intersections')}# O(m)
        
        # Add the 'whereto' attribute to each intersection
        for inter in self.dictionary['intersections'].values():# O(m)
            inter['whereto'] = []

        # Populate the 'whereto' attribute based on the segments
        for segment in self.dictionary.get('segments'):# O(n)
            origin = segment['origin']#O(1)
            destination = segment['destination'] #O(1)
            distance = segment['distance'] #O(1)
            speed_kmh = segment['speed'] # O(1)

            # Convert speed from km/h to m/s
            speed_ms = speed_kmh * (1000 / 3600)
            self.dictionary['mostRepeatedSpeed'].append(speed_ms)
            # Si tenemos una velocidad mayor a la predeterminada, la cogemos
            if(speed_ms > self.dictionary.get('maxSpeedOfAllSpeeds')):#O(1)
                self.dictionary['maxSpeedOfAllSpeeds'] = speed_ms
    
            # Calculate the cost
            cost = distance / speed_ms
    
            # Add the destination and cost to the 'whereto' attribute of the origin intersection
            if origin in self.dictionary.get('intersections'): # O(1)
                self.dictionary.get('intersections').get(origin).get('whereto').append({'id': destination, 'cost': cost})
                # Convertir la lista de intersecciones a un diccionario donde la clave sea el 'identifier'
                #self.dictionary['intersections'] = {intersection['identifier']: {**intersection, 'whereto': set()} for intersection in self.dictionary.get('intersections')}
        self.dictionary['mostRepeatedSpeed'] = statistics.multimode(self.dictionary.get('mostRepeatedSpeed')) # O(1)
        self.initializeOpen(self.dictionary.get('initial')) # inicializo nodo raiz # O(1)
        
    def initializeOpen(self,initial): # O(1)
        longitudeInitialNode = self.dictionary.get('intersections').get(initial).get('longitude')
        latitudeInitialNode = self.dictionary.get('intersections').get(initial).get('latitude')
        self.root = Node(None,State(initial,longitudeInitialNode,latitudeInitialNode),Action(None,initial,0),0,0) # no estoy seguro si para llegar al nodo raiz action == None
        self.nodesGenerated+=1
        self.root.momento = self.nodesGenerated
    #################################################################################
    ####################             search              ############################
    #################################################################################
    def search(self,search_param): # O(n)
        """:param search_param: strategy to use
        
        :returns: empty list of list of actions"""
        search_param.insert(self.root)
        while len(search_param.openDS)!=0:    
            node = search_param.extract() # O(1) 
            self.exploredNodes +=1
            if node.state.state not in self.explored:
                if(self.testGoal(node)): 
                    self.depth = node.depth
                    self.totalCost = node.accumulatedCost
                    return self.recoverPath(node,[],0)
                successors1 = self.expand(node) # O(n)
                if (len(successors1)>0):
                    self.expandedNodes+=1
                for  successor in successors1: # O(n)
                    search_param.insert(successor) # O(1)
                self.explored.add(node.state.state) #  node.state es el objeto y node.state.state es la variable en el objeto state
        print("Solución no encontrada y hemos recorrido todo el árbol")
        return search_param.openDS

     #################################################################################
    ####################             testGoal              ############################
    #################################################################################
    def testGoal(self,node):# O(1)
        return self.dictionary.get('final') == node.state.state# node.state es de tipo State y node.state.state es de tipo int
    #################################################################################
    ####################             expand             ############################
    #################################################################################
    def expand(self,Node_param): #O(n)
        """ 
        :param Node_param: nodo al que apuntamos 
        :returns: list of nodes """
        successors = []
        currentIntersection = self.dictionary.get('intersections').get(Node_param.state.state) # O(1)

        listOrdered = sorted(currentIntersection.get("whereto"), key = lambda x:x['id']) # O(n*log(n)) # Timsort
        for destination in listOrdered: # O(n)
            """currentIntersection.get("whereto")
            [{'id': 1256026663, 'cost': 1.7331}, {'id': 1531659796, 'cost': 2.346}]"""
            if destination.get('id') in self.explored: # O(1) # preguntamos si ya lo hemos recorrido
                continue
            newAction = Action(# O(1)
                    Node_param.state.state, #origen
                    destination.get("id"), # destino
                    destination.get("cost") #coste
                )
            # REMEMBER THAT destination is A DICTIONARY {"id":,"cost":}
            newState = State(newAction.destination,self.dictionary.get('intersections').get(destination.get('id')).get('longitude'),self.dictionary.get('intersections').get(destination.get('id')).get('latitude')) #self.applyAction(Node_param.state,action) # Node.state es un objeto de tipo state
            newNode = Node(Node_param,newState,newAction,Node_param.depth+1,Node_param.accumulatedCost+newAction.cost)
            self.nodesGenerated+=1
            newNode.momento = self.nodesGenerated
            successors.append(newNode)
        return successors
    def recoverPath(self,node,list_param,total_cost):# O(n)
        if node.parent is None:# O(1)
            temp = []# O(1)
            i = deque(list_param)
            while  len(i) != 0:# O(n)
                temp.append(i.pop())# O(1)
            return temp
        else:
            list_param.append(node.action)# O(1)
            total_cost = total_cost + node.action.cost
            return self.recoverPath(node.parent,list_param=list_param,total_cost=total_cost) # O(T) # not that expensive it could be worse