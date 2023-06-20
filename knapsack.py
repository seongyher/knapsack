import random

# (weight, size, value)
trove_1 = [(1,1,1), (3,1,2), (4,2,0), (2,6,5), (1,4,1), (4,6,1), (7,10,6), (8,8,6), (7,4,6), (5,5,5)]
trove_2 = [(2,1,2), (1,3,2), (5,1,7), (6,3,8), (9,4,6), (7,7,7), (1,1,1)]

class Knapsack:
    """
    A knapsack with limited space.
    Randomly fill each time a new instance is created.
    """
    
    def __init__(self, trove):
        self.space = 4
        self.weight_limit = 15
        self.size_limit = 15
        self.total_weight = 0
        self.total_size = 0
        self.total_value = 0
        self.trove_copy = trove.copy()
        self.options = []

        self.stash(trove)
        self.calculate()
    
    def stash(self, trove):
        for i in range(self.space):
            rand_treasure = random.randrange(len(self.trove_copy))
            self.options.append(self.trove_copy[rand_treasure])
            self.trove_copy.remove(self.trove_copy[rand_treasure])
            # this part is crucial since I don't want to add the same object twice
    
    def calculate(self):
        for i in self.options:
            self.total_weight += i[0]
            self.total_size += i[1]
            self.total_value += i[2]
        if self.total_size > self.size_limit:
            self.total_value = 0
        elif self.total_weight > self.weight_limit:
            self.total_value = 0
    
    
class GenePool:
    """
    Generate a gene pool of n knapsacks, which are stored in a dict
    with var names as keys and total value as the values.
    """
    
    def __init__(self, pool_size, trove):
        self.pool = {}
        self.pool_size = pool_size
        self.trove = trove
        
        self.generate_sacks()
        self.sack_size = 4
        #self.sack_size = len(self.pool[sack_0][0])
        #should probably be run asynchronously somehow?
        
        #self.mutation_rate = self.pool_size // 10 * random.randrange(self.pool_size)
        #self.crossover_rate = self.pool_size // 5 * random.randrange(self.pool_size)
        
        for i in range(self.mutation_rate):
            self.mutate()
        
        for j in range(self.crossover_rate):
            self.crossover()
    
    def generate_sacks(self):
        for i in range(self.pool_size):
            current_sack = Knapsack(self.trove)
            self.pool[f"sack_{i}"] = (current_sack.options, current_sack.total_value)

    def crossover(self):
        parent_1 = random.randrange(self.pool_size)
        parent_2 = random.randrange(self.pool_size) # ignore that this causes self-pollination for now
        cross_1 = random.randrange(self.sack_size)
        cross_2 = random.randrange(self.sack_size)
        self.pool[f"sack_{parent_1}"][0][cross_1], self.pool[f"sack_{parent_2}"][0][cross_2] = self.pool[f"sack_{parent_2}"][0][cross_2], self.pool[f"sack_{parent_1}"][0][cross_1]
    
    def mutate(self):
        temp_options = Knapsack(self.trove)
        mutating_sack = random.randrange(self.pool_size)
        mutation_point = random.randrange(self.sack_size)
        self.pool[mutating_sack][0][mutation_point] = temp_options.options[mutation_point]
        #But how do I check for duplicates (i.e. doubling up on the same option)?
        #Would it be easier if knapsack was not a separate class?
        #Or perhaps a list of options should be a list of unique indices?

# 2023-06-18
# next step: create an algorithm for how the mutations happen
# next step after that is probably comparing different algorithms
# based on performance
# the step after that is probably selecting between different
# algorithms by mutating and crossing over the algorithms themselves

class Strategy:
    """
    Evolutionary strategy including mutation site and rate, crossover, etc.
    Expressed as a class attribute expressing the algorithm (?).
    A database of strategies and the score for each strategy stored as a class
    attribute (cf. instance attribute) that gets updated with the outcomes.
    """
    
    def __init__(self):
        self.strat_dict = {}
        
    def gen_tactic(self):
        """
        Instructions for how to evolve the knapsacks
        """
        # 2023-06-19
        # It's the knapsacks that are being selected, and it's the makeup of the
        # options in the knapsacks that are evolving.
        # what am I evolving for? 
        # I guess the fewer "cycles" a strategy takes to converge on a solution,
        # the better it is. And the higher the value of the knapsacks in the
        # population, the closer it is to the solution. And if it stops changing
        # after several cycles, then it must have hit a local maximum (could be
        # also the global maximum). Do I assume that I don't know the maximum
        # possible value of a population? I think I would want to generate a
        # random trove in order to test the strategies. 
        # 

        
    def select(self):
        """
        Compare the strategies in the dictionary and return the best one
        """
    def diversity(self):
        """
        Calculate the diversity of strategies based on a crude methodology,
        by comparing the number of letters between the algorithms
        """
        

# p = GenePool()
# s = Strategy()
# s.evolve(p) -> modify the set of Knapsack instances within the gene pool
# 
#genes_1 = GenePool(200, trove_1)
