from Search import Search
from Solution import Solution
class RandomSearch(Search):
    def __init__(self,problem):
        Search.a_star_real = 0
        Search.a_star_total = 0
        super().__init__(problem)
    def search(self,MaxIters = 50):
        iteration = 0
        list_of_solutions_with_corresponding_score = []
        while (iteration < MaxIters):
            x =Solution(0,self.generateARandomSolution())
            score = self.evaluation(x.solution)
            import heapq
            x.score = score
            heapq.heappush(list_of_solutions_with_corresponding_score,x)
            iteration += 1
        return list_of_solutions_with_corresponding_score