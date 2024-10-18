import time
import os
from Problem import Problem
from BreadthFirst import BreadthFirst
from DepthFirst import DepthFirst
from collections import deque
from BestFirst import BestFirst
from AStar import AStar
from Search import Search

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
    #os.curdir()
    
    directorio = "C:\\googleMapsVS\\Google-Maps\\problems\\huge"
    archivos = os.listdir(directorio)
    #print(archivos)
    print(f"#################################################")
    print(f"#                    COMENZAMOS                 #")
    print(f"#################################################")

    for i in archivos:
        os.chdir(directorio)
        problem = Problem('calle_del_virrey_morcillo_albacete_2000_4.json')
        #print(f"#################################################")
        #print(f"#            DEPTH FIRST SEARCH                 #")
        #print(f"#################################################")
        # print(f"#                       {i}                     #")
        # print(f"#################################################")
        # print(';'.join(map(str,problem.search(DepthFirst()))))
        # print(f"#################################################")
        # print(f"#            BREADTH FIRST SEARCH                 #")
        # print(f"#################################################")
        # print(f"#                       {i}                     #")
        # print(f"#################################################")
        # print(';'.join(map(str,problem.search(BreadthFirst()))))
        print(f"#################################################")
        print(f"#            BEST FIRST SEARCH                  #")
        print(f"#################################################")
        print(f"#                       {i}                     #")
        print(f"#################################################")
        start = time.time()
        print(','.join(map(str,problem.search(BestFirst(problem)))))
        end = time.time()
        print(f'\n Execution time --> {end-start}')
        print(f"#################################################")
        print(f"#                       A*                      #")
        print(f"#################################################")
        print(f"#                       {i}                     #")
        print(f"#################################################")
        start = time.time()
        print(','.join(map(str,problem.search(AStar(problem)))))
        end = time.time()
        print(f'\n Execution time --> {end-start}')
    #problem.search(DepthFirst())
    #######
    #problem = Problem('paseo_simón_abril_albacete_250_1.json')
    #print(';'.join(map(str,problem.search(BreadthFirst()))))
    #os.chdir(directorio)
    #problem = Problem('paseo_simoÌn_abril_250_0.json')
    #print(';'.join(map(str,problem.search(DepthFirst()))))
    # Obtiene el directorio actual donde está ejecutándose el script
    # o pide al usuario que lo proporcione
    
    #C:\googleMapsVS\Google-Maps\Scripts\problemas\
    #problema = Problem("calle_mariÌa_mariÌn_500_0.json")
        
    # Ejecuta la búsqueda y muestra los resultados
    #print(';'.join(map(str, problem.search(DepthFirst()))))
    #print(';'.join(map(str, problema.search(BreadthFirst()))))
    #problem = Problem('alabacete_simo_abril')
    #search = Search(problem)
    #problem.search(search)
    

    
main()