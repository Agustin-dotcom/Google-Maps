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
    #problem.search(DepthFirst())
    #######
    #problem = Problem('paseo_simón_abril_albacete_250_1.json')
    #print(';'.join(map(str,problem.search(BreadthFirst()))))
    #
    #problem = Problem('paseo_simón_abril_albacete_250_1.json')
    #print(';'.join(map(str,problem.search(DepthFirst()))))
    directorio = 'C:\googleMaps\Google-Maps\Scripts\problemas'

    # Obtiene la lista de archivos y carpetas en el directorio
    archivos = os.listdir(directorio)

    # Filtra solo los archivos (opcional)
    solo_archivos = [f for f in archivos if os.path.isfile(os.path.join(directorio, f))]
    #print(solo_archivos[0])
    # Imprime la lista de archivos
    problema = Problem(os.path.join(directorio,solo_archivos[0]))
    print(';'.join(map(str,problema.search(DepthFirst()))))
main()