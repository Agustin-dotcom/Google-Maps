
import os

os.chdir('C:\\googleMapsVS\\Google-Maps\\Lab2')
from Problem import Problem
problem = Problem('calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json')
from RandomSearch import RandomSearch
agus = RandomSearch(problem)
agus.search(20)