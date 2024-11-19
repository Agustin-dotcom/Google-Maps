import heapq
from search import Search

class AStar(Search):
    def __init__(self):
        self.super()
    def insert(self,element):
         # element is a node
        """self.openDS is by default a deque() (see Search __init__) so we
        have to convert deque() into a list"""
        self.openDS = list(self.openDS)
        heuristic = (super().computeHeuristic(element)/self.problem.dictionary.get('maxSpeedOfAllSpeeds'))+element.accumulatedCost
        #print('\n-----------\n'.join(map(str,self.openDS)))
        heapq.heappush(self.openDS,(heuristic,element)) # element is going to be a paired value (h,Node)