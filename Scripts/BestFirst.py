import heapq # O(log n )
from Search import Search
class BestFirst(Search): # takes into account only h(n)
    def __init__(self):
        self.openDS = []
    def extract(self):#We have to extract the one with the lowest f(n) = h(n)
        if len(self.openDS)<1:
            raise Exception(ErrorMessage = "No puedes extraer algo que no existe")
        return heapq.heappop(self.openDS)
    def insert(self,element):#We have to insert taking into account f(n) as well (we call it h which is the priority the heuristic)
        heapq.heappush(self.openDS,element) # element is going to be a paired value (h,Node)