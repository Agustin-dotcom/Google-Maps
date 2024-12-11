from Search import Search
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#                       GeneticAlgorithm
#////////////////////////////////////////////////////////////////
class GeneticAlgorithm(Search):
    def __init__(self,problem):
        self.p = []
        super().__init__(problem)
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       search
    #/////////////////////////////////////////////////////////////////////
    from Replacement import Replacement
    def search(self,population_size,strategy = Replacement.PROPORTION_BASED_SELECTION):
        #Lesson 8 Slide 18
        
        self.p = self.generate_population(population_size) # O(n) # create candidate solutions (individuals)
        self.evaluate(self.p) # obtains  their score
        
        import heapq
        import numpy as np
        counter = 0
        while(True):# O(n)
            temp = self.p
            previous_current_solution = heapq.heappop(temp)[1]
            p_ = self.select_population(self.p,strategy) # Selects some individuals by score
            self.crossover(p_) #crosses pairs of selected individuals
            self.mutation(p_) # mutates the crossed individuals
            self.evaluate(p_) # obtains the score of the new individuals
            self.p = self.combine(self.p,p_) # forms the new generation            
            temp = self.p
            new_current_solution = heapq.heappop(temp)[1]
            condition = np.array_equal(previous_current_solution, new_current_solution)
            if condition:
                counter +=1
            if not condition:
                counter = 0
            if counter == 5:
                break
        return self.p
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       generate_population
    #////////////////////////////////////////////////////////////////////
    def generate_population(self,population_size):#O(n)
        population = []
        import heapq
        for _ in range(population_size):#O(n)
            heapq.heappush(population,(0,tuple(self.generateARandomSolution())))
        return population
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                           evaluate
    #/////////////////////////////////////////////////////////////////////
    def evaluate(self,population):
        total = 0
        import heapq
        list_for_heapq = []
        evaluation_values_not_to_be_calculated_again = []
        for i in range(len(population)):# O(n)
            evaluation_values_not_to_be_calculated_again.append(self.evaluation(population[i][1]))
            total += evaluation_values_not_to_be_calculated_again[i]
        for i in range(len(population)):# O(n)
            evaluation_value = evaluation_values_not_to_be_calculated_again[i]
            heapq.heappush(list_for_heapq,(evaluation_value,tuple(population[i])))
        population  = list_for_heapq
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                               select_population
    #/////////////////////////////////////////////////////////////////////////
    def select_population(self,population,strategy):
        k = len(population)
        new_population = []
        for _ in range(len(population)):
            # 1. Take k individuals randomly
            import numpy as np
            np.random.seed(42)
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
            # we must remove some ones
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
            for j in range(len(population[i][1])): # going through bits
                if random.uniform(0,1) <= mutation_rate:
                    population[i][1][j] = 1 - population[i][1].item(j) # mutate gene
        population = population
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       combine
    #/////////////////////////////////////////////////////////////////////////
    from Selection import Selection
    def combine(self,population_one,population_two,strategy_combine = Selection.REPLACEMENT):
        bag_of_individuals = []
        import heapq
        if  len(population_one) % 2 != 0:
            bag_of_individuals.append(heapq.heappop(population_one)[1])
        from Selection import Selection
        match(strategy_combine):
            case Selection.REPLACEMENT:
                return population_two
            case Selection.ELITISM:
                for _ in range(int(len(population_two)-1)):
                    bag_of_individuals.append(heapq.heappop(population_two)[1])
                bag_of_individuals.append(heapq.heappop(population_one)[1])
                return bag_of_individuals
            case Selection.TRUNCATION:
                for _ in range(int(len(population_one)/2)):
                    bag_of_individuals.append(heapq.heappop(population_one)[1])
                    bag_of_individuals.append(heapq.heappop(population_two)[1])
                return bag_of_individuals
            case _: 
                return population_two