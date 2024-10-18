import heapq
from Search import Search
class InformedSearch(Search):
    """notice that we work with a tuple
    so if we want to return a node we must say tuple[1]
    where the tuple is (heuristic,node)"""
    def extract(self):#We have to extract the one with the lowest f(n) = h(n)
        #if len(self.openDS)<1:
        #    raise Exception(ErrorMessage = "No puedes extraer algo que no existe")
        return heapq.heappop(self.openDS)[1]
    # def insert(self,element):#We have to insert taking into account f(n) as well (we call it h which is the priority the heuristic)
    #     # element is a node
    #     """self.openDS is by default a deque() (see Search __init__) so we
    #     have to convert deque() into a list"""
    #     self.openDS = list(self.openDS)
    #     heuristic = super().computeHeuristic(element)
    #     heapq.heappush(self.openDS,(heuristic,element)) # element is going to be a paired value (h,Node)