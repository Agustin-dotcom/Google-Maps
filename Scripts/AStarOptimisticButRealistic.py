from InformedSearch import InformedSearch
import heapq
class AStarOptimisticButRealistic(InformedSearch):
    def insert(self,element): #O(1)
         # element is a node
        """self.openDS is by default a deque() (see Search __init__) so we
        have to convert deque() into a list"""
        self.openDS = list(self.openDS)
        # f(n) = h(n) + g(n) donde la heuristica es la distancia euclidea a la meta entre la maxima velocidad de entre todas las velocidades que tenemos  
        heuristic = (super().computeHeuristic(element)/self.problem.dictionary.get('maxSpeedOfAllSpeeds'))+element.accumulatedCost
        #print('\n-----------\n'.join(map(str,self.openDS)))
        heapq.heappush(self.openDS,(heuristic,element)) # element is going to be a paired value (h,Node)