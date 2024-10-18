class State:
    def __init__(self,state,longitude,latitude):
        #if not isinstance(state,int):
        #    raise TypeError(f"Introduce an int, not a {type(state).__name__}")
        #if not isinstance(longitude,float):
        #    raise TypeError(f"Introduce a float, not a {type(longitude).__name__}")
        #if not isinstance(latitude,float):
        #    raise TypeError(f"Introduce a float, not a {type(latitude).__name__}")
        self.state = state
        self.longitude = longitude
        self.latitude = latitude
    def __lt__(self,obj):
        return (self.state,self.longitude,self.latitude) < (obj.state,obj.longitude,obj.latitude)
