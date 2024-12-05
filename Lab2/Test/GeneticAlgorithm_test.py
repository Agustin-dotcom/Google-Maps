import unittest
import sys
sys.path.append('C:\\googleMapsVS\\Google-Maps\\Lab2\\Scripts')
#from Search import Search
from GeneticAlgorithm import GeneticAlgorithm
from Problem import Problem
class GeneticAlgorithm_test(unittest.TestCase): 
    def test_proportion_based_selection(self):
        #sys.path.append('')
        problem = Problem('C:\\googleMapsVS\\Google-Maps\\Lab2\\calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json')
        self.actual_result = GeneticAlgorithm(problem)
        self.assertEqual(self.actual_result.proportion_based_selection([]),False)
if __name__ == '__main__':
    unittest.main()