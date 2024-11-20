class Solution:
    def __init__(self):
        self.configuration = {candidate[0]:{"identifier":candidate[0],"population":candidate[1]} for candidate in self.dictionary.get('candidates')}
        self.configuration['number_stations'] = self.dictionary.get('number_stations')
        