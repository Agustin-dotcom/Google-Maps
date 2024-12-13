import sys
#sys.path.append('c:\\users\\agus\\appdata\\local\\programs\\python\\python312\\lib\\site-packages')
#from geographiclib.geodesic import Geodesic # pip install geographiclib
import heapq
sys.path.append('c:\\users\\agus\\appdata\\local\\programs\\python\\python312\\lib\\site-packages')
import numpy as np


from abc import ABC,abstractmethod
class Search(ABC):
    initial = 0
    final = 0
    a_star_total = 0
    a_star_real = 0
    evaluated_real = 0
    evaluated_total = 0
    time = dict()
    individuals_already_evaluated = dict()
    def __init__(self,problem):
        Search.evaluated_total = 0
        Search.evaluated_real = 0
        self.problem = problem
        self.openDS = [] # open_data_structure
        self.explored = {0}
        self.nodesGenerated = 0
    def insert(self,element):  
        self.openDS.append(element)
    def extract():
        pass
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       evaluation
    #////////////////////////////////////////////////////////////////////
    def evaluation(self,solution):#O(n^2)
        if tuple(solution) in Search.individuals_already_evaluated:
            Search.evaluated_total += 1
            return Search.individuals_already_evaluated.get(tuple(solution))
        total_population = 0 
        weight_per_candidate = 0
        
        # 1. Iterate through each station
        for idx,i in enumerate(self.problem.dictionary.get('candidates').values()): # O(n^2)
            min_of_all_a_star = 3600*5
            pop = i.get('population')
            total_population += pop 
            candidate = i.get('identifier') 
            Search.initial = candidate
            from Main import Main
            if Main.DEBUG_EVALUATION:
                print(f'place_id={candidate};citizens={pop}')
            # 2. Calculate the time from each candidate to a fixed station
            for idj,j in enumerate(self.problem.dictionary.get('candidates').values()): # O(n) 
                if solution[idj] == 0:
                    continue 
                station = j.get('identifier')
                Search.final = station 
                time_a_star = self.get_time_a_star() 
                from Main import Main
                if Main.DEBUG_EVALUATION:
                    print(f'to station with id {station} = {time_a_star}')
                if time_a_star < min_of_all_a_star:
                    min_of_all_a_star = time_a_star
            if min_of_all_a_star == 3600*5:
                continue
            if Main.DEBUG_EVALUATION:
                print(f'min_distance --> {min_of_all_a_star}')
            only_this_one = min_of_all_a_star * pop
            weight_per_candidate += only_this_one
            if Main.DEBUG_EVALUATION:
                print(f'accounting for ={only_this_one}')
                print(f'__________________________________________')
        Search.evaluated_real += 1
        Search.evaluated_total += 1
        Search.individuals_already_evaluated[tuple(solution)] = weight_per_candidate / total_population
        return Search.individuals_already_evaluated[tuple(solution)]
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       get_time_a_star
    #////////////////////////////////////////////////////////////////////
    def get_time_a_star(self):
        Search.a_star_total += 1
        if( not self.is_already_in_memory()): # if it is NOT in memory
            # save it in memory
            return self.save_changes()
        #otherwise just get it from memory
        return Search.time.get((Search.initial,Search.final))
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       is_already_in_memory
    #////////////////////////////////////////////////////////////////////
    def is_already_in_memory(self):
        return (Search.initial,Search.final) in Search.time
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       save_changes
    #////////////////////////////////////////////////////////////////////
    def save_changes(self):
        from AStar import AStar
        Search.a_star_real += 1
        instance_of_search = AStar(self.problem)
        time_a_star = instance_of_search.search()
        Search.time[(Search.initial,Search.final)] = time_a_star
        return time_a_star
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       search
    #////////////////////////////////////////////////////////////////////
    @abstractmethod
    def search(self):
       pass
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       generateARandomSolution
    #////////////////////////////////////////////////////////////////////
    def generateARandomSolution(self):
        length_of_array_of_candidates = len(self.problem.dictionary.get('candidates'))
        number_of_ones_we_need = self.problem.dictionary.get('number_stations')
        random_solution = np.zeros(length_of_array_of_candidates,dtype=int)
        positions_where_we_are_going_to_introduce_ones = np.random.choice(length_of_array_of_candidates,number_of_ones_we_need,replace = False)
        random_solution[positions_where_we_are_going_to_introduce_ones] = 1
        return random_solution
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       expand
    #////////////////////////////////////////////////////////////////////
    def expand(self,Node_param): #O(n)
        successors = []
        currentIntersection = self.problem.dictionary.get('intersections').get(Node_param.state.state) # O(1)

        listOrdered = sorted(currentIntersection.get("whereto"), key = lambda x:x['id']) # O(n*log(n)) # Timsort
        for destination in listOrdered: # O(n)
            """currentIntersection.get("whereto")
            [{'id': 1256026663, 'cost': 1.7331}, {'id': 1531659796, 'cost': 2.346}]"""
            if destination.get('id') in self.explored: # O(1) 
                continue
            from Action import Action
            newAction = Action(# O(1)
                    Node_param.state.state, 
                    destination.get("id"), 
                    destination.get("cost") 
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
    