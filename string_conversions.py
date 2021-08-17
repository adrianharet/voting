import string

alphabet_list = list(string.ascii_lowercase)
char_dict  = {c: alphabet_list.index(c) for c in alphabet_list}

def to_integers(G):
    """
        Assumes that G (a profile or a majority graph) is given as a list of strings, 
        and converts it to integer values.
    """
    if len(G[0]) == 2: # assuming G is a simple majority graph
        return [(char_dict[element[0]], char_dict[element[1]]) for element in G]
    else: # G is a profile of linear orders
        return [[char_dict[c] for c in element] for element in G]

def to_string(G):
    """
        Assumes that G (a profile or a majority graph) is given as a list of integers, 
        and converts it to string form.
    """
    return [''.join([c for i in element for c in alphabet_list if char_dict[c] == i]) for element in G]
