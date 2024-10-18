class Action: # Maybe we can receive a state and return a new one 
    def __init__(self,origin,destination,cost):
        #if not isinstance(origin,(int,type(None))):
        #    raise TypeError(f"Introduce an int, not a {type(origin).__name__}")
        #if not isinstance(destination,int):
        #    raise TypeError(f"Introduce an int, not a {type(destination).__name__}")
        #if not isinstance(cost,(int,float)):
        #    raise TypeError(f"Introduce an int or a float, not a {type(cost).__name__}")
        self.origin = origin
        self.destination = destination
        self.cost = cost
    def __str__(self):
        return(
            f' {self.origin} → {self.destination} ({self.cost})'
        )