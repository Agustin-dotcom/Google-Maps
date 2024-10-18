from collections import deque
import math
import heapq # O(log n )
from Search import Search
from InformedSearch import InformedSearch
class BestFirst(InformedSearch): # takes into account only h(n)
    def computeHeuristic(self,node_param):
        """:params node_param : a node
        :returns : straight line distance from state of the parameter to the goal"""
        return super().computeHeuristic(node_param=node_param)
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
    