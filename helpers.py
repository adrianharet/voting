import itertools

def alternatives(X):
    """
        Returns a list of alternatives given iterable X 
        containing the relevant information.

        [2, 3, 1, 4] --> [1, 2, 3, 4]
        {(1, 2), (3, 4)} --> [1, 2, 3, 4]
        [[2, 1, 3, 4], [4, 2, 1, 3]] --> [1, 2, 3, 4]
    """

    if isinstance(X[0], int):
        return sorted(X)
    else:
        return sorted(list(set(c for e in X for c in e)))

def linear_orders(Alternatives):
    """
        Generates linear orders from given list of alternatives.

        [1,2,3] --> [1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]

        Also works if the alternatives are given as a or as a string.
    """

    for S in itertools.permutations(Alternatives, len(Alternatives)):
        yield list(S)

def support(Profile, x, y):
    """
        Returns the number of voters in Profile 
        where x is preferred to y.

        [[1,2,3], [1,2,3], [2,1,3]], 1, 2 --> 2    
    """

    return len([l for l in Profile if l.index(x) - l.index(y) < 0])

def margin(Profile, x, y):
    """
        Returns the margin of victory for alternative x over alternative y 
        with respect to the given profile Profile. 

        Can be negative.

        [[1,2,3], [1,3,2]], 1, 2 --> 2-0 = 2
        [[1,2,3], [1,3,2]], 2, 1 --> 0-2 = -2
    """
    return support(Profile, x, y) - support(Profile, y, x)

def SMG(Graph_Thingy):
    """
        Returns the SMG (simple majority graph) of Graph_Thingy as a list 
        of tuples. Each tuple (x, y) is an edge in the graph, 
        indicating that there is a strict preference for x over y
        with respect to Graph_Thingy.

        Graph_Thingy can be a profile or a linear order.
        
        [1,2,3] --> [(1,2), (2,3), (1,3)]
        [[1,2,3], [2,3,1], [3,1,2]] --> [(1,2), (2,3), (3,1)]
    """

    if isinstance(Graph_Thingy[0], int): # in this case Graph_Thingy is (or should be) a linear order
        return list(itertools.combinations(Graph_Thingy, 2)) # return just the individual edges, or comparisons, of this order
    if isinstance(Graph_Thingy[0], tuple): # here it's assumed that Graph_Thingy is a set of tuples, in which case nothing needs to be done
        return sorted(Graph_Thingy)
    elif isinstance(Graph_Thingy[0], list): # Graph_Thingy should now be a profile
        result = []
        for (a, b) in itertools.combinations(alternatives(Graph_Thingy), 2): # add the edges that enjoy majority support
            if margin(Graph_Thingy, a, b) > 0:
                result.append((a, b))
            if margin(Graph_Thingy, a, b) < 0:
                result.append((b, a))
        return sorted(result)

def hamming_distance(L1, L2):
    """
        Returns the Hamming distance between two lists of tuples.
        A tuple (x, y) stands for a strict preference of x over y,
        and is assumed to be obtained from either a profile or a linear order.

        [(1,2), (1,3)], [(2,3)] --> 3
        [(1,2), (2,3), (1,3)], [(3,2), (2,1), (3,1)] --> 6
    """

    return len(set(L1) ^ set(L2)) # the length of the symmetric difference of L1 and L2, thought of as sets

A = [1,2,3]
P = [[1,2,3], [2,3,1], [3,1,2]]

L1 = [(1,2), (1,3)]
L2 = [(2,3)]


