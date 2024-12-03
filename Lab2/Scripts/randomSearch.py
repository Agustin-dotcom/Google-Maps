from Search import Search
class RandomSearch(Search):
    def search(self,MaxIters):
        iteration = 0
        list_of_solutions_with_corresponding_score = []
        while (iteration < MaxIters):
            x = self.generateARandomSolution()
            score = self.evaluation(x)
            import heapq
            heapq.heappush(list_of_solutions_with_corresponding_score,(score,x))
            print(f'This is the random solution we have just created {x}')
            #x_ = self.hillClimbing(x)
            #if(self.evaluation(x_) > self.evaluation(solution)):
            #    solution = x_
            iteration += 1
        return list_of_solutions_with_corresponding_score