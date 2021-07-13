import helpers

def slater(G):
    """
        Returns a list of linear orders: the Slater winners with respect to G.

        G can be a profile or a list of individual edges (the simple majority graph).

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

P = [[1,2,3], [2,3,1], [3,1,2]]
print(slater(P))






