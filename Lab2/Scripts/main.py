from Search import Search
from RandomSearch import RandomSearch
from GeneticAlgorithm import GeneticAlgorithm
from Problem import Problem
import sqlite3
import os
import heapq
import time
import time
class Main:
    DEBUG_EVALUATION = False
    DEBUG_MAIN = True
    def main(self):
        __file__ = "resultados_programa_lab2.db"
        BASE_DIR = "C:\\googleMapsVS\\Google-Maps\\Lab2\\" #TODO: CHANGE PATH
        db_path = os.path.join(BASE_DIR, "resultados_programa_lab2.db")
        with sqlite3.connect(db_path) as db:
            c = db.cursor()
        print("Base de datos creada/conectada exitosamente")
        print(os.getcwd())
        db.execute('''SELECT * FROM sqlite_master''')
        # Eliminar la tabla si ya existe
        c.execute('''DROP TABLE IF EXISTS resultados''')
        # Crear la tabla
        c.execute('''CREATE TABLE resultados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nameProblem VARCHAR(50),
                    typeOfProblem TEXT,
                    nodesGenerated INTEGER,
                    nodesExpanded INTEGER,
                    executionTime REAL,
                    formattedCostTime TEXT,
                    depthOfSolution INTEGER,
                    SolutionCost REAL,
                    algorithm TEXT
                    )''')
        print("Tabla 'resultados' creada o ya existe.")
        # Guardar los cambios
        db.commit()
        os.chdir('C:\\googleMapsVS\\Google-Maps\\Lab2')
        for j in ['medium','small']:
            directory = 'C:\\googleMapsVS\\Google-Maps\\Lab2\\sample-problems-lab2\\'+j
            files = os.listdir(directory)
            if Main.DEBUG_MAIN:
                print(j)
            for i in files:
                os.chdir(directory)
                problem = Problem(i)
                for k in [RandomSearch(problem),GeneticAlgorithm(problem)]:
                    if Main.DEBUG_MAIN:
                        print(f'num_candidates is {len(problem.dictionary.get('candidates'))}, to select {problem.dictionary.get('number_stations')}')
                    start = time.perf_counter()
                    if Main.DEBUG_MAIN:
                        print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
                        print(f"\t \t {k.__class__.__name__}") 
                        print("//////////////////////////////////////////")
                    search = k
                    solution = search.search()
                    solution = heapq.heappop(solution)
                    end = time.perf_counter()
                    if Main.DEBUG_MAIN:
                        execution_time = self.formatear_segundos(end - start)
                        print(f'total seconds (Execution time) is : {execution_time}')
                        print(f'Best Solution : {solution.solution}')
                        print(f'fitness = {solution.score}')
                        print(f'The {problem.dictionary.get('number_stations')} stations will be located in intersections:')
                        print(solution.solution)
                        for id,i in enumerate(search.problem.dictionary.get('candidates').values()):
                            if  solution.solution[id] == 0:
                                continue
                            print(i.get('identifier'))
                        print('\n')
                        print('A_Star calls:')
                        print(f'\ttotal --> {Search.a_star_total}')
                        print(f'\treal --> {Search.a_star_real}')
                        print('Evaluated individuals:')
                        print(f'\ttotal --> ')
                        print(f'\treal --> ')
                        print('___________________________________________')
                        print('\n')
                        self.guardar_en_base_de_datos(i,problem,execution_time,j,k.__class__.__name__)
    def formatear_segundos(self,segundos):
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segundos_restantes = segundos % 60
        return f"{horas:02}:{minutos:02}:{segundos_restantes:02}"
    def guardar_en_base_de_datos(self,nombre_problema,problem,tiempo_ejecucion,tipo_problema,algoritmo):
        os.chdir("C:\\googleMapsVS\\Google-Maps\\Lab2\\")
        __file__ = "resultados_programa_lab2.db"
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "resultados_programa_lab2.db")
        with sqlite3.connect(db_path) as db:
            c = db.cursor()
        c.execute('''INSERT INTO resultados 
                         (nameProblem,
                    typeOfProblem,
                    nodesGenerated,
                    nodesExpanded,
                    executionTime,
                    formattedCostTime,
                    depthOfSolution,
                    SolutionCost,
                    algorithm) 
                         VALUES (?,?,?,?, ?, ?, ?, ?, ?)''', 
                     (nombre_problema,tipo_problema, problem.nodesGenerated,problem.expandedNodes, 
                     tiempo_ejecucion,self.formatear_segundos(problem.totalCost), problem.depth, 
                     problem.totalCost, algoritmo))
        db.commit()