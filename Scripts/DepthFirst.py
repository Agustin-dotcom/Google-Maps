from Scripts.Search import Search
class DepthFirst(Search): # LIFO queue
    def extract(self):
        if len(self.openDS)<1:
            raise Exception("No puedes extraer algo que no existe")
        return self.openDS.pop() # lo del return tiene sentido yo creo