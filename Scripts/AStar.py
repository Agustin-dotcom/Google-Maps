from collections import deque
import math
from Search import Search
from InformedSearch import InformedSearch
class AStar(InformedSearch):# takes into account g(n), not only h(n)
    def computeHeuristic(self,node_param):
        """:params node_param : a node
        :returns : straight line distance from state of the parameter to the goal"""
        return super().computeHeuristic(node_param=node_param) + node_param.accumulatedCost
    #def __init__(self):
    #    self.openDS = deque()
    