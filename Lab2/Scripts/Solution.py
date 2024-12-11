class Solution:
    momento = 0
    def __init__(self,score,solution,momento):
        self.score = score
        self.solution = solution
        self.momento = momento
    def __lt__(self,obj):
        (self.score < obj.score) or (self.momento < obj.momento)