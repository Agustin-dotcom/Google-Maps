from Search import Search
class RandomSearch(Search):
    def search(self,MaxIters):
        """
        This function is intended to solve the problem. At least, give a solution.
        As it is Random, I assume we are going to be exploiting all the time. Not really, we are going to be exploiting when we are evaluating 
        a given solution and exploring when we generate a random solution. The idea here is to balance exploitaion and exploration. I think
        it would be nice to have this one on the class RandomSearch, not here in Search.

        :param MaxIters: maximum of iterations you want to compute.
        """
        # Lesson 7 slide 27
        solution = self.generateARandomSolution()
        iteration = 0
        while (iteration < MaxIters):
            x = self.generateARandomSolution()
            print(f'Esta es la solucion random que acabamos de crear{x}')
            x_ = self.hillClimbing(x)
            if(self.evaluation(x_) > self.evaluation(solution)):
                solution = x_
            iteration += 1
        return solution