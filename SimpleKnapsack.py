import random

class Trove:
    """
    One treasure trove with random objects.
    """
    def __init__(self, treasure_count):
        self.all_treasures = []
        self.max_value = 99
        self.max_weight = 99
        for i in range(treasure_count):
            self.all_treasures.append((random.randrange(self.max_value+1), random.randrange(self.max_weight+1)))
            # append a tuple in form of (value, weight) to self.treasures

class Knapsack_Pool:
    """
    One knapsack with random members from the trove.
    """
    
    def __init__(self, trove, pool_size):
        self.pool = []
        self.trove = trove
        self.weight_limit = 50 * pool_size
        for i in range(pool_size):
            self.spawn()

    def spawn(self):
        sack = []
        total_value  = 0
        total_weight = 0
        for i in range(len(self.trove.all_treasures)):
            sack.append(random.randrange(2))
            # binary for inclusion/exclusion in sack
        for j in sack:
            total_value += self.trove.all_treasures[j][0]
            total_weight += self.trove.all_treasures[j][1]
        if total_weight > self.weight_limit:
            total_value = 0
        self.pool.append((total_value, sack))

    def select(self):
        """
        Kills off the bottom 10% of the lowest value sacks
        """
        self.pool.sort() # from smallest value to largest
        self.pool = self.pool[len(self.pool)/10:] # slice off the first 10%

    def cross(self):
        """
        take two random members of pool, creating a third member that is a
        random combination of the two 'parent' knapsacks.
        """
        parents = []
        offspring = []
        for i in range(2):
            parents.append(self.pool[random.randrange(len(self.pool))])
            # assign two parents to list of parents
        for j in parents[0]:
            offspring.append(parents[random.randrange(2)][j])
            # randomly pick between two parents for each 'base' in gene
        self.pool.append(offspring)
    
    def mutate(self):
        """
        modify one random member in place, replacing it with a similar but
        different knapsack
        """
        mutator = self.pool[random.randrange(len(self.pool))]
        mutation_rate = 10
        mutation_threshold = 7
        for i in range(len(mutator)):
            mutation_score = random.randrange(mutation_rate)
            if mutation_score <= mutation_threshold:
                mutator[i] = random.randrange(2)
            
    def show_sacks(self):
        """
        Print all sacks
        """
        for i in self.pool:
            print(i)
        
    # 2023-06-28 next steps:
    # 1. mutate and select (on a loop)
    # 2. know when to stop mutating and selecting (solution found)
    # step 2 should be based on how much change there was between 
    # the previous several generations, or perhaps by looking
    # at how many of the top n members are the same
    # another feature I could add is to always breed the top 2
    # members or always include the top 1 so that mating is assortative
    
# TEST CASES
test_trove = Trove(10)
test_sack = Knapsack_Pool(test_trove, 20)