from Search import Search
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#                       GeneticAlgorithm
#////////////////////////////////////////////////////////////////
class GeneticAlgorithm(Search):
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       search
    #/////////////////////////////////////////////////////////////////////
    def search(self,population_size):
        #Lesson 8 Slide 18
        stop_condition = False
        p = self.generate_population(population_size) # create candidate solutions (individuals)
        p = self.evaluate(p) # obtains  their score
        while(stop_condition==False):
            p_ = self.select_population(p) # Selects some individuals by score
            p_ = self.crossover(p_) #crosses pairs of selected individuals
            p_ = self.mutation(p_) # mutates the crossed individuals
            p_ = self.evaluate(p_) # obtains the score of the new individuals
            p = self.combine(p,p_) # forms the new generation
        return p
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       generate_population
    #////////////////////////////////////////////////////////////////////
    def generate_population(self,population_size):
        population = []
        for _ in range(population_size):
            population.append(self.generateARandomSolution())
        return population
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                           evaluate
    #/////////////////////////////////////////////////////////////////////
    def evaluate(self,population):
        """:param population : a list 
         :returns: a heapq of paired value (score,solution)"""
        heapq_list = []
        import heapq
        for i in range(len(population)):
            heapq.heappush(heapq_list,(self.evaluation(population[i]),population[i])) # (score,solution)
        return heapq_list
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                               select_population
    #/////////////////////////////////////////////////////////////////////////
    def select_population(self,population):
        """
        :param population: a heapq with paired values (score,solution)
        :returns elite_population: a list of solutions with randomized length
        """
        elite_population = []
        import heapq
        import numpy as np
        for _ in np.random.choice(range(len(population)))+1:
            elite_population.append(heapq.heappop(population))[1]
        return elite_population
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                               crossover
    #//////////////////////////////////////////////////////////////////////
    def crossover(self,population):
        from collections import deque
        deque_list = deque(population)
        if len(population) %2 != 0:
            deque_list.popleft()
        first_half = []
        for _ in len(deque_list)/2:
            first_half.append(deque_list.pop())
        first_half = deque(first_half)
        final_crossover = []
        for _ in len(deque_list):
            final_crossover.append(self.join_these_two(deque_list.pop(),first_half.pop()))
        return final_crossover
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                               join_these_two
    #//////////////////////////////////////////////////////////////////////
    # 1. Pick a random split
        places_in_which_we_can_split = len(self.problem.dictionary.get('candidates'))
        #2. Cross parents
        pass
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       mutation
    #//////////////////////////////////////////////////////////////////////
    def mutation(self,population):
        mutation_rate = 0.1
        import random
        
        for i in len(population): # going through solutions
            for j in len(population[i]): # going through bits
                if random.uniform(0,1) <= mutation_rate:
                    population[i][j] = 1 - population[i][j] # mutate gene
        return population
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       combine
    #/////////////////////////////////////////////////////////////////////////
    def combine(self,population_one,population_two):
        """
        :returns truncation_policy_list : a population
        """
        truncation_policy_list = []
        import heapq
        if  len(population_one) % 2 != 0:
            truncation_policy_list.append(heapq.heappop(population_one)[1])
        for _ in len(population_one)//2:
            truncation_policy_list.append(heapq.heappop(population_one)[1])
            truncation_policy_list.append(heapq.heappop(population_two)[1])
        return truncation_policy_list