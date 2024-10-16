import math
import json
from collections import deque
class Search: # this is where we use inheritance
    def __init__(self,problem):
        self.openDS = deque()
        self.problem = problem
    def insert(self,successor):
        self.openDS.append(successor)
    def extract():
        pass
    def computeHeuristic(self,node_param):
        """:params node_param : a node
        :returns : straight line distance from state of the parameter to the goal"""
        goalId = self.problem.dictionary['final']
        thisIsWhatIWanted = [d for d in self.problem.dictionary['intersections'] if d['identifier'] ==goalId ][0]
        x2 = thisIsWhatIWanted.get("longitude")
        y2 = thisIsWhatIWanted.get("latitude")
        x1 = node_param.state.longitude
        y1 = node_param.state.latitude
        return math.sqrt((x2-x1)**2+(y2-y1)**2)