from typing import Iterable
import string
import itertools
import networkx as nx
import matplotlib.pyplot as plt

class Alternatives:
    def __init__(self, input):
        """
            Should be given as list of characters.
        """
        self.list = sorted(input)

    def __str__(self) -> str:
        return str(self.list)
    
    def __iter__(self):
        return iter(self.list)

    def number(self):
        return len(self.list)

class LinearOrder:
    def __init__(self, input):
        if type(input) == list:
            self.order = input
        if type(input) == str:
            self.order = list(input)

    def __str__(self) -> str:
        return ''.join(self.order)
    
    def length(self):
        return len(self.order)

    def edges(self):
        return list(itertools.combinations(self.order, 2))

    def index(self, x):
        return self.order.index(x)

class MajorityGraph:
    def __init__(self, nodes, edge_list = []):
        self.G = nx.DiGraph()
        self.weighted = all(len(e) == 3 for e in edge_list) 
        self.G.add_nodes_from(nodes)
        if self.weighted:
            self.G.add_weighted_edges_from(edge_list)
        else:
            self.G.add_weighted_edges_from([(e[0], e[1], 1) for e in edge_list])
    
    def add_nodes_from(self, input):
        self.G.add_nodes_from(input)
    
    def add_edge(self, u, v, weight=1):
        self.G.add_edge(u, v, weight = weight)
    
    def update_edge_weight(self, u, v, w):
        self.G[u][v]['weight'] = w
        
    def nodes(self):
        return self.G.nodes
    
    def edges(self):
        return self.G.edges
    
    def weighted_edges(self):
        return nx.get_edge_attributes(self.G, 'weight')
    
    def cycles(self):
        return sorted(nx.simple_cycles(self.G))

    def draw(self):
        pos = nx.circular_layout(self.G)
        nx.draw(self.G, pos, node_color='white', with_labels=True, font_size=16, font_family='serif', node_size=1000, edgecolors = 'black')
        if self.weighted:
            labels = nx.get_edge_attributes(self.G, 'weight')
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)  
        plt.show()

class Profile:
    def __init__(self, input):
        self.orders = [LinearOrder(order) for order in input]
        self.alternatives = Alternatives(input[0])

    def __str__(self):
        return str([str(L) for L in self.orders])

    def support(self, x, y):
        """
            Returns the number of voters in the profile 
            who prefer x to y.

            [[1,2,3], [1,2,3], [2,1,3]], 1, 2 --> 2    
        """
        s = 0
        for l in self.orders:
            if l.index(x) - l.index(y) < 0:
                s += 1
        return s

    def margin(self, x, y):
        """
            Returns the margin of victory for alternative x over alternative y 
            with respect to the given profile Profile. 

            Can be negative.

            [[1,2,3], [1,3,2]], 1, 2 --> 2-0 = 2
            [[1,2,3], [1,3,2]], 2, 1 --> 0-2 = -2
        """
        return self.support(x, y) - self.support(y, x)

    def majority_graph(self):
        G = MajorityGraph(nodes = self.alternatives)
        for (x, y) in itertools.combinations(self.alternatives, 2): # add the edges that enjoy majority support
            w = self.margin(x,y)
            if w > 0:
                G.add_edge(x, y, weight = w)
            if w < 0:
                G.add_edge(y, x, weight = -w)
        return G

class Generator:
    def __init__(self) -> None:
        pass
    
    def all_linear_orders(self, alternatives):
        for S in itertools.permutations(alternatives, len(alternatives)):
            yield LinearOrder(list(S))  
                 
class Distance:
    def __init__(self) -> None:
        pass

    def Hamming(self, l1, l2):
        """
            Returns the Hamming distance between two lists of tuples.
            A tuple (x, y) stands for a strict preference of x over y,
            and is assumed to be obtained from either a profile or a linear order.

            [(1,2), (1,3)], [(2,3)] --> 3
            [(1,2), (2,3), (1,3)], [(3,2), (2,1), (3,1)] --> 6
        """
        return len(set(l1) ^ set(l2)) # the length of the symmetric difference of L1 and L2, thought of as sets
    
    def weightedHamming(self, G, L):
        """
            Assumes G is a MajorityGraph and L is a LinearOrder.
            Computes distance based on number of edges in G that l inverts.
        """
        d = 0
        for (x, y) in L.edges():
            if (y, x) in G.edges():
                d += G.weighted_edges()[(y, x)]
        return d

class VotingRules:
    def __init__(self, input):
        if type(input) == MajorityGraph:
            self.G = input
        if type(input) == Profile:
            self.G = input.majority_graph()
        self.Slater_result = {}
        self.Kemeny_result = {}
        self.Slater_minimal_score = float('inf')
        self.Kemeny_minimal_score = float('inf')

    def closest_to_graph(self, G):
        """
            Assumes G is a MajorityGraph.
        """
        result = {}
        minimal_score = float('inf')
        for L in Generator().all_linear_orders(G.nodes()):
            current_score = Distance().weightedHamming(G, L)
            if current_score < minimal_score:
                result = {L}
                minimal_score = current_score
            elif current_score == minimal_score:
                result = result | {L}
        return (result, minimal_score)
    
    def compute_Kemeny_result(self):
        self.Kemeny_result, self.Kemeny_minimal_score = self.closest_to_graph(self.G)[0], self.closest_to_graph(self.G)[1] 
    
    def compute_Slater_result(self):
        unweightedG = MajorityGraph(nodes=self.G.nodes(), edge_list=self.G.edges())
        self.Slater_result, self.Slater_minimal_score = self.closest_to_graph(unweightedG)[0], self.closest_to_graph(unweightedG)[1] 

    def show_Slater_result(self) -> str:
        print("{" + str(sorted([str(l) for l in self.Slater_result]))[1:-1] + "}")

    def show_Kemeny_result(self) -> str:
        print("{" + str(sorted([str(l) for l in self.Kemeny_result]))[1:-1] + "}")