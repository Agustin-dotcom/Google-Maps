import json
import os
class State:
    def __init__(self,current,acumulatedCost):
        self.current = current
        self.acumulatedCost = acumulatedCost
class Node:
    def __init__(self,parent,state,action):
        self.parent = parent
        self.state = state # we want it to be type State
        self.action = action # the same with action is going to be a class
class Problem: # TODO
    def __init__(self,file_name):
        with open(file_name,'r') as file:
            new_dictionary = json.load(file)
            for i in new_dictionary['intersections']:
                i['whereto'] = [(j['destination'],j['distance']/j['speed']) for j in new_dictionary['segments'] if j['origin'] == i['identifier']]

class Action: # Maybe we can receive a state and return a new one 
    def __init__(self,action):
        self.action = action
    pass # TODO
def main():
    problem = Problem('paseo_simón_abril_albacete_250_1')
main()