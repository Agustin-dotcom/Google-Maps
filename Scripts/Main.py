import os
from Problem import Problem
from BreadthFirst import BreadthFirst
from DepthFirst import DepthFirst
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
    #os.curdir()
    directorio = "C:\\googleMapsVS\\Google-Maps\\problems\\small"
    archivos = os.listdir(directorio)
    print(archivos)

    for i in archivos:
        os.chdir(directorio)
        problem = Problem(i)
        print(f"#################################################")
        print(f"#            DEPTH FIRST SEARCH                 #")
        print(f"#################################################")
        print(f"#            {i}                 #")
        print(f"#################################################")
        print(';'.join(map(str,problem.search(DepthFirst()))))
        print(f"#################################################")
        print(f"#            BREADTH FIRST SEARCH                 #")
        print(f"#################################################")
        print(f"#            {i}                 #")
        print(f"#################################################")
        print(';'.join(map(str,problem.search(BreadthFirst()))))
    #problem.search(DepthFirst())
    #######
    #problem = Problem('paseo_simón_abril_albacete_250_1.json')
    #print(';'.join(map(str,problem.search(BreadthFirst()))))
    #
    #problem = Problem('paseo_simón_abril_albacete_250_1.json')
    #print(';'.join(map(str,problem.search(DepthFirst()))))
    # Obtiene el directorio actual donde está ejecutándose el script
    # o pide al usuario que lo proporcione
    
    #C:\googleMapsVS\Google-Maps\Scripts\problemas\
    #problema = Problem("calle_mariÌa_mariÌn_500_0.json")
        
    # Ejecuta la búsqueda y muestra los resultados
    #print(';'.join(map(str, problema.search(DepthFirst()))))
    #print(';'.join(map(str, problema.search(BreadthFirst()))))
    
main()