
import heapq
from Search import Search
class AStar(Search):# takes into account g(n), not only h(n)
    def __init__(self):
        self.openDS = []
    def extract(self):#We have to extract the one with the lowest f(n) = h(n)
        #if len(self.openDS)<1:
        #    raise Exception(ErrorMessage = "No puedes extraer algo que no existe")
        return heapq.heappop(self.openDS)
    def insert(self,element):#We have to insert taking into account f(n) as well (we call it h which is the priority the heuristic)
        # element is a node
        heuristic = super().computeHeuristic(node_param=element)
        heapq.heappush(self.openDS,(heuristic,element)) # element is going to be a paired value (h,Node)
    def computeHeuristic(self,node_param):
        """:params node_param : a node
        :returns : straight line distance from state of the parameter to the goal"""
        return super().computeHeuristic(node_param=node_param) + node_param.accumulatedCost