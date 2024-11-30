
import os

os.chdir('C:\\googleMapsVS\\Google-Maps\\Lab2')
from Problem import Problem
problem = Problem('calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json')
# from RandomSearch import RandomSearch
# agus = RandomSearch(problem)
# solution  = agus.search(2)
# for id,i in enumerate(agus.problem.dictionary.get('candidates').values()):
#     if solution[id] == 0:
#         continue
#     print(i.get('identifier'))

from GeneticAlgorithm import GeneticAlgorithm
agus_dos = GeneticAlgorithm(problem=problem)
me_deberia_devolver_una_populacion = agus_dos.search(20)
# for i in range(len(me_deberia_devolver_una_populacion)):
#     print(me_deberia_devolver_una_populacion[i])
for id,i in enumerate(agus_dos.problem.dictionary.get('candidates').values()):
    if me_deberia_devolver_una_populacion[id] == 0:
        continue
    print(i.get('identifier'))