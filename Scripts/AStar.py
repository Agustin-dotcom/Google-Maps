import heapq
from collections import deque
import math
from Search import Search
from InformedSearch import InformedSearch
class AStar(InformedSearch):# takes into account g(n), not only h(n)
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
        heuristic = super().computeHeuristic(element)+element.accumulatedCost
        heapq.heappush(self.openDS,(heuristic,element)) # element is going to be a paired value (h,Node)