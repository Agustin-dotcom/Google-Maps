from Search import Search
class BreadthFirst(Search):# FIFO queue    
    def extract(self): # O(1)
        return self.openDS.popleft() # extrae por la izquierda (el primero en llegar)