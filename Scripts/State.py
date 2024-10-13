class State:
    def __init__(self,state,longitude,latitude):
        if not isinstance(state,int):
            raise TypeError(f"Introduce an int, not a {type(state).__name__}")
        if not isinstance(longitude,int):
            raise TypeError(f"Introduce an int, not a {type(longitude).__name__}")
        if not isinstance(latitude,int):
            raise TypeError(f"Introduce an int, not a {type(latitude).__name__}")
        self.state = state
        self.longitude = longitude
        self.latitude = latitude
