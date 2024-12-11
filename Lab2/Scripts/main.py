class Main:
    DEBUG = False
    def main(self):
        import os
        import time
        os.chdir('C:\\googleMapsVS\\Google-Maps\\Lab2')
        from Problem import Problem
        from Selection import Selection
        from Replacement import Replacement 
        problem = Problem('calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json')
        from RandomSearch import RandomSearch
        import numpy as np
        import time
        # Establish seed
        #np.random.seed(42)
        
        agus = RandomSearch(problem)
        
        print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
        print("\t \t RANDOM ALGORITHM")
        print("//////////////////////////////////////////")
        start = time.perf_counter()
        solution  = agus.search(200)
        end = time.perf_counter()
        print(f'time on Random --> {end - start}')
        import heapq
        jesus = heapq.heappop(solution)
        agustin = jesus.solution
        for id,i in enumerate(agus.problem.dictionary.get('candidates').values()):
            if agustin[id] == 0:
                continue
            print(i.get('identifier'))

        from GeneticAlgorithm import GeneticAlgorithm
        agus_dos = GeneticAlgorithm(problem=problem)
        # population_size cannot be longer than import math math.comb(n,k) where n is the number of candidates and k the number of stations since you cannot generate more solutions than combinations possible
        start = time.perf_counter()
        me_deberia_devolver_una_populacion = agus_dos.search(300)
        end = time.perf_counter()
        print(f'time on Genetic --> {end - start}')
        # for i in range(len(me_deberia_devolver_una_populacion)):
        #     print(me_deberia_devolver_una_populacion[i])
        print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
        print("\t \t GENETIC ALGORITHM")
        print("//////////////////////////////////////////")
        import heapq
        solution = me_deberia_devolver_una_populacion[0]
        for id,i in enumerate(agus_dos.problem.dictionary.get('candidates').values()):
            if  solution.solution[id] == 0:
                continue
            print(i.get('identifier'))