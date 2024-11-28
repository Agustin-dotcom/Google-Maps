import sys
sys.path.append('c:\\users\\agus\\appdata\\local\\programs\\python\\python312\\lib\\site-packages')
from geographiclib.geodesic import Geodesic # pip install geographiclib
import heapq
from abc import ABC,abstractmethod
class Search(ABC):
    def __init__(self,problem):
        self.problem = problem
        self.openDS = [] # open_data_structure
        self.nodesGenerated = 0
        self.initial = 0
        self.final = 0
    def insert(self,element): # siempre insertamos de la misma forma
        self.openDS.append(element)
    #@abstractmethod
    def extract():
        pass
    #@abstractmethod
    ##############################################################################################
    ######################################### evaluation #########################################
    ##############################################################################################
    def evaluation(self,solution):
        """
        Here is where we are going to store in memory the results of A* so that if in a near future we need it,
        we can go and look in memory, not performing all the calculations again. Also, bear in mind what was mentioned
        in the lab that if we are trying to minimize then we must take f_ = 1/f. In other words, if you want the
        highest score of the class, you want to transform a 10 to a 1/10 so that it is the smallest one of all.
        If you divide 1 over a number that is greater, then the ratio is going to be smaller.
        1/10 < 1/9. 10 is a better grade than 9 and as you want to keep the same information but minimizing,
        that is why we do the ratio. So, maybe we are going to have to do this here. We want to minimize the time
        we spend to go to a certain Service Station.
        :param solution: a given solution to be evaluated 
        """
        total_population = 0
        weight_per_station = 0
        for i in self.problem.dictionary.get('candidates').values():
            pop = i.get('population')
            total_population += pop
            initial = i.get('identifier')
            self.initial = initial
        
            for j in self.problem.dictionary.get('candidates').values():    
                final = j.get('identifier')
                self.final = final
                time_a_star = self.get_time_a_star(initial,final)
                weight_per_station += time_a_star * pop * solution[i]
                
        return weight_per_station / total_population
  ##############################################################################################
    ######################################### get_time_a_star #########################################
    ##############################################################################################
    def get_time_a_star(self,initial,final):
        
        if( not self.is_already_in_memory(initial,final)): # if it is NOT in memory
            # save it in memory
            return self.save_changes(initial,final)
        #otherwise just get it from memory
        return self.problem.dictionary.get('candidates').get(initial).get('time').get(final).get('A*')# get it from memory
           ##############################################################################################
    ######################################### is_already_in_memory #########################################
    ##############################################################################################
    def is_already_in_memory(self,initial,final):
        if ('time' in self.problem.dictionary.get('candidates').get(initial)):
            for i in self.problem.dictionary.get('candidates').get(initial).get('time').values():
                if(i.get('identifier') == final):
                    return True
        return False
        ##############################################################################################
    ######################################### save_changes #########################################
    ##############################################################################################
    def save_changes(self,initial,final):
        """
        The idea is saving a dictionary of dictionaries ('time') which for each candidate will store 
        where it can go and how much time it costs

        {'candidate1':{'identifier':,'population':,'time': {'identifier':,'A*':}},
        'candidate2':{'identifier':,'population':,'time':{'identifier':,'A*':}}}
        """
        instance_of_search = AStar(self.problem)
        time_a_star = instance_of_search.search(initial,final)
        if('time' in self.problem.dictionary.get('candidates').get(initial)):
            # just append it as it already exists
            self.problem.dictionary.get('candidates').get(initial).get('time')[final] = {'identifier':final,'A*':time_a_star}
            return time_a_star
        #create the attribute and store it
        self.problem.dictionary.get('candidates').get(initial)['time'] = dict()
        self.problem.dictionary.get('candidates').get(initial).get('time')[final] ={'identifier':final,'A*':time_a_star}
        return time_a_star
            
    def search(self):
       pass
    ##############################################################################################
    ############################## correctPossibleNumberStations #################################
    ##############################################################################################
    def correctPossibleNumberStations(self,configuration):
        """
        In this function we correct the number of ceros and ones to our needs.
        :param configuration: ndarray from numpy library representing a binary array, a configuration, a solution, a chromosome
        """
        # we get the number of ones
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
    ##############################################################################################
    ################################### generateARandomSolution ##################################
    ##############################################################################################
    def generateARandomSolution(self):
        """
        Function to create a random solution.
        
        """
        length_of_array_of_candidates = len(self.problem.dictionary.get('candidates'))
        number_of_ones_we_need = self.problem.dictionary.get('number_stations')
        random_solution = np.zeros(length_of_array_of_candidates,dtype=int)
        positions_where_we_are_going_to_introduce_ones = np.random.choice(length_of_array_of_candidates,number_of_ones_we_need,replace = False)
        random_solution[positions_where_we_are_going_to_introduce_ones] = 1
        return random_solution
    ##############################################################################################
    ######################################## hillClimbing ########################################
    ##############################################################################################
    def hillClimbing(self,initialSolution):
        """
        This is where we exploit, hill climb. We revise our neighbours.
        """
        #Lesson 7 Slide 13
        currentSolution = initialSolution
        currentScore = self.evaluation(currentSolution)
        improves = True
        while (improves):
            improves = False
            neighbours = self.generateNeighbours(currentSolution)
            for neighbour in neighbours:
                score = self.evaluation(neighbour)
                if (score > currentScore):
                    currentSolution = neighbour
                    currentScore = score
                    improves = True
        return currentScore
    ##############################################################################################
    ######################################## generateNeighbours ##################################
    ##############################################################################################
    def generateNeighbours(self,currentSolution):
        """
        We generate neighbours by just changing one bit at a time. Permutation.
        Notice that all the neighbours are not valid solutions. Maybe we can optimize this in a future.
        """
        neighbours = []
        for i in range(0,len(currentSolution)): # for the length of the array
            neighbour_ = currentSolution.copy()

            negihbour_[i] = 1 - neighbour_[i] # 1-0 is 1 and 1-1 = 0 so that we change the bit 
            condition = checkIfThisIsASolution(neighbour_) # if it is a valid solution
            if (condition):
                neighbours.append(negihbour_) # we put it into our bag of solutions
                
        return np.array(neighbours)
    ##############################################################################################
    ######################################## checkIfThisIsASolution ##############################
    ##############################################################################################
    def checkIfThisIsASolution(self,solution):
        """
        Checks if a given solution is valid.
        :param solution: given solution
        :return boolean: returns a boolean
        """
        number_of_ones_in_this_solution = np.count_nonzero(solution==1) # gets the number of zeros we have in the solution passed by parameter
        return number_of_ones_in_this_solution == self.problem.dictionary.get('number_stations') # returns true if it has the number of stations 
        #we must submit
    