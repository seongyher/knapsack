import random

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
    
    def __init__(self, pool_size, trove, pool):
        self.pool_size = pool_size
        self.trove = trove
        self.pool = pool
        self.pool_total = self.tally() # update for class each generation
        self.generate_sacks()
        self.sack_size = 4
        #self.sack_size = len(self.pool[sack_0][0])
        #should probably be run asynchronously somehow?
        
        #self.mutation_rate = self.pool_size // 10 * random.randrange(self.pool_size)
        #self.crossover_rate = self.pool_size // 5 * random.randrange(self.pool_size)
        
        #for i in range(self.mutation_rate):
            #self.mutate()
        
        #for j in range(self.crossover_rate):
            #self.crossover()
    
    def tally(self):
        """
        Give the mean 
        """
        
        tally_total = 0
        for i in self.pool:
            tally_total += i[1]
        return tally_total
    
    
    
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
        
    def solve(self):
        history = [-1, -1, -1]
    
        self.tally()
        new_total = self.pool_total
    
        history[0] = history[1]
        history[1] = history[2]
        history[2] = new_total
        # check if pool has changed in value over the 
        # last 3 generations
    
        self.mutate()
        self.tally()
        print(f"Mutation: The new total value is {new_total}.")
        self.crossover()
        self.tally()
        print(f"Crossover: The new total value is {new_total}.")
    
        while history[2] != -1:
            if history[0] == history[1] and history[1] == history[2]:
                return self.pool        


# (weight, size, value)
trove_1 = [(1,1,1), (3,1,2), (4,2,0), (2,6,5), (1,4,1), (4,6,1), (7,10,6), (8,8,6), (7,4,6), (5,5,5)]
trove_2 = [(2,1,2), (1,3,2), (5,1,7), (6,3,8), (9,4,6), (7,7,7), (1,1,1)]

ex_cohort = {
    "sack_0": [(1,1,1), (3,1,2), (4,2,0), (2,6,5)],
    "sack_1": [(2,6,5), (1,4,1), (7,10,6), (8,8,6)],
    "sack_2": [(3,1,2), (1,4,1), (2,6,5), (7,10,6)],
    "sack_3": [(2,6,5), (1,4,1), (4,6,1), (8,8,6)]
}
pool_1 = GenePool(4, trove_1, ex_cohort)