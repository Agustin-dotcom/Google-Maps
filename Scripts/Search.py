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
    