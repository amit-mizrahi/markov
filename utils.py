import string

""" Helper functions. """

def sort_keys_by_value(dictionary):
    """ Sorts the keys of a dictionary by descending value in the dictionary.
    :returns the sorted list """
    return sorted(
        dictionary.keys(),
        reverse = True,
        key = dictionary.get
    )

def tokenize(s):
    """ Naively tokenizes an input string.
    :returns a list of words, all lowercase and stripped of punctuation. """
    tokens = s.split()
    tokens = map(lambda w : w.lower(), tokens)
    tokens = map(lambda w: w.translate(string.maketrans("", ""), string.punctuation), tokens)
    return tokens
