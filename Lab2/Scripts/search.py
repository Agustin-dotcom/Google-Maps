from abc import ABC,abstractmethod
class Search(ABC):
    @abstractmethod
    def __init__():
        pass
    @abstractmethod
    def insert():
        pass
    @abstractmethod
    def extract():
        pass
    @abstractmethod
    def evaluation():
        pass
    def search(self,search_param): # O(n)
        """:param search_param: strategy to use
        
        :returns: empty list of list of actions"""
        search_param.insert(self.root)
        while len(search_param.openDS)!=0:    
            node = search_param.extract() # O(1) 
            self.exploredNodes +=1
            if node.state.state not in self.explored:
                if(self.testGoal(node)): 
                    self.depth = node.depth
                    self.totalCost = node.accumulatedCost
                    return self.recoverPath(node,[],0)
                successors1 = self.expand(node) # O(n)
                if (len(successors1)>0):
                    self.expandedNodes+=1
                for  successor in successors1: # O(n)
                    search_param.insert(successor) # O(1)
                self.explored.add(node.state.state) #  node.state es el objeto y node.state.state es la variable en el objeto state
        print("Solución no encontrada y hemos recorrido todo el árbol")
        return search_param.openDS