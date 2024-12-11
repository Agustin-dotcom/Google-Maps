import heapq
from Search import Search
import sys
sys.path.append('c:\\users\\agus\\appdata\\local\\programs\\python\\python312\\lib\\site-packages')
from geographiclib.geodesic import Geodesic # pip install geographiclib

class AStar(Search):# takes into account g(n), not only h(n)
    ##############################################################################################
    ############################################# insert #########################################
    ##############################################################################################
    def insert(self,element):
         # element is a node
        """self.openDS is by default a deque() (see Search __init__) so we
        have to convert deque() into a list"""
        goalId = Search.final
        self.openDS = list(self.openDS)
        heuristic = (self.computeHeuristic(element,goalId)/self.problem.dictionary.get('maxSpeedOfAllSpeeds'))+element.accumulatedCost
        #print('\n-----------\n'.join(map(str,self.openDS)))
        heapq.heappush(self.openDS,(heuristic,element)) # element is going to be a paired value (h,Node)
    ##############################################################################################
    ############################################ extract #########################################
    ##############################################################################################
    def extract(self): #O(1)
        return heapq.heappop(self.openDS)[1] 
    ##############################################################################################
    ######################################## computeHeuristic ####################################
    ##############################################################################################
    def computeHeuristic(self,node_param,goalId): #O(1)
        self.openDS = list(self.openDS) 
        coord_1 = (node_param.state.longitude, node_param.state.latitude) 
        coord_2 = (self.problem.dictionary.get('intersections').get(goalId).get('longitude'), 
        self.problem.dictionary.get('intersections').get(goalId).get('latitude'))   
        resultado = self.haversine(coord_1[0], coord_1[1], coord_2[0], coord_2[1]) 
        distancia = resultado * 1000
        return distancia

#////////////////////////////////////////////////////////////////////
#                   haversine
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
    def haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance in kilometers between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        from math import radians, cos, sin, asin, sqrt
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
        return c * r
    ##############################################################################################
    ######################################### search #########################################
    ##############################################################################################
    def search(self): # O(n) 
        self.initializeOpen(Search.initial) # O(1)
        self.insert(self.root)
        while len(self.openDS)!=0:    
            node = self.extract() # O(1) 
            if node.state.state not in self.explored:
                if(self.testGoal(node)): 
                    self.depth = node.depth
                    self.totalCost = node.accumulatedCost
                    return node.accumulatedCost 
                successors1 = self.expand(node) # O(n)
                for  successor in successors1: # O(n)
                    self.insert(successor) # O(1)
                self.explored.add(node.state.state) 
        return float('inf') 
    ##############################################################################################
    ######################################## initializeOpen ######################################
    ##############################################################################################
    def initializeOpen(self,initial): # O(1)
        longitudeInitialNode = self.problem.dictionary.get('intersections').get(initial).get('longitude')
        latitudeInitialNode = self.problem.dictionary.get('intersections').get(initial).get('latitude')
        from Node import Node
        from State import State
        from Action import Action
        self.root = Node(None,State(initial,longitudeInitialNode,latitudeInitialNode),Action(None,initial,0),0,0) # no estoy seguro si para llegar al nodo raiz action == None
        self.nodesGenerated+=1
        self.root.momento = self.nodesGenerated
    #################################################################################
    ####################             testGoal              ##########################
    #################################################################################
    def testGoal(self,node):# O(1)
        return Search.final == node.state.state# node.state es de tipo State y node.state.state es de tipo int