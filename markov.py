""" Predicts the next word in a string of text, treating text generation as a Markov process. """

def assemble_transition_matrix(s):
    """ Creates the transition matrix for the 'generate single word' Markov process.
    :return a dictionary of the form {'word1':
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
        possible_next_words = sorted(
            next_word_dict.keys(),
            reverse = True,
            key = next_word_dict.get
        )
        return possible_next_words[0]
    else:
        return None

def predict_from_file(file, word):
    with open(file, 'r') as f:
        contents = f.read()
        return predict_next_word(contents, word)

print predict_from_file('hamlet.txt', 'you')
