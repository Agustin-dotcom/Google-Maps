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
    def __init__(self,problem):
        self.problem = problem
        self.openDS = [] # open_data_structure
        self.explored = {0}
        self.nodesGenerated = 0
        self.time = dict()
    def insert(self,element):  
        self.openDS.append(element)
    def extract():
        pass
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       evaluation
    #////////////////////////////////////////////////////////////////////
    def evaluation(self,solution):#O(n^2)
        total_population = 0 
        weight_per_station = 0
        
        # 1. Iterate through each station
        for idx,i in enumerate(self.problem.dictionary.get('candidates').values()): # O(n^2)
            min_of_all_a_star = float('inf')
            if solution[idx] == 0:
                continue 
            pop = i.get('population')
            total_population += pop 
            station = i.get('identifier') 
            Search.final = station
            # 2. Calculate the time from each candidate to a fixed station
            for j in self.problem.dictionary.get('candidates').values(): # O(n) 
                candidate = j.get('identifier')
                print(f'place_id={candidate};citizens={pop}')
                Search.initial = candidate 
                time_a_star = self.get_time_a_star() 
                print(f'to station with id {station} = {time_a_star}')
                if time_a_star == 0:
                    continue
                if time_a_star < min_of_all_a_star:
                    min_of_all_a_star = time_a_star
            if min_of_all_a_star == float('inf'):
                continue
            weight_per_station += min_of_all_a_star * pop
        return weight_per_station / total_population 
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       get_time_a_star
    #////////////////////////////////////////////////////////////////////
    def get_time_a_star(self):
        
        if( not self.is_already_in_memory()): # if it is NOT in memory
            # save it in memory
            return self.save_changes()
        #otherwise just get it from memory
        return self.time.get((Search.initial,Search.final))
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       is_already_in_memory
    #////////////////////////////////////////////////////////////////////
    def is_already_in_memory(self):
        return (Search.initial,Search.final) in self.time
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #                       save_changes
    #////////////////////////////////////////////////////////////////////
    def save_changes(self):
        from AStar import AStar
        instance_of_search = AStar(self.problem)
        time_a_star = instance_of_search.search()
        self.time[(self.initial,self.final)] = time_a_star
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
        np.random.seed(42)
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
    