import heapq
# import os
# import os
# os.chdir("c:\\users\\agus\\appdata\\local\\programs\\python\\python312\\lib\\site-packages")
import sys
sys.path.append('c:\\users\\agus\\appdata\\local\\programs\\python\\python312\\lib\\site-packages')
from geographiclib.geodesic import Geodesic
from InformedSearch import InformedSearch
class AStarGeodesicWithMostRepeatedSpeed(InformedSearch):
        # def computeHeuristic(self,node_param):
        #     """:params node_param : a node
        #     :returns : straight line distance from state of the parameter to the goal"""
        #     return super().computeHeuristic(node_param=node_param) + node_param.accumulatedCost
        #def __init__(self):
        #    self.openDS = deque()
    def insert(self,element):
         # element is a node
        """self.openDS is by default a deque() (see Search __init__) so we
        have to convert deque() into a list"""
        self.openDS = list(self.openDS)
         # Coordenadas de los dos puntos
        goalId = self.problem.dictionary.get('final')
        coord_1 = (element.state.longitude, element.state.latitude) 
        coord_2 = (self.problem.dictionary.get('intersections').get(goalId).get('longitude'), 
                   self.problem.dictionary.get('intersections').get(goalId).get('latitude'))  

        # Usar el elipsoide WGS84 para calcular la distancia
        geod = Geodesic.WGS84
        resultado = geod.Inverse(coord_1[0], coord_1[1], coord_2[0], coord_2[1])

        # Distancia en metros
        distancia = resultado['s12'] 
        # f(n) = h(n) + g(n) donde la heuristica es la distancia euclidea a la meta entre la maxima velocidad de entre todas las velocidades que tenemos  
        heuristic = (distancia/self.problem.dictionary.get('mostRepeatedSpeed')[0])+element.accumulatedCost
        #print('\n-----------\n'.join(map(str,self.openDS)))
        heapq.heappush(self.openDS,(heuristic,element)) # element is going to be a paired value (h,Node)