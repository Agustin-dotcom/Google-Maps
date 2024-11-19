import json
class Problem_2:
    def __init__(self,file_name):
        with (file_name,'r') as file:
            self.dictionary = json.load(file)
        self.dictionary['intersections'] = {inter['identifier']: inter for inter in self.dictionary.get('intersections')}# O(m)
        self.dictionary['maxSpeedOfAllSpeeds'] = float('-inf') # definiendo la maxima velocida a menos infinito
        # Add the 'whereto' attribute to each intersection
        for inter in self.dictionary['intersections'].values():# O(m)
            inter['whereto'] = []

        # Populate the 'whereto' attribute based on the segments
        for segment in self.dictionary.get('segments'):# O(n)
            origin = segment['origin']#O(1)
            destination = segment['destination'] #O(1)
            distance = segment['distance'] #O(1)
            speed_kmh = segment['speed'] # O(1)

            # Convert speed from km/h to m/s
            speed_ms = speed_kmh * (1000 / 3600)
            #self.dictionary['mostRepeatedSpeed'].append(speed_ms)
            # Si tenemos una velocidad mayor a la predeterminada, la cogemos
            if(speed_ms > self.dictionary.get('maxSpeedOfAllSpeeds')):#O(1)
                self.dictionary['maxSpeedOfAllSpeeds'] = speed_ms
    
            # Calculate the cost
            cost = distance / speed_ms
    
            # Add the destination and cost to the 'whereto' attribute of the origin intersection
            #if origin in self.dictionary.get('intersections'): # O(1)
            self.dictionary.get('intersections').get(origin).get('whereto').append({'id': destination, 'cost': cost})
        for i in self.dictionary.get('intersections'):
            self.dictionary['intersections'][i]['whereto'] = sorted(self.dictionary.get('intersections').get(i).get('whereto'),key = lambda x:x['id'])