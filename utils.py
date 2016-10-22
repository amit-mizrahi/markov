import random
import string

""" Helper functions. """

def tokenize(s):
    """ Naively tokenizes an input string.
    :returns a list of words, all lowercase and stripped of punctuation. """
    tokens = s.split()
    tokens = map(lambda w : w.lower(), tokens)
    tokens = map(lambda w: w.translate(string.maketrans("", ""), string.punctuation), tokens)
    tokens = map(lambda w: w.replace("\n", ""), tokens)
    tokens = filter(lambda w: not w.isdigit(), tokens)
    return tokens

def choose_randomly_with_frequencies(frequency_dict):
    """ Takes a dictionary of word frequencies and randomly chooses a word
    with weights based on frequencies.
    :returns a randomly chosen string. """
    # Association list is a way of compressing the (potentially large) list
    # of words "multiplied by" their frequencies, instead of generating the full list.
    assoc_list = [(word, frequency_dict[word]) for word in frequency_dict]
    r = random.randint(0, len(assoc_list)-1)
    counter = 0
    # Run through the association list until reaching the word indexed at r
    for i in xrange(len(assoc_list)):
        if counter + assoc_list[i][1] < r:
            counter += assoc_list[i][1]
        else:
            return assoc_list[i][0]
