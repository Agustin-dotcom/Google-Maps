from Search import Search
from Solution import Solution
import heapq
import numpy as np
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#                       GeneticAlgorithm
#////////////////////////////////////////////////////////////////
class GeneticAlgorithm(Search):
    def __init__(self,problem):
        self.p = []
        self.p_ = []
        self.momento_solution = 0
        Search.a_star_real = 0
        Search.a_star_total = 0
        super().__init__(problem)
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       search
    #/////////////////////////////////////////////////////////////////////
    from Replacement import Replacement
    
    def search(self,population_size = 200):
        #Lesson 8 Slide 18
        
        self.p = self.generate_population(population_size) # O(n) # create candidate solutions (individuals)
        self.p = self.evaluate(self.p) # obtains  their score
        

        number_of_generations = 50
        while(number_of_generations != 0):# O(n)
            self.p_ = self.select_population(self.p) # Selects some individuals by score
            self.p_ = self.crossover(self.p_) #crosses pairs of selected individuals
            self.p_ = self.mutation(self.p_) # mutates the crossed individuals
            self.p_ = self.evaluate(self.p_) # obtains the score of the new individuals
            self.p = self.combine(self.p,self.p_) # forms the new generation            
            number_of_generations -= 1
        return self.p
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       generate_population
    #////////////////////////////////////////////////////////////////////
    
    def generate_population(self,population_size):#O(n)
        population = []
        import heapq
        for _ in range(population_size):#O(n)
            heapq.heappush(population,Solution(0,self.generateARandomSolution()))
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
            evaluation_values_not_to_be_calculated_again.append(self.evaluation(population[i].solution))
            total += evaluation_values_not_to_be_calculated_again[i]
        for i in range(len(population)):# O(n)
            evaluation_value = evaluation_values_not_to_be_calculated_again[i]
            heapq.heappush(list_for_heapq,Solution(evaluation_value,population[i].solution))
        return list_for_heapq
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                               select_population
    #/////////////////////////////////////////////////////////////////////////
    def select_population(self,population):
        length_of_the_list_of_individuals = len(population)
        new_population = []
        # 1. Take k individuals randomly
        k = 3 #np.random.randint(1,length_of_the_list_of_individuals+1)
        for _ in range(len(population)):
            import numpy as np
            import heapq
            # 2. Play the tournament
            tournament = []
            for _ in range(k):
                take_this_population = np.random.randint(0,length_of_the_list_of_individuals)
                heapq.heappush(tournament,population[take_this_population])
            new_population.append(heapq.heappop(tournament))
        return new_population
        
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                               crossover
    #//////////////////////////////////////////////////////////////////////
    def crossover(self,population):
        if len(population) % 2 != 0:
            population = population[:-1]
        first_half = []
        for i in range(int(len(population)/2)):
            first_half.append(population[0])
            population = population[1:]
        final_crossover = []
        for i in range(len(population)):
            list_of_two_children = self.join_these_two(population[i].solution,first_half[i].solution)
            population[i].solution = list_of_two_children[0]
            first_half[i].solution = list_of_two_children[1]
            final_crossover.append(population[i])
            final_crossover.append(first_half[i])
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
        mutation_rate = 0.2
        import random
        for i in range(len(population)): # going through solutions
            if random.uniform(0,1) <= mutation_rate:
                positions_where_zeros_are = np.where(population[i].solution == 0)[0]
                in_this_position_there_is_a_ZERO = np.random.choice(positions_where_zeros_are,1, replace = False)
                j = in_this_position_there_is_a_ZERO
                population[i].solution[j] = 1 # mutate gene
                positions_where_ones_are = np.where(population[i].solution == 1)[0]
                in_this_position_there_is_a_ONE = np.random.choice(positions_where_ones_are,1,replace = False)
                j = in_this_position_there_is_a_ONE
                population[i].solution[j] = 0  # mutate gene
        return population
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       combine
    #/////////////////////////////////////////////////////////////////////////
    from Selection import Selection
    def combine(self,population_one,population_two,strategy_combine = Selection.TRUNCATION):
        bag_of_individuals = []
        import heapq
        if  len(population_one) % 2 != 0:
            bag_of_individuals.append(heapq.heappop(population_one))
        from Selection import Selection
        match(strategy_combine):
            case Selection.REPLACEMENT:
                return population_two
            case Selection.ELITISM:
                for _ in range(int(len(population_two)-1)):
                    bag_of_individuals.append(heapq.heappop(population_two))
                bag_of_individuals.append(heapq.heappop(population_one))
                return bag_of_individuals
            case Selection.TRUNCATION:
                for _ in range(int(len(population_one)/2)):
                    bag_of_individuals.append(heapq.heappop(population_one))
                    bag_of_individuals.append(heapq.heappop(population_two))
                return bag_of_individuals
            case _: 
                return population_two