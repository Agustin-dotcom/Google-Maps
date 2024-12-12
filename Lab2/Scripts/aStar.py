import heapq
from Search import Search
import sys
sys.path.append('c:\\users\\agus\\appdata\\local\\programs\\python\\python312\\lib\\site-packages')
from geographiclib.geodesic import Geodesic # pip install geographiclib

class AStar(Search):# takes into account g(n), not only h(n)
    ##############################################################################################
    ############################################# insert #########################################
    ##############################################################################################
    def __init__(self,problem):
        self.distance = dict()
        super().__init__(problem)
    def insert(self,element):
        goalId = Search.final
        self.openDS = list(self.openDS)
        heuristic = (self.computeHeuristic(element,goalId)/self.problem.dictionary.get('maxSpeedOfAllSpeeds'))+element.accumulatedCost
        heapq.heappush(self.openDS,(heuristic,element))
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
        coord_1 = (
            node_param.state.longitude,
              node_param.state.latitude
              ) 
        coord_2 = (
            self.problem.dictionary.get('intersections').get(goalId).get('longitude'), 
        self.problem.dictionary.get('intersections').get(goalId).get('latitude')
        )   
        if (coord_1,coord_2) in self.distance:
            return self.distance.get((coord_1,coord_2))
        resultado = self.haversine(coord_1,coord_2)
        self.distance[(coord_1,coord_2)] = resultado 
        distancia = resultado * 1000
        return distancia

#////////////////////////////////////////////////////////////////////
#                   haversine
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
    def haversine(self,coord1,coord2):
        lon1,lat1=coord1
        lon2,lat2=coord2
        import math
        R=6371000                               # radius of Earth in meters
        phi_1=math.radians(lat1)
        phi_2=math.radians(lat2)

        delta_phi=math.radians(lat2-lat1)
        delta_lambda=math.radians(lon2-lon1)

        a=math.sin(delta_phi/2.0)**2+\
           math.cos(phi_1)*math.cos(phi_2)*\
           math.sin(delta_lambda/2.0)**2
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        
        meters=R*c                         # output distance in meters
        km=meters/1000.0              # output distance in kilometers
        return km
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
        self.root = Node(None,State(initial,longitudeInitialNode,latitudeInitialNode),Action(None,initial,0),0,0) 
        self.nodesGenerated+=1
        self.root.momento = self.nodesGenerated
    #################################################################################
    ####################             testGoal              ##########################
    #################################################################################
    def testGoal(self,node):# O(1)
        return Search.final == node.state.state