from InformedSearch import InformedSearch
import heapq
class AStarAssumingOneHundredAndTwentyKilometersPerHour(InformedSearch):
    def insert(self,element):
         # element is a node
        """self.openDS is by default a deque() (see Search __init__) so we
        have to convert deque() into a list"""
        self.openDS = list(self.openDS)
        hundredTwentyKilometersPerHour = 120
        metersPerSecond = hundredTwentyKilometersPerHour * (1000/3600)
        # f(n) = h(n) + g(n) donde la heuristica es la distancia euclidea a la meta entre la maxima velocidad de entre todas las velocidades que tenemos  
        heuristic = (super().computeHeuristic(element)/metersPerSecond)+element.accumulatedCost
        #print('\n-----------\n'.join(map(str,self.openDS)))
        heapq.heappush(self.openDS,(heuristic,element)) # element is going to be a paired value (h,Node)