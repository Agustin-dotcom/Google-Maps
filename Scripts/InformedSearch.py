import heapq
from Search import Search
import sys
sys.path.append('c:\\users\\agus\\appdata\\local\\programs\\python\\python312\\lib\\site-packages')
from geographiclib.geodesic import Geodesic # pip install geographiclib
class InformedSearch(Search):
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