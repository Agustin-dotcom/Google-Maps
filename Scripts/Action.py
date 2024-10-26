class Action: 
    def __init__(self,origin,destination,cost):
        self.origin = origin
        self.destination = destination
        self.cost = cost
    def __str__(self):
       return(
           f' {self.origin} → {self.destination} ({self.cost})'
       )