import math
from Search import Search
class AStar(Search):# takes into account g(n), not only h(n)
    def __init__(self):
        pass
    def computeHeuristic(self,node_param):
        """:params node_param : a node
        :returns : straight line distance from state of the parameter to the goal"""
        return super().computeHeuristic(node_param=node_param) + node_param.accumulatedCost