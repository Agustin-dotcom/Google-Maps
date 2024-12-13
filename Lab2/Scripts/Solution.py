class Solution:
    momento = 0
    def __init__(self,score,solution):
        self.score = score
        self.solution = solution
        self.momento = Solution.momento
        Solution.momento += 1
    def __lt__(self,obj):
        if self.score == obj.score:
            return self.momento < obj.momento
        return self.score < obj.score