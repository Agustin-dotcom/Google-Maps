from AStarGeodesicWithMostRepeatedSpeed import AStarGeodesicWithMostRepeatedSpeed
from AStarAssumingOneHundredAndTwentyKilometersPerHour import AStarAssumingOneHundredAndTwentyKilometersPerHour
from AStarOptimisticButRealistic import AStarOptimisticButRealistic
import sqlite3
import time
import os
from Problem import Problem
from BreadthFirst import BreadthFirst
from DepthFirst import DepthFirst
from BestFirst import BestFirst
from AStar import AStar
class Main:
    def main(self):
        __file__ = "resultados_programa.db"
        BASE_DIR = "C:\\googleMapsVS\\Google-Maps\\" #TODO: CHANGE PATH
        db_path = os.path.join(BASE_DIR, "resultados_programa.db")
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
        for j in ['huge','large','medium','small']:
            directorio = "C:\\Users\\Agus\\Downloads\\SUBMISSION\\problems\\"+j #TODO: CHANGE PATH
            archivos = os.listdir(directorio)
            print(f"#################################################")
            print(f"#                    COMENZAMOS                 #")
            print(f"#################################################")

            for i in archivos:
                os.chdir(directorio)
                problem = Problem(i)
                start = time.perf_counter()
                busqueda = AStar(problem)
                print(f"#################################################")
                print(f"#                       {busqueda.__class__.__name__}                      #")
                print(f"#################################################")
                print(f"#                       {i}                     #")
                print(f"#################################################")
                result = problem.search(busqueda)
                end = time.perf_counter()
                print(f'Generated nodes: {problem.nodesGenerated}\n')
                print(f'Expanded nodes: {problem.expandedNodes}\n')
                print(f'Execution time: {self.formatear_segundos(end-start)}\n')
                print(f'Solution length: {problem.depth}\n')
                print(f'Solution cost: {self.formatear_segundos(problem.totalCost)}\n')
                print(f'Solution: [')
                print(','.join(map(str,result)))
                print(f']')
                self.guardar_en_base_de_datos(i,problem,end-start,j,busqueda.__class__.__name__)
                ############################################################################
                os.chdir(directorio)
                problem = Problem(i)
                start = time.perf_counter()
                busqueda = BreadthFirst(problem)
                print(f"#################################################")
                print(f"#                       {busqueda.__class__.__name__}                      #")
                print(f"#################################################")
                print(f"#                       {i}                     #")
                print(f"#################################################")
                result = problem.search(busqueda)
                end = time.perf_counter()
                print(f'Generated nodes: {problem.nodesGenerated}\n')
                print(f'Expanded nodes: {problem.expandedNodes}\n')
                print(f'Execution time: {self.formatear_segundos(end-start)}\n')
                print(f'Solution length: {problem.depth}\n')
                print(f'Solution cost: {self.formatear_segundos(problem.totalCost)}\n')
                print(f'Solution: [')
                print(','.join(map(str,result)))
                print(f']')
                self.guardar_en_base_de_datos(i,problem,end-start,j,busqueda.__class__.__name__)
                ############################################################################
                os.chdir(directorio)
                problem = Problem(i)
                start = time.perf_counter()
                busqueda = DepthFirst(problem)
                print(f"#################################################")
                print(f"#                       {busqueda.__class__.__name__}                      #")
                print(f"#################################################")
                print(f"#                       {i}                     #")
                print(f"#################################################")
                result = problem.search(busqueda)
                end = time.perf_counter()
                print(f'Generated nodes: {problem.nodesGenerated}\n')
                print(f'Expanded nodes: {problem.expandedNodes}\n')
                print(f'Execution time: {self.formatear_segundos(end-start)}\n')
                print(f'Solution length: {problem.depth}\n')
                print(f'Solution cost: {self.formatear_segundos(problem.totalCost)}\n')
                print(f'Solution: [')
                print(','.join(map(str,result)))
                print(f']')
                self.guardar_en_base_de_datos(i,problem,end-start,j,busqueda.__class__.__name__)
                #############################################################################
                os.chdir(directorio)
                problem = Problem(i)
                start = time.perf_counter()
                busqueda = BestFirst(problem)
                print(f"#################################################")
                print(f"#                       {busqueda.__class__.__name__}                      #")
                print(f"#################################################")
                print(f"#                       {i}                     #")
                print(f"#################################################")
                result = problem.search(busqueda)
                end = time.perf_counter()
                print(f'Generated nodes: {problem.nodesGenerated}\n')
                print(f'Expanded nodes: {problem.expandedNodes}\n')
                print(f'Execution time: {self.formatear_segundos(end-start)}\n')
                print(f'Solution length: {problem.depth}\n')
                print(f'Solution cost: {self.formatear_segundos(problem.totalCost)}\n')
                print(f'Solution: [')
                print(','.join(map(str,result)))
                print(f']')
                self.guardar_en_base_de_datos(i,problem,end-start,j,busqueda.__class__.__name__)
                # Ctrl + / para descomentar <--
                #############################################################################
                os.chdir(directorio)
                problem = Problem(i)
                start = time.perf_counter()
                busqueda = AStarOptimisticButRealistic(problem)
                print(f"#################################################")
                print(f"#                       {busqueda.__class__.__name__}                      #")
                print(f"#################################################")
                print(f"#                       {i}                     #")
                print(f"#################################################")
                result = problem.search(busqueda)
                end = time.perf_counter()
                print(f'Generated nodes: {problem.nodesGenerated}\n')
                print(f'Expanded nodes: {problem.expandedNodes}\n')
                print(f'Execution time: {self.formatear_segundos(end-start)}\n')
                print(f'Solution length: {problem.depth}\n')
                print(f'Solution cost: {self.formatear_segundos(problem.totalCost)}\n')
                print(f'Solution: [')
                print(','.join(map(str,result)))
                print(f']')
                self.guardar_en_base_de_datos(i,problem,end-start,j,busqueda.__class__.__name__)
                #############################################################################
                os.chdir(directorio)
                problem = Problem(i)
                start = time.perf_counter()
                busqueda = AStarAssumingOneHundredAndTwentyKilometersPerHour(problem)
                print(f"#################################################")
                print(f"#                       {busqueda.__class__.__name__}                      #")
                print(f"#################################################")
                print(f"#                       {i}                     #")
                print(f"#################################################")
                result = problem.search(busqueda)
                end = time.perf_counter()
                print(f'Generated nodes: {problem.nodesGenerated}\n')
                print(f'Expanded nodes: {problem.expandedNodes}\n')
                print(f'Execution time: {self.formatear_segundos(end-start)}\n')
                print(f'Solution length: {problem.depth}\n')
                print(f'Solution cost: {self.formatear_segundos(problem.totalCost)}\n')
                print(f'Solution: [')
                print(','.join(map(str,result)))
                print(f']')
                self.guardar_en_base_de_datos(i,problem,end-start,j,busqueda.__class__.__name__)
                #############################################################################
                os.chdir(directorio)
                problem = Problem(i)
                start = time.perf_counter()
                busqueda = AStarGeodesicWithMostRepeatedSpeed(problem)
                print(f"#################################################")
                print(f"#                       {busqueda.__class__.__name__}                      #")
                print(f"#################################################")
                print(f"#                       {i}                     #")
                print(f"#################################################")
                result = problem.search(busqueda)
                end = time.perf_counter()
                print(f'Generated nodes: {problem.nodesGenerated}\n')
                print(f'Expanded nodes: {problem.expandedNodes}\n')
                print(f'Execution time: {self.formatear_segundos(end-start)}\n')
                print(f'Solution length: {problem.depth}\n')
                print(f'Solution cost: {self.formatear_segundos(problem.totalCost)}\n')
                print(f'Solution: [')
                print(','.join(map(str,result)))
                print(f']')
                self.guardar_en_base_de_datos(i,problem,end-start,j,busqueda.__class__.__name__)
    def formatear_segundos(self,segundos):
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segundos_restantes = segundos % 60
        return f"{horas:02}:{minutos:02}:{segundos_restantes:02}"
    def guardar_en_base_de_datos(self,nombre_problema,problem,tiempo_ejecucion,tipo_problema,algoritmo):
        os.chdir('C:\\googleMapsVS\\Google-Maps')
        __file__ = "resultados_programa.db"
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "resultados_programa.db")
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