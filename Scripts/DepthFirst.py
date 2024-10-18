from collections import deque
from Search import Search
class DepthFirst(Search): # LIFO queue
    def extract(self):
        #if len(self.openDS)<1:
        #    raise Exception("No puedes extraer algo que no existe")
        temp = deque(self.openDS)
        self.openDS = []
        while len(temp)!=0:
            self.openDS.append(temp.pop())
        return self.openDS.pop() # lo del return tiene sentido yo creo