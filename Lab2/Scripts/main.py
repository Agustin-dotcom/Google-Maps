
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
# population_size cannot be longer than import math math.comb(n,k) where n is the number of candidates and k the number of stations since you cannot generate more solutions than combinations possible
me_deberia_devolver_una_populacion = agus_dos.search(20000)
# for i in range(len(me_deberia_devolver_una_populacion)):
#     print(me_deberia_devolver_una_populacion[i])
print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
print("\t \t \t GENETIC ALGORITHM")
print("//////////////////////////////////////////")
import heapq
solution = heapq.heappop(me_deberia_devolver_una_populacion)[1]
for id,i in enumerate(agus_dos.problem.dictionary.get('candidates').values()):
    if  solution[id] == 0:
        continue
    print(i.get('identifier'))