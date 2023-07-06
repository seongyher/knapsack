import random

class Trove:
    """
    One treasure trove with random objects.
    """
    def __init__(self, treasure_count):
        self.all_treasures = []
        self.max_value = 100
        self.max_weight = 20
        self.total_value = 0
        self.total_weight = 0
        for i in range(treasure_count):
            self.all_treasures.append((random.randrange(self.max_value+1), random.randrange(self.max_weight+1)))
        for j in range(treasure_count):
            self.total_value += self.all_treasures[j][0]
            self.total_weight += self.all_treasures[j][1]
            # append a tuple in form of (value, weight) to self.treasures
            
    def show_treasures(self):
        for i in self.all_treasures:
            print(i)

class Knapsack_Pool:
    """
    One knapsack with random members from the trove.
    """
    
    def __init__(self, trove, pool_size):
        self.pool = []
        self.pool_size = pool_size
        self.trove = trove
        self.weight_limit = pool_size * 10
        self.gen_minus_2 = 0 # total pool value for grandparents generation
        self.gen_minus_1 = 0 # total pool value for parents generation
        for i in range(pool_size):
            self.spawn()

    def spawn(self):
        sack = [0]
        total_value  = 0
        total_weight = 0
        for i in range(len(self.trove.all_treasures)):
            sack.append(random.randrange(2))
            # binary for inclusion/exclusion in sack
        for j in range(len(sack) - 1):
            if sack[j] == 1: # only run below weight and value gain if binary is 1
                total_value += self.trove.all_treasures[j][0]
                total_weight += self.trove.all_treasures[j][1]
        if total_weight > self.weight_limit:
            total_value = 0
        sack[0] = total_value # prepend total value as first element of list
        self.pool.append(sack)
        
    def evolve(self):
        self.gen_minus_2 = self.gen_minus_1
        self.gen_minus_1 = 0
        for i in self.pool:
            self.gen_minus_1 += i[0]/self.pool_size # idx 0 shows the total value of each sack
        # while self.gen_minus_2 < self.gen_minus_1:
        for i in range(500):
            self.mutate()
            self.mutate()
            self.mutate()
            self.assortative_cross()
            # I should probably make this random, but it's fine for now
            self.select()
            print("Evolving...")
            self.show_sacks()

    def select(self):
        """
        Kills off the bottom 10% of the lowest value sacks
        """
        self.pool.sort() # from smallest value to largest
        self.pool = self.pool[1:] # kill off lowest

    def cross(self):
        """
        take two random members of pool, creating a third member that is a
        random combination of the two 'parent' knapsacks.
        """
        parents = []
        for i in range(2):
            parents.append(self.pool[random.randrange(len(self.pool))][1:])
            # add each parent without the total value elm (idx 0)
            print("Parent added:", parents[i])
        self.mating(parents)
        
    def assortative_cross(self):
        """
        always cross two highest value pair
        """
        parents = self.pool[:-2]
        for i in range(2):
            parents[i] = parents[i][1:]
            # add each parent without the total value elm (idx 0)
            print("Parent added:", parents[i])
        self.mating(parents)
            
    def mating(self, parents):
        offspring = []
        offspring_weight = 0
        offspring_value = 0
        for j in range(len(parents[0])):
            allele = parents[random.randrange(1)][j]
            # randomly pick between two parents for each 'base' in gene
            offspring.append(allele)
            if allele == 1:
                offspring_value += self.trove.all_treasures[j][0]
                offspring_weight += self.trove.all_treasures[j][1]
        if offspring_weight <= self.weight_limit:
            offspring = [offspring_value] + offspring
        else:
            offspring = [0] + offspring
        print("Offspring added:", offspring)
        self.pool.append(offspring)
                
    
    def mutate(self):
        """
        modify one random member in place, replacing it with a similar but
        different knapsack
        """
        self.pool.sort()
        mutator = self.pool[random.randrange(len(self.pool)-5)]
        # this leaves out the top 5 sacks
        mutation_rate = 10
        mutation_threshold = 7
        mutator_new_val = 0
        mutator_new_weight = 0
        for i in range(1, len(mutator)): # skip first element (that's the value)
            mutation_score = random.randrange(mutation_rate)
            if mutation_score <= mutation_threshold:
                mutator[i] = random.randrange(2)
        for j in range(1, len(mutator)):
            if j == 1:
                mutator_new_val += self.trove.all_treasures[j][0]
                mutator_new_weight += self.trove.all_treasures[j][1]
        if mutator_new_weight > self.weight_limit:
            mutator_new_val = 0
        mutator[0] = mutator_new_val
            
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
    
    # 2023-07-04
    # Evolution is actually working now.
    # Assortative mating is working but it's still not enough for there
    # to be reliable progress. The population quickly becomes homogenous
    # too early. I can just add more mutation, but that will soon make the
    # process random again. Maybe mating should produce more than 1 offspring?
    # but what would that do in this scenario exactly?
    # 
    # I wonder why there's regression betewen generations sometimes. I guess
    # it's the mutation randomly hitting the top sacks (that is bad luck).
    # Maybe mutation should only happen as a result of mating, to the offspring?
    # 
    
    
# TEST CASES
test_trove = Trove(10)
test_sack = Knapsack_Pool(test_trove, 20)