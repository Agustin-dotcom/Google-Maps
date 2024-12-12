from Search import Search
from Solution import Solution
class RandomSearch(Search):
    def search(self,MaxIters = 50):
        iteration = 0
        list_of_solutions_with_corresponding_score = []
        while (iteration < MaxIters):
            x =Solution(0,self.generateARandomSolution(),Solution.momento)
            Solution.momento += 1
            score = self.evaluation(x.solution)
            import heapq
            x.score = score
            heapq.heappush(list_of_solutions_with_corresponding_score,x)
            list_of_solutions_with_corresponding_score.sort()
            print(f'This is the random solution we have just created {x}')
            iteration += 1
        return list_of_solutions_with_corresponding_score