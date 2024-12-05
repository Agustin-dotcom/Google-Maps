import unittest
import sys
sys.path.append('C:\\googleMapsVS\\Google-Maps\\Lab2\\Scripts')
from Search import Search
from Problem import Problem
class Search_test(unittest.TestCase): 
    def test_is_already_in_memory_false(self):
        #sys.path.append('')
        problem = Problem('C:\\googleMapsVS\\Google-Maps\\Lab2\\calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json')
        self.expected_result = Search(problem)
        self.assertEqual(self.expected_result.is_already_in_memory(1736146191,435465434),False)
    def test_is_already_in_memory_true(self):
        problem = Problem('C:\\googleMapsVS\\Google-Maps\\Lab2\\calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json')
        self.expected_result = Search(problem)
        self.expected_result.problem.dictionary.get('candidates').get(1736146191)['time']={1736146191:{'identifier':435465434,'A*':23.4}}
        self.assertEqual(self.expected_result.is_already_in_memory(1736146191,435465434),True)
    def test_
if __name__ == '__main__':
    unittest.main()