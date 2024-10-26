from InformedSearch import InformedSearch
import heapq
class AStarGeodesicWithMostRepeatedSpeed(InformedSearch): #O(1)
    def insert(self,element):
        distancia = super().computeHeuristic(element) 
        # f(n) = h(n) + g(n) donde la heuristica es la distancia euclidea a la meta entre la velocidad más repetida entre todas las velocidades que tenemos  
        heuristic = (distancia/self.problem.dictionary.get('mostRepeatedSpeed')[0])+element.accumulatedCost
        #print('\n-----------\n'.join(map(str,self.openDS)))
        heapq.heappush(self.openDS,(heuristic,element)) # element is going to be a paired value (h,Node)