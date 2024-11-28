from search import Search
class GeneticAlgorithm(Search):
    def search(self):
        #Lesson 8 Slide 18
        p = self.generate_population() # create candidate solutions (individuals)
        self.evaluate(p) # obtains  their score
        while(stop_condition==false):
            p_ = self.select_population(p) # Selects some individuals by score
            self.crossover(p_) #crosses pairs of selected individuals
            self.mutation(p_) # mutates the crossed individuals
            self.evaluate(p_) # obtains the score of the new individuals
            p = self.combine(p,p_) # forms the new generation
            