import sys
#sys.path.append('c:\\users\\agus\\appdata\\local\\programs\\python\\python312\\lib\\site-packages')
#from geographiclib.geodesic import Geodesic # pip install geographiclib
import heapq
sys.path.append('c:\\users\\agus\\appdata\\local\\programs\\python\\python312\\lib\\site-packages')
import numpy as np

from abc import ABC,abstractmethod
class Search:
    def __init__(self,problem):
        self.problem = problem
        self.openDS = [] # open_data_structure
        self.explored = {0}
        self.nodesGenerated = 0
        #self.initial = 0
        #self.final = 0
    def insert(self,element): # siempre insertamos de la misma forma
        self.openDS.append(element)
    #@abstractmethod
    def extract():
        pass
    #@abstractmethod
    ##############################################################################################
    ######################################### evaluation #########################################
    ##############################################################################################
    def evaluation(self,solution):#O(n^2)
        print(f'def evaluation: Solucion antes de evaluarla {solution}')
        total_population = 0 # this is for the denominator
        min_of_all_stations_weight = float('inf') # this is for the second summatory on the evaluation function
        for idx,i in enumerate(self.problem.dictionary.get('candidates').values()): # O(n^2)
            weight_per_station = 0  # this is for the summing all the times of the candidates to a given station
            if solution[idx] == 0: # if the solution does not inlude this candidate
                continue # skip it
            pop = i.get('population')
            total_population += pop # this is just getting the total population for the denominator on the evaluation function
            station = i.get('identifier') # we fix a pointer into a candidate and we call it station
            #self.final = station
        
            for j in self.problem.dictionary.get('candidates').values(): # O(n) # we go through the candidates
                candidate = j.get('identifier')
                #self.initial = candidate
                time_a_star = self.get_time_a_star(candidate,station) # and we calculate the time it takes every candidate to reach the pointed station
                weight_per_station += time_a_star * pop
            if weight_per_station == 0:
                continue
            if weight_per_station < min_of_all_stations_weight:
                min_of_all_stations_weight = weight_per_station
                          
        print(f'def evaluation: Solucion despues de haber hecho los calculos {solution}')
        return 1/(min_of_all_stations_weight / total_population) # we return the correct ratio
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
                    print(f'def is_already_in_memory: Ya lo tenemos en memoria!! No hace falta calcularlo!!')
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
        from AStar import AStar
        instance_of_search = AStar(self.problem)
        time_a_star = instance_of_search.search(initial,final)
        print(f' We just made a call to A* ')
        if(not 'time' in self.problem.dictionary.get('candidates').get(initial)):
            print(f' Antes no existia el campo time. ahora si 😎')
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
        return currentSolution
    ##############################################################################################
    ######################################## generateNeighbours ##################################
    ##############################################################################################
    def generateNeighbours(self,currentSolution):
        """
        We use shuffle which has O(n) complexity. 
        Shotout to Fisher-Yates algorithm.
        This is cheaper than permutating for sure and we 
        needn't check if the number of ones is the same as the number of stations.
        """
        neighbours = []
        import math
        number_of_possible_neighbours =math.comb(len(currentSolution),self.problem.dictionary.get('number_stations')) # this is material for the report --> intersection with math
        for _ in range(number_of_possible_neighbours): # for the length of the array
            neighbour_ = currentSolution.copy()
            # Encuentra los índices de todos los 1s y 0s en el array
            indices_unos = np.where(neighbour_ == 1)[0]
            indices_ceros = np.where(neighbour_ == 0)[0]
            print(f'indices_unos {indices_unos}')
            print(f'indices_ceros {indices_ceros}')
            
            
            # Selecciona un índice aleatorio de los 1s y un índice aleatorio de los 0s
            indice_uno = np.random.choice(indices_unos)
            indice_cero = np.random.choice(indices_ceros)
            
            # Intercambia los bits seleccionados
            neighbour_[indice_uno], neighbour_[indice_cero] = neighbour_[indice_cero], neighbour_[indice_uno]
            
            neighbours.append(neighbour_.tolist())    
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
    #################################################################################
    ####################             expand             ############################
    #################################################################################
    def expand(self,Node_param): #O(n)
        """ 
        :param Node_param: nodo al que apuntamos 
        :returns: list of nodes """
        successors = []
        currentIntersection = self.problem.dictionary.get('intersections').get(Node_param.state.state) # O(1)

        listOrdered = sorted(currentIntersection.get("whereto"), key = lambda x:x['id']) # O(n*log(n)) # Timsort
        for destination in listOrdered: # O(n)
            """currentIntersection.get("whereto")
            [{'id': 1256026663, 'cost': 1.7331}, {'id': 1531659796, 'cost': 2.346}]"""
            if destination.get('id') in self.explored: # O(1) # preguntamos si ya lo hemos recorrido
                continue
            from Action import Action
            newAction = Action(# O(1)
                    Node_param.state.state, #origen
                    destination.get("id"), # destino
                    destination.get("cost") #coste
                )
            # REMEMBER THAT destination is A DICTIONARY {"id":,"cost":}
            from State import State
            newState = State(newAction.destination,self.problem.dictionary.get('intersections').get(destination.get('id')).get('longitude'),self.problem.dictionary.get('intersections').get(destination.get('id')).get('latitude')) #self.applyAction(Node_param.state,action) # Node.state es un objeto de tipo state
            from Node import Node
            newNode = Node(Node_param,newState,newAction,Node_param.depth+1,Node_param.accumulatedCost+newAction.cost)
            self.nodesGenerated+=1
            newNode.momento = self.nodesGenerated
            successors.append(newNode)
        return successors
    