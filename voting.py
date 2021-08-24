from typing import Iterable
import string
import itertools
import networkx as nx
import matplotlib.pyplot as plt

class Alternatives:
    def __init__(self, input):
        if type(input) == int:
            self.as_characters = list(string.ascii_lowercase)[:input]
        elif type(input) == str:
            self.as_characters = sorted(list(input))
        elif isinstance(input, Iterable):
            if all(type(c) == str for c in input):
                self.as_characters = sorted(input)
            elif all(type(i) == int for i in input):
                self.as_characters = list(string.ascii_lowercase)[:len(input)]            
        self.as_integers = list(range(len(self.as_characters)))
        self.to_int_dict = {c: self.as_characters.index(c) for c in self.as_characters}
        self.to_str_dict = {i:c for c, i in self.to_int_dict.items()}
        self.number = len(self.as_integers)

    def __str__(self) -> str:
        return str(self.as_characters)

class LinearOrder:
    def __init__(self, input):
        self.alternatives = Alternatives(input)
        if type(input) == str:
            self.as_str = input
            self.as_int_list = [self.alternatives.to_int_dict[c] for c in input]
        elif isinstance(input, Iterable):
            if all([type(c) == str for c in input]):
                self.as_str = ''.join(input)
                self.as_int_list = [self.alternatives.to_int_dict[c] for c in input]
            if all([type(i) == int for i in input]):
                self.as_int_list = input 
                self.as_str = ''.join([self.alternatives.to_str_dict[i] for i in input])

    def __str__(self) -> str:
        return self.as_str
    
    def length(self):
        return len(self.as_int_list)

    def edges(self):
        return list(itertools.combinations(self.as_int_list, 2))

    def index(self, x):
        if isinstance(x, int):
            return self.as_int_list.index(x)
        if isinstance(x, str):
            return self.as_str.index(x)

class MajorityGraph:
    def __init__(self, nodes, edge_list = [], weighted_edge_list = []):
        self.G = nx.DiGraph()
        self.alternatives = Alternatives(nodes)
        self.G.add_nodes_from(self.alternatives.as_integers)
        if edge_list and all([type(e) == str for e in edge_list]):
            self.G.add_edges_from([(self.alternatives.to_int_dict[e[0]], self.alternatives.to_int_dict[e[1]]) for e in edge_list])
        self.G.add_weighted_edges_from(weighted_edge_list)
    
    def add_nodes_from(self, input):
        self.G.add_nodes_from(input)
    
    def add_edge(self, u, v, weight=1):
        if type(u) == str and type(v) == str:
            self.G.add_edge(self.alternatives.to_int_dict[u], self.alternatives.to_int_dict[v], weight = weight)
        if type(u) == int and type(v) == int:
            self.G.add_edge(u, v, weight = weight)
        
    def nodes(self):
        return self.G.nodes
    
    def edges(self):
        return self.G.edges
    
    def draw(self):
        pos = nx.kamada_kawai_layout(self.G)
        nx.draw(self.G, pos, labels = self.alternatives.to_str_dict, node_color='white', font_size=16, font_family='serif', node_size=1000, edgecolors = 'black')
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels = labels)
        plt.show()

class Profile:
    def __init__(self, orders):
        self.orders = [LinearOrder(order) for order in orders]
        self.alternatives = self.orders[0].alternatives

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
        G = MajorityGraph(nodes = self.alternatives.as_integers)
        for (x, y) in itertools.combinations(self.alternatives.as_integers, 2): # add the edges that enjoy majority support
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

class VotingRules:
    def __init__(self, input):
        if type(input) == MajorityGraph:
            self.G = input
        if type(input) == Profile:
            self.G = input.majority_graph()
        self.Slater_result = {}
        self.Slater_minimal_score = float('inf')

    def compute_Slater_result(self):
        nodes, edges = self.G.nodes(), self.G.edges()
        for l in Generator().all_linear_orders(nodes):
            current_score = Distance().Hamming(edges, l.edges())
            if current_score < self.Slater_minimal_score:
                self.Slater_result = {l}
                self.Slater_minimal_score = current_score
            elif self.Slater_minimal_score == current_score:
                self.Slater_result = self.Slater_result | {l}
    
    def show_Slater_result(self) -> str:
        print("{" + str(sorted([str(l) for l in self.Slater_result]))[1:-1] + "}")