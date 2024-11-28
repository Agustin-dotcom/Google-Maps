from problem import Problem
problem = Problem('calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json')
agus = RandomSearch(problem)
agus.search(20)