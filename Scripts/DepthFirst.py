from Search import Search
class DepthFirst(Search): # LIFO queue
    def extract(self):#O(1)
        return self.openDS.pop() 