from utils import sort_keys_by_value

""" Predicts the next word in a string of text, treating text generation as a Markov process. """

def assemble_transition_matrix(s):
    """ Creates the transition matrix for the 'generate single word' Markov process.
    :returns a dictionary of the form {'word1':
        {'next_word1': frequency, 'next_word2': frequency, ...},
    ...}
    """
    transition_matrix = {}
    tokens = s.split()
    for i in xrange(0, len(tokens)-1):
        word = tokens[i]
        next_word = tokens[i+1]
        if word in transition_matrix:
            if next_word in transition_matrix[word]:
                transition_matrix[word][next_word] += 1
            else:
                transition_matrix[word][next_word] = 1
        else:
            transition_matrix[word] = { next_word: 1 }
    return transition_matrix

def predict_next_word(s, word):
    """ Predicts the next word in a sequence of words.
    :returns the likely next word, or None if it is impossible to determine. """
    transition_matrix = assemble_transition_matrix(s)
    if word in transition_matrix:
        next_word_dict = transition_matrix[word]
        possible_next_words = sort_keys_by_value(next_word_dict)
        return possible_next_words[0]
    else:
        return None

class InvalidMarkovChain(Exception):
    pass

def generate_markov_chain(s, start_word, length):
    """ Generates a markov chain of length `length` and starting with `start_word,`
    given a string corpus of text `s`.
    :returns a sequence of words of length `length`, or an exception if start word is not
    in the transition matrix. """
    transition_matrix = assemble_transition_matrix(s)
    if start_word in transition_matrix:
        current_word = start_word
        result = []
        for i in xrange(length):
            next_word_dict = transition_matrix[current_word]
            possible_next_words = sort_keys_by_value(next_word_dict)
            next_word = possible_next_words[0]
            result.append(next_word)
            current_word = next_word
        return " ".join(result)
    else:
        raise InvalidMarkovChain("Start word not found in corpus.")

def predict_from_file(file, word):
    """ Predicts the next word given a text file corpus and a preceding word.
    :returns the prediction from the contents of the file """
    with open(file, 'r') as f:
        contents = f.read()
        return predict_next_word(contents, word)

def generate_chain_from_file(file, start_word, length):
    """ Generates a Markov chain given a text file.
    :returns a Markov chain using the file contents, start word, and length """
    with open(file, 'r') as f:
        contents = f.read()
        return generate_markov_chain(contents, start_word, length)


print predict_from_file('hamlet.txt', 'you')
print generate_chain_from_file('hamlet.txt', 'you', 500)
