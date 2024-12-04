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
        
        p = self.generate_population(population_size) # O(n) # create candidate solutions (individuals)
        p = self.evaluate(p) # obtains  their score

        while(population_size != 0 ):# O(n)
            p_ = self.select_population(p) # Selects some individuals by score
            p_ = self.crossover(p_) #crosses pairs of selected individuals
            p_ = self.mutation(p_) # mutates the crossed individuals
            p_ = self.evaluate(p_) # obtains the score of the new individuals
            p = self.combine(p,p_) # forms the new generation            
            population_size-=1
        return p
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       generate_population
    #////////////////////////////////////////////////////////////////////
    def generate_population(self,population_size):#O(n)
        population = []
        import math
        no_bigger_than_this = math.comb(len(self.problem.dictionary.get("candidates")),self.problem.dictionary.get("number_stations"))

        if (population_size > no_bigger_than_this):
            #print(f'If you have {population_size} of random solutions, you are going to either have wrong solutions or repeated ones')
            #print(f'Reassigning to {no_bigger_than_this} random solutions')
            population_size = no_bigger_than_this
        for _ in range(population_size):#O(n)
            population.append(self.generateARandomSolution())#O(1)
        return population
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                           evaluate
    #/////////////////////////////////////////////////////////////////////
    def evaluate(self,population):
        """:param population : a list 
         :returns: a heapq of paired value (score,solution)"""
        heapq_list = []
        import heapq
        for i in range(len(population)):# O(n)
            heapq.heappush(heapq_list,((1/self.evaluation(population[i])),tuple(population[i]))) # (score,solution)
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
        for _ in range(
            np.random.choice(
                range(
                    int(len(population)/2),
                    len(population)
                )
            ).item()
        ):
            elite_population.append((heapq.heappop(population))[1])
        return elite_population
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                               crossover
    #//////////////////////////////////////////////////////////////////////
    def crossover(self,population):
        if len(population) % 2 != 0:
            population = population[:-1]
        first_half = []
        # print(len(deque_list))
        # print(len(deque_list)/2)
        for i in range(int(len(population)/2)):
            first_half.append(population[i])
            population = population[:-1]
        final_crossover = []
        for i in range(len(population)):
            #print(f'Parents\n \t\t Parent1:{population[i]}\n\t\t Parent2:{first_half[i]}\n')
            list_of_two_children = self.join_these_two(population[i],first_half[i])
            #print(f'Children \n')
            for j in range(len(list_of_two_children)):
                #print(f'\t\tChild{j+1}:{list_of_two_children[j]}\n')
                final_crossover.append(list_of_two_children[j])
        return final_crossover
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                               join_these_two
    #//////////////////////////////////////////////////////////////////////
    def join_these_two(self,parent_one,parent_two):
        # 1. Pick a random split
        places_in_which_we_can_split = len(self.problem.dictionary.get('candidates')) -1
        import numpy as np
        point_in_which_we_split = np.random.choice(range(places_in_which_we_can_split))+1
        #2. Cross parents
        list_of_children = []
        first_child = np.concatenate((parent_one[:point_in_which_we_split] ,parent_two[point_in_which_we_split:]),axis=None)
        list_of_children.append(first_child)
        second_child =np.concatenate(( parent_one[point_in_which_we_split:] , parent_two [:point_in_which_we_split]),axis=None)
        list_of_children.append(second_child)
        return list_of_children
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       mutation
    #//////////////////////////////////////////////////////////////////////
    def mutation(self,population):
        mutation_rate = 0.1
        import random
        
        for i in range(len(population)): # going through solutions
            for j in range(len(population[i])): # going through bits
                if random.uniform(0,1) <= mutation_rate:
                    population[i][j] = 1 - population[i].item(j) # mutate gene
        return population
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       combine
    #/////////////////////////////////////////////////////////////////////////
    def combine(self,population_one,population_two):
        """
        :returns truncation_policy_list : a population
        """
        # 1. Truncation: Selects the best individuals among both population (P and P')
        # 2. Elitism: Preserves the best individual in the former population and sacrifices the worst one in the new one.
        # In other words, take P' and the worst indivual interchanges with the best in P
        # 3. Replacement: In this case, the generated population replaces the former one.
        truncation_policy_list = []
        import heapq
        if  len(population_one) % 2 != 0:
            truncation_policy_list.append(heapq.heappop(population_one)[1])
        for _ in range(int(len(population_one)/2)):
            truncation_policy_list.append(heapq.heappop(population_one)[1])
            truncation_policy_list.append(heapq.heappop(population_two)[1])
        return self.evaluate(truncation_policy_list)