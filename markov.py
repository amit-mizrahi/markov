import random
import utils

""" Predicts the next word in a string of text, treating text generation as a Markov process. """

MAX_N_GRAM = 10

def assemble_bigram_transition_matrix(s):
    """ Creates the transition matrix for the 'generate single word' Markov process.
    :returns a dictionary of the form {'word1':
        {'next_word1': frequency, 'next_word2': frequency, ...},
    ...}
    """
    transition_matrix = {}
    tokens = utils.tokenize(s)
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
    """ Predicts the next word in a sequence of words using the bigram transition matrix.
    :returns the likely next word, or None if it is impossible to determine. """
    transition_matrix = assemble_bigram_transition_matrix(s)
    if word in transition_matrix:
        next_word_dict = transition_matrix[word]
        return utils.choose_randomly_with_frequencies(next_word_dict)
    else:
        return None

def assemble_ngram_transition_matrix(s):
    """ Creates the transition matrix for the 'generate n random words' Markov process,
    where n is between 1 and 9 (thus generating bigrams, trigrams, ..., 10-grams).
    :returns a dictionary of the form {'word1':
        {1: {'next_word1': frequency, ...}},
        {2: {'next_word2 next_word3': frequency, ...}},
        ...
    }
    """
    transition_matrix = {}
    tokens = utils.tokenize(s)
    for i in xrange(0, len(tokens)-(MAX_N_GRAM - 1)):
        word = tokens[i]
        for j in xrange(1, MAX_N_GRAM):
            next_words = " ".join(tokens[i+1:i+j])
            if word in transition_matrix:
                if j in transition_matrix[word]:
                    if next_words in transition_matrix[word][j]:
                        transition_matrix[word][j][next_words] += 1
                    else:
                        transition_matrix[word][j][next_words] = 1
                else:
                    transition_matrix[word][j] = { next_words : 1 }
            else:
                transition_matrix[word] = { j : { next_words: 1 } }
    return transition_matrix

class InvalidMarkovChain(Exception):
    pass

def generate_markov_chain(s, start_word, length):
    """ Generates a markov chain of length `length` and starting with `start_word,`
    given a string corpus of text `s`. Uses bigrams.
    :returns a sequence of words of length `length`, or an exception if start word is not
    in the transition matrix. """
    transition_matrix = assemble_bigram_transition_matrix(s)
    if start_word in transition_matrix:
        current_word = start_word
        result = [start_word]
        for i in xrange(length):
            next_word_dict = transition_matrix[current_word]
            next_word = utils.choose_randomly_with_frequencies(next_word_dict)
            result.append(next_word)
            current_word = next_word
        return " ".join(result)
    else:
        raise InvalidMarkovChain("Start word not found in corpus.")

def generate_ngram_markov_chain(s, start_word, length):
    """ Generates an n-gram markov chain of n-gram length `length` and starting with `start_word`,
    given a string corpus of text `s`.
    Randomly chooses between n-grams of various lengths between 2 and 10.
    :returns a sequence of words of length `length`, or an exception if start word is not
    present in the transition matrix. """
    transition_matrix = assemble_ngram_transition_matrix(s)
    if start_word in transition_matrix:
        current_word = start_word
        result = [start_word]
        for i in xrange(length):
            next_words_dict = transition_matrix[current_word]
            random_n_gram = random.randint(1, MAX_N_GRAM - 1)
            next_words = utils.choose_randomly_with_frequencies(next_words_dict[random_n_gram])
            result.append(next_words)
            current_word = next_words.split(" ")[-1]
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

def generate_ngram_chain_from_file(file, start_word, length):
    """ Generates a random n-gram Markov chain given a text file.
    :returns an n-gram Markov chain using the file contents, start word, and length """
    with open(file, 'r') as f:
        contents = f.read()
        return generate_ngram_markov_chain(contents, start_word, length)


print predict_from_file('hamlet.txt', 'you')
print generate_chain_from_file('hamlet.txt', 'you', 500)
print generate_ngram_chain_from_file('hamlet.txt', 'you', 100)
print generate_ngram_chain_from_file('dante.txt', 'the', 100)
