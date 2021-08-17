import helpers
import string_conversions

def slater(G):
    """
        Returns a list of linear orders: the orders selected by the Slater rule, 
        i.e., the orders closest (in terms of Hamming distance) to the simply majority 
        graph of G.

        G can be given a profile or a list of individual edges (the simple majority graph).

        [[1,2,3], [1,3,2]] --> [[1,2,3], [1,3,2]]
        [(1,2), (1,3)] --> [[1,2,3], [1,3,2]]
    """
    if G == []:
        return []
    else:
        M = helpers.SMG(G)
        result = []
        current_minimal_score = float('inf')
        for l in helpers.linear_orders(helpers.alternatives(G)):
            current_score = helpers.hamming_distance(M, helpers.SMG(l))
            if current_score < current_minimal_score:
                result = [l]
                current_minimal_score = current_score
            elif current_minimal_score == current_score:
                result.append(l)
        return result

P = ['abc', 'bca', 'cab']
print(slater(string_conversions.to_integers(P)))






