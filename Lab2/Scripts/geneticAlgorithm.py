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
        p = self.evaluate(p) # obtains  their score

        while(population_size != 0 ):# O(n)
            p_ = self.select_population(p,strategy) # Selects some individuals by score
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
        import heapq
        list_for_heapq = []
        for i in range(len(population)):
            total += self.evaluation(population[i])
        for i in range(len(population)):# O(n)
            evaluation_value=self.evaluation(population[i])
            evaluation_value = self.deal_with_division_by_zero(evaluation_value)
            evaluation_value /= total
            evaluation_value = -evaluation_value
            heapq.heappop(list_for_heapq,(evaluation_value,tuple(population[i])))
        return list_for_heapq
    def deal_with_division_by_zero(self,evaluation_value):
        if evaluation_value == 0:
            return float('inf')
        return 1/evaluation_value
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
        for i in range(len(population)):
            evaluation.append(-population[i][0])
        # 2. Arrange the wheel
        evaluation = np.cumsum(evaluation)
        last = float('inf')
        i = -1
        while last == float('inf'):
            last = evaluation[len(evaluation)+i]
            i-=1
        # 3. Replicate individuals according to wheel
        new_generation = []
        for i in range(len(population)):#O(n)
            random_number = np.random.uniform(0,last)
            solution_to_get = np.where(random_number <= evaluation)[0][0]
            new_generation.append(population[solution_to_get][1])
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
            population = population[1:]
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
        first_child = self.correctPossibleNumberStations(first_child)
        list_of_children.append(first_child)
        second_child =np.concatenate(( parent_one[point_in_which_we_split:] , parent_two [:point_in_which_we_split]),axis=None)
        second_child = self.correctPossibleNumberStations(second_child)
        list_of_children.append(second_child)
        return list_of_children
      ##############################################################################################
    ############################## correctPossibleNumberStations #################################
    ##############################################################################################
    def correctPossibleNumberStations(self,configuration):
        """
        In this function we correct the number of ceros and ones to our needs.
        :param configuration: ndarray from numpy library representing a binary array, a configuration, a solution, a chromosome
        """
        # we get the number of ones
        import numpy as np
        number_of_ones_we_must_have = self.problem.dictionary.get('number_stations')
        number_of_ones_we_have = np.count_nonzero(configuration==1)
        if (number_of_ones_we_have < number_of_ones_we_must_have):
            # we must introduce some ones
            difference = number_of_ones_we_must_have - number_of_ones_we_have
            positions_where_zeros_are = np.where(configuration == 0)[0]
            new_positions_ones = np.random.choice(positions_where_zeros_are,difference, replace = False)
            configuration[new_positions_ones] = 1
        if (number_of_ones_we_have > number_of_ones_we_must_have):
            # we compute the difference 
            difference =  number_of_ones_we_have - number_of_ones_we_must_have
            positions_where_ones_are = np.where(configuration==1)[0]
            new_positions_zero = np.random.choice(positions_where_ones_are,difference,replace = False)
            configuration[new_positions_zero] = 0
        return configuration
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