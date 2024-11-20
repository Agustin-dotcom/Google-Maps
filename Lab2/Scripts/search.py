import sys
sys.path.append('c:\\users\\agus\\appdata\\local\\programs\\python\\python312\\lib\\site-packages')
from geographiclib.geodesic import Geodesic # pip install geographiclib
import heapq
from abc import ABC,abstractmethod
class Search(ABC):
    def __init__(self,problem):
        self.problem = problem
        self.openDS = []
    def insert(self,element): # siempre insertamos de la misma forma
        self.openDS.append(element)
    @abstractmethod
    def extract():
        pass
    @abstractmethod
    def evaluation():
        pass
    def search(self,search_param): # O(n) # y siempre buscamos de la misma forma
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
    """notice that we work with a tuple
    so if we want to return a node we must say tuple[1]
    where the tuple is (heuristic,node)"""
    def extract(self): #O(1)
        # tenemos que extraer el que menor heurística tiene --> la heurística hace de prioridad
        return heapq.heappop(self.openDS)[1] # heapq es una priorityQueue sin ser una Queue sino una Heap
    def computeHeuristic(self,node_param): #O(1)
        """self.openDS is by default a deque() (see Search __init__) so we
        have to convert deque() into a list"""
        self.openDS = list(self.openDS) # medios para obtener lo que queremos
        goalId = self.problem.dictionary.get('final') # Obtenemos estado final
        coord_1 = (node_param.state.longitude, node_param.state.latitude) # (longitude,latitude)
        coord_2 = (self.problem.dictionary.get('intersections').get(goalId).get('longitude'), 
                   self.problem.dictionary.get('intersections').get(goalId).get('latitude'))  # (longitude,latitude)
        # Usar el elipsoide WGS84 para calcular la distancia
        geod = Geodesic.WGS84 # cosas de la librería
        resultado = geod.Inverse(coord_1[0], coord_1[1], coord_2[0], coord_2[1]) # cosas de la librería
        # Distancia en metros
        distancia = resultado['s12'] 
        return distancia
    def correctPossibleNumberStations(currentConfiguration):
        """
        :params currentConfiguration:  
        """
        # if in our list or dictionary (current configuration) we have more stations
        # than possible, we remove some
        counterStations = 0
        for i in self.problem.get('candidates')
        while (!counterStations < ) 