from collections import deque
import math
import heapq # O(log n )
from Search import Search
from InformedSearch import InformedSearch
class BestFirst(InformedSearch): # takes into account only h(n)
    # def computeHeuristic(self,node_param):
    #     """:params node_param : a node
    #     :returns : straight line distance from state of the parameter to the goal"""
    #     return super().computeHeuristic(node_param=node_param)
    #def __init__(self):
    #    self.openDS = deque()
    
            #################################################################################
    ###                    decideWhetherAStarOrBestFirst              ###############
    #################################################################################
    # def decideWhetherAStarOrBestFirst(node_param,argument):
    #     """:param node_param: nodo recientemente creado
    #         :param search_param: estrategia de búsqueda
            
    #         :returns: f(n)"""
    #     boolean = isinstance(argument,AStar)
    #     if(boolean):
    #         return node_param.accumulatedCost + node_param.heuristic#g(n)+h(n)
    #     return node_param.heuristic
    #################################################################################
    ####################             computeHeuristic              ############################
    #################################################################################
     # element is a node
     def insert(self,element):
        """self.openDS is by default a deque() (see Search __init__) so we
        have to convert deque() into a list"""
        self.openDS = list(self.openDS)
        heuristic = super().computeHeuristic(element)
        heapq.heappush(self.openDS,(heuristic,element)) # element is going to be a paired value (h,Node)