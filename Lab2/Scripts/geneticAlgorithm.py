from Search import Search
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#                       GeneticAlgorithm
#////////////////////////////////////////////////////////////////
class GeneticAlgorithm(Search):
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       search
    #/////////////////////////////////////////////////////////////////////
    from Replacement import Replacement
    def search(self,population_size,strategy = Replacement.PROPORTION_BASED_SELECTION):
        #Lesson 8 Slide 18
        
        p = self.generate_population(population_size) # O(n) # create candidate solutions (individuals)
        #p = self.evaluate(p) # obtains  their score

        while(population_size != 0 ):# O(n)
            p_ = self.select_population(p,strategy) # Selects some individuals by score
            p_ = self.crossover(p_) #crosses pairs of selected individuals
            p_ = self.mutation(p_) # mutates the crossed individuals
            #p_ = self.evaluate(p_) # obtains the score of the new individuals
            p = self.combine(p,p_) # forms the new generation            
            population_size-=1
        return p
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       generate_population
    #////////////////////////////////////////////////////////////////////
    def generate_population(self,population_size):#O(n)
        population = []
        
        for _ in range(population_size):#O(n)
            population.append(self.generateARandomSolution())#O(1)
        return population
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                           evaluate
    #/////////////////////////////////////////////////////////////////////
    def evaluate(self,population):
        """:param population : a list 
         :returns: a heapq of paired value (score,solution)"""
        total = 0
        import numpy as np
        list_evaluation_of_different_solutions = np.array([])
        evaluation_value = 0
        for i in range(len(population)):# O(n)
            evaluation_value=self.evaluation(population[i])
            total+=evaluation_value
            list_evaluation_of_different_solutions.append(1/evaluation_value)
        for i in range(len(population)):#O(n)
            list_evaluation_of_different_solutions /= total 
        return list_evaluation_of_different_solutions
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                               select_population
    #/////////////////////////////////////////////////////////////////////////
    from Replacement import Replacement
    def select_population(self,population,strategy):
        """
        :param population: a set of solutions

        :returns : a generation with elitism and diversity 
        """
        from Replacement import Replacement
        match strategy:
            case Replacement.PROPORTION_BASED_SELECTION:
                return self.proportion_based_selection(population)
            case Replacement.RANK_ASSIGNATION:
                return self.rank_assignation(population)
            case Replacement.TOURNAMENT:
                return self.tournament_assignation(population)
            case _:
                return self.proportion_based_selection(population)
    def proportion_based_selection(self,population):
        import numpy as np
        evaluation = np.array([],dtype=float)
        total = 0
        # 1. Evaluate each individual 
        for i in range(len(population)):#O(n)
            evaluation = np.append(evaluation,self.evaluation(population[i]))
            total += evaluation.item(i)
        
        #if 0 in evaluation:
        #    print(f'You tried to divide by zero!')
        #    return 
        evaluation = 1/evaluation
        evaluation /= total
        import numpy as np
        # 2. Arrange the wheel
        evaluation = np.cumsum(evaluation)
        last = evaluation[len(evaluation)-1]
        # 3. Replicate individuals according to wheel
        new_generation = []
        for i in range(len(population)):#O(n)
            random_number = np.random.uniform(0,last)
            solution_to_get = np.where(random_number <= evaluation)[0]
            new_generation.append(population[solution_to_get])
        return new_generation
    def rank_assignation(self,population):
        evaluation = np.array([],dtype=float)
        N = len(population)
        # 1. Evaluate each individual 
        for i in range(len(population)):#O(n)
            evaluation.append(self.evaluation(population[i]))
        evaluation = 1/evaluation
        indices_where_we_have_the_data_before_making_the_sort = np.argsort(evaluation)[::-1]
        evaluation = np.sort(evaluation)
        evaluation = evaluation[::-1]
        denominator = N ** 2 + N
        for i in range(len(evaluation)):
            pos = i+1
            evaluation[i] = (2*(N-pos+1)/denominator)
        import numpy as np
        # 2. Arrange the wheel
        evaluation = np.cumsum(evaluation)
        last = evaluation[len(evaluation)-1]
        # 3. Replicate individuals according to wheel
        new_generation = []
        for i in range(len(population)):#O(n)
            random_number = np.random.uniform(0,last)
            solution_to_get = np.where(random_number <= evaluation)[0][0].item()
            new_generation.append(population[indices_where_we_have_the_data_before_making_the_sort[solution_to_get]])
        return new_generation
    def tournament_assignation(self,population):
        k = len(population)
        new_population = []
        for _ in range(len(population)):
            # 1. Take k individuals randomly
            import numpy as np
            import heapq
            number_of_individuals_to_take = np.random.randint(1,k+1)
            # 2. Play the tournament
            tournament = []
            for _ in range(number_of_individuals_to_take):
                take_this_population = np.random.randint(0,k)
                heapq.heappush(tournament,(self.evaluation(population[take_this_population]),tuple(population[take_this_population])))
            new_population.append(heapq.heappop(tournament)[1])
        return new_population
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                               crossover
    #//////////////////////////////////////////////////////////////////////
    def crossover(self,population):
        if (population == None):
            print(f'population == None')
            return
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
        places_in_which_we_can_split = len(self.problem.dictionary.get('candidates'))-1
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
    from Selection import Selection
    def combine(self,population_one,population_two,strategy_combine = Selection.REPLACEMENT):
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
        from Selection import Selection
        match(strategy_combine):
            case Selection.REPLACEMENT:
                return population_two
            case Selection.ELITISM:
                population_one_with_evaluation = []
                for i in range(len(population_one)):
                    heapq.heappush(population_one_with_evaluation,self.evaluation(population_one[i],tuple(population_one[i])))
                population_two_with_evaluation = []
                for i in range(len(population_two)):
                    heapq.heappush(population_two_with_evaluation,self.evaluation(population_two[i],tuple(population_two[i])))
                for _ in range(int(len(population_one)-1)):
                    truncation_policy_list.append(heapq.heappop(population_one_with_evaluation)[1])
                truncation_policy_list.append(heapq.heappop(population_two_with_evaluation)[1])
                return truncation_policy_list
            case Selection.TRUNCATION:
                population_one_with_evaluation = []
                for i in range(len(population_one)):
                    heapq.heappush(population_one_with_evaluation,self.evaluation(population_one[i],tuple(population_one[i])))
                population_two_with_evaluation = []
                for i in range(len(population_two)):
                    heapq.heappush(population_two_with_evaluation,self.evaluation(population_two[i],tuple(population_two[i])))
                for _ in range(int(len(population_one)/2)):
                    truncation_policy_list.append(heapq.heappop(population_one_with_evaluation)[1])
                    truncation_policy_list.append(heapq.heappop(population_two_with_evaluation)[1])
                return truncation_policy_list
            case _: 
                return population_two