from Scripts.Search import Search
class BreadthFirst(Search):# FIFO queue    
    def extract(self):
        if len(self.openDS)<1:
            raise Exception("No puedes extraer algo que no existe")    
        return self.openDS.popleft() # extrae por la izquierda (el primero en llegar)