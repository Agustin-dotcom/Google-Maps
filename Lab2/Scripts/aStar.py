import heapq
from search import Search

class AStar(Search):# takes into account g(n), not only h(n)
    ##############################################################################################
    ############################################# insert #########################################
    ##############################################################################################
    def insert(self,element):
         # element is a node
        """self.openDS is by default a deque() (see Search __init__) so we
        have to convert deque() into a list"""
        self.openDS = list(self.openDS)
        heuristic = (self.computeHeuristic(element)/self.problem.dictionary.get('maxSpeedOfAllSpeeds'))+element.accumulatedCost
        #print('\n-----------\n'.join(map(str,self.openDS)))
        heapq.heappush(self.openDS,(heuristic,element)) # element is going to be a paired value (h,Node)
    ##############################################################################################
    ############################################ extract #########################################
    ##############################################################################################
    def extract(self): #O(1)
        # tenemos que extraer el que menor heurística tiene --> la heurística hace de prioridad
        return heapq.heappop(self.openDS)[1] # heapq es una priorityQueue sin ser una Queue sino una Heap
    ##############################################################################################
    ######################################## computeHeuristic ####################################
    ##############################################################################################
    def computeHeuristic(self,node_param): #O(1)
        """self.openDS is by default a deque() (see Search __init__) so we
        have to convert deque() into a list"""
        self.openDS = list(self.openDS) # medios para obtener lo que queremos
        goalId = self.final # Obtenemos estado final
        coord_1 = (node_param.state.longitude, node_param.state.latitude) # (longitude,latitude)
        coord_2 = (self.problem.dictionary.get('intersections').get(goalId).get('longitude'), 
        self.problem.dictionary.get('intersections').get(goalId).get('latitude'))  # (longitude,latitude)
        # Usar el elipsoide WGS84 para calcular la distancia
        geod = Geodesic.WGS84 # cosas de la librería
        resultado = geod.Inverse(coord_1[0], coord_1[1], coord_2[0], coord_2[1]) # cosas de la librería
        # Distancia en metros
        distancia = resultado['s12'] 
        return distancia
         ##############################################################################################
    ######################################### search #########################################
    ##############################################################################################
    def search(self,initial,final): # O(n) # y siempre buscamos de la misma forma
        """:param search_param: strategy to use
        
        :returns: empty list of list of actions"""
        self.initializeOpen(initial) # inicializo nodo raiz # O(1)
        self.insert(self.root)
        while len(self.openDS)!=0:    
            node = self.extract() # O(1) 
            self.exploredNodes +=1
            if node.state.state not in self.explored:
                if(self.testGoal(node,final)): 
                    self.depth = node.depth
                    self.totalCost = node.accumulatedCost
                    return node.accumulatedCost # the accumulated cost of the last node is the total cost of the path and that is exactly what we want
                successors1 = self.expand(node) # O(n)
                if (len(successors1)>0):
                    self.expandedNodes+=1
                for  successor in successors1: # O(n)
                    self.insert(successor) # O(1)
                self.explored.add(node.state.state) #  node.state es el objeto y node.state.state es la variable en el objeto state
        print("Solución no encontrada y hemos recorrido todo el árbol")
        # if A* gives an NaN result, we are going to be here since there is no path
        return float('inf')
    """notice that we work with a tuple
    so if we want to return a node we must say tuple[1]
    where the tuple is (heuristic,node)"""
    ##############################################################################################
    ######################################## initializeOpen ######################################
    ##############################################################################################
    def initializeOpen(self,initial): # O(1)
        longitudeInitialNode = self.problem.dictionary.get('intersections').get(initial).get('longitude')
        latitudeInitialNode = self.problem.dictionary.get('intersections').get(initial).get('latitude')
        self.root = Node(None,State(initial,longitudeInitialNode,latitudeInitialNode),Action(None,initial,0),0,0) # no estoy seguro si para llegar al nodo raiz action == None
        self.nodesGenerated+=1
        self.root.momento = self.nodesGenerated
    #################################################################################
    ####################             testGoal              ##########################
    #################################################################################
    def testGoal(self,node,final):# O(1)
        return final == node.state.state# node.state es de tipo State y node.state.state es de tipo int