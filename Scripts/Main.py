import sqlite3
import time
import os
from Problem import Problem
from BreadthFirst import BreadthFirst
from DepthFirst import DepthFirst
from collections import deque
from BestFirst import BestFirst
from AStar import AStar
from Search import Search
class Main:
    def main(self):
        os.chdir('C:\\googleMapsVS\\Google-Maps')
        __file__ = "resultados_programa.db"
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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
                    tipo_problema TEXT,
                    nodos_explorados INTEGER,
                    nodos_generados INTEGER,
                    tiempo_ejecucion REAL,
                    profundidad_solucion INTEGER,
                    costo_solucion REAL,
                    algoritmo TEXT
                    )''')
        print("Tabla 'resultados' creada o ya existe.")

        # Guardar los cambios
        db.commit()
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
        #os.curdir()
        for j in ['huge','large','medium','small']:
            directorio = "C:\\googleMapsVS\\Google-Maps\\problems\\"+j
            archivos = os.listdir(directorio)
            #print(archivos)
            #print(f"#################################################")
            #print(f"#                    COMENZAMOS                 #")
            #print(f"#################################################")

            for i in archivos:
                os.chdir(directorio)
                problem = Problem(i)
                #print(f"#################################################")
                #print(f"#            DEPTH FIRST SEARCH                 #")
                #print(f"#################################################")
                #print(f"#                       {i}                     #")
                #print(f"#################################################")
                start = time.time()
                busqueda = DepthFirst(problem)
                problem.search(busqueda)
                #print(';'.join(map(str,problem.search(busqueda))))
                end = time.time()
                self.guardar_en_base_de_datos(problem,end-start,j,busqueda.__class__.__name__)
                #print(f'\n Execution time --> {end-start}')
                #print(f"#################################################")
                #print(f"#            BREADTH FIRST SEARCH                 #")
                #print(f"#################################################")
                #print(f"#                       {i}                     #")
                #print(f"#################################################")
                start = time.time()
                busqueda = BreadthFirst(problem)
                problem.search(busqueda)
                #print(';'.join(map(str,problem.search(busqueda))))
                end = time.time()
                self.guardar_en_base_de_datos(problem,end-start,j,busqueda.__class__.__name__)
                #print(f'\n Execution time --> {end-start}')
                #print(f"#################################################")
                #print(f"#            BEST FIRST SEARCH                  #")
                #print(f"#################################################")
                #print(f"#                       {i}                     #")
                #print(f"#################################################")
                start = time.time()
                busqueda = BestFirst(problem)
                problem.search(busqueda)
                #print(','.join(map(str,problem.search(busqueda))))
                end = time.time()
                self.guardar_en_base_de_datos(problem,end-start,j,busqueda.__class__.__name__)
                #print(f'\n Execution time --> {end-start}')
                #print(f"#################################################")
                #print(f"#                       A*                      #")
                #print(f"#################################################")
                #print(f"#                       {i}                     #")
                #print(f"#################################################")
                start = time.time()
                busqueda = AStar(problem)
                problem.search(busqueda)
                #print(','.join(map(str,problem.search(busqueda))))
                self.guardar_en_base_de_datos(problem,end-start,j,busqueda.__class__.__name__)
                end = time.time()
                print(f'\n Execution time --> {end-start}')
            #problem.search(DepthFirst())
            #######
            #problem = Problem('paseo_simón_abril_albacete_250_1.json')
            #print(';'.join(map(str,problem.search(BreadthFirst()))))
            #os.chdir(directorio)
            #problem = Problem('paseo_simoÌn_abril_250_0.json')
            #print(';'.join(map(str,problem.search(DepthFirst()))))
            # Obtiene el directorio actual donde está ejecutándose el script
            # o pide al usuario que lo proporcione
            
            #C:\googleMapsVS\Google-Maps\Scripts\problemas\
            #problema = Problem("calle_mariÌa_mariÌn_500_0.json")
                
            # Ejecuta la búsqueda y muestra los resultados
            #print(';'.join(map(str, problem.search(DepthFirst()))))
            #print(';'.join(map(str, problema.search(BreadthFirst()))))
            #problem = Problem('alabacete_simo_abril')
            #search = Search(problem)
            #problem.search(search)`
    def guardar_en_base_de_datos(self,problem,tiempo_ejecucion,tipo_problema,algoritmo):
        os.chdir('C:\\googleMapsVS\\Google-Maps')
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "resultados_programa.db")
        with sqlite3.connect(db_path) as db:
            c = db.cursor()
        c.execute('''INSERT INTO resultados 
                         (tipo_problema, nodos_explorados, nodos_generados, tiempo_ejecucion, 
                         profundidad_solucion, costo_solucion, algoritmo) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                     (tipo_problema, problem.exploredNodes, problem.nodesGenerated, 
                     tiempo_ejecucion, problem.depth, 
                     problem.totalCost, algoritmo))
        db.commit()
        db.close()