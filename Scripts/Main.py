from Scripts.Problem import Problem
from Scripts.BreadthFirst import BreadthFirst
from Scripts.DepthFirst import DepthFirst
from collections import deque
def main():
    #os.chdir("C:\googleMapsVS\Google-Maps")
    #problem = Problem("paseo_simón_abril_albacete_250_1.json")
    #print(problem.root)
    #clase1 = BreadthFirst()
    #cola = deque()
    #cola.append('a')s
    #cola.append('g')
    #print(clase1.extract(cola))
    #print(cola)
    #print(clase1.extract(cola))
    #print(cola)
    #agus = Node(None,State(12),Action(None,12,0),0)
    #print(agus.state.state)
    #problem.search(DepthFirst())
    #######
    #problem = Problem('paseo_simón_abril_albacete_250_1.json')
    #print(';'.join(map(str,problem.search(BreadthFirst()))))
    #
    problem = Problem('paseo_simón_abril_albacete_250_1.json')
    print(';'.join(map(str,problem.search(DepthFirst()))))
main()