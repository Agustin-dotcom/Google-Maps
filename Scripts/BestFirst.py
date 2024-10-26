from InformedSearch import InformedSearch
import heapq # O(log n )
class BestFirst(InformedSearch): # takes into account only h(n)
     # element is a node
     def insert(self,element): #O(1)
        """self.openDS is by default a deque() (see Search __init__) so we
        have to convert deque() into a list"""
        self.openDS = list(self.openDS)
        heuristic = super().computeHeuristic(element)
        #print('\n-----------\n'.join(map(str,self.openDS)))
        heapq.heappush(self.openDS,(heuristic,element)) # element is going to be a paired value (h,Node)