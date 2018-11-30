import math
import pickle

smoothing = 0.5
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
en_language_model = {}
fr_language_model = {}
es_language_model = {}


# Function to check the probability of a character in a list of characters
def probability(list, character):
    total_values = len(list)
    character_prob = 0;
    for i in list:
        if character.lower() == i:
            character_prob+=1
    actual_prob = ((character_prob + smoothing) / (total_values + smoothing * len(alphabet)))
    return actual_prob;


# Function to check the conditional probability of a character in a list of characters
# Given the character before it
def conditional_probability(list, character, given_character):
    total_values = len(list)
    character_prob = 0;
    previous_char  = ''
    for i in list:
        if character == i and given_character == previous_char:
            character_prob+=1
        previous_char = i
    actual_prob = (character_prob / total_values)
    return actual_prob;


# Parse the file and make a list of all the characters in the file
def uni_parse(fname):
    char_list = [ch for ch in open('./Data/'+ fname).read().lower() if ch != '\n' if ch != ' ' if ch != '"' if ch != ',' if ch != '!' if ch != '-' if ch != ':' if ch != ';' if ch != '.']
    return char_list


# Function that takes a language model and a sentence and figures out the sum of probabilities of the sentence
def unigram_sentence(sentence):

    # Read the language models from a file
    fr_language_model = read_model("FR-model")
    en_language_model = read_model("EN-model")
    es_language_model = read_model("ES-model")

    probability_so_far_en = 0;
    probability_so_far_fr = 0;
    probability_so_far_es = 0;

    output = ''

    output += sentence + "\n"
    for ch in sentence:
        if ch != '\n' and ch != ' ' and ch != '"' and ch != ',' and ch != '!' and ch != '-' and ch != ':' and ch != ';' and ch != '.' and ch != '?' and ch != '’' and ch != '\'':
            probability_so_far_en += (math.log(en_language_model[ch.lower()], 10))
            probability_so_far_fr += (math.log(fr_language_model[ch.lower()], 10))
            probability_so_far_es += (math.log(es_language_model[ch.lower()], 10))

            # Unigram Model
            output += "Unigram: " + ch.lower() + "\n"
            output += "FRENCH:  " + 'P(' + ch.lower() + ') = ' + str(fr_language_model[ch.lower()]) + ' ==> log prob of sentence so far: ' + str(math.exp(probability_so_far_fr)) + "\n"
            output += "ENGLISH: " + 'P(' + ch.lower() + ') = ' + str(en_language_model[ch.lower()]) + ' ==> log prob of sentence so far: ' + str(math.exp(probability_so_far_en)) + "\n"
            output += "SPANISH: " + 'P(' + ch.lower() + ') = ' + str(es_language_model[ch.lower()]) + ' ==> log prob of sentence so far: ' + str(math.exp(probability_so_far_es)) + "\n"

    #TODO: Return language accordning to probabilities
    if probability_so_far_en > probability_so_far_fr and probability_so_far_en > probability_so_far_es:
        output += "\nAccording to the unigram model, the sentence is in English"
    elif probability_so_far_fr > probability_so_far_en and probability_so_far_fr > probability_so_far_es:
        output += "\nAccording to the unigram model, the sentence is in French"
    elif probability_so_far_es > probability_so_far_en and probability_so_far_es > probability_so_far_fr:
        output += "\nAccording to the unigram model, the sentence is in Spanish"
    else:
        output += "\nCan't tell"
    return output


# Function that will output the lamguage model and their probabilities for a unigram and a language
# Also returns the model after training
def train_unigram_model(model, language):
    language_model_output = ''

    for character in alphabet:
        if language == 'EN':
            en_language_model.update({character.lower(): probability(model, character)})
            save_model(en_language_model, language + '-model')
        elif language == 'FR':
            fr_language_model.update({character.lower(): probability(model, character)})
            save_model(fr_language_model, language + '-model')
        elif language == 'ES':
            es_language_model.update({character.lower(): probability(model, character)})
            save_model(es_language_model, language + '-model')
        else:
            language_model_output += "ERROR"
        language_model_output += ("P(" + character + ") = " + str(probability(model, character))) + '\n'

    f = open("unigram" +language+ ".txt", "w")
    f.write(language_model_output)


# Main Function to run the models given an input of sentences
def run_models(filename):
    sentences = [line.rstrip('\n') for line in open(filename)]
    filenum = 0;
    for sentence in sentences:
        filenum += 1
        output = unigram_sentence(sentence)
        f = open("output/out" + str(filenum) + ".txt", "a")
        f.write(output)

# Saves models to a file for easier accessing
def save_model(model, name):
    pickle.dump(model, open('models/' + name + ".p", "wb"))


# Read language models from a file (loads a list of probabilities
def read_model(filename):
    return pickle.load(open('models/' + filename + ".p", "rb"))


# First Attempt to Train an english model and predict if it's english.
# training_corpus_en = uni_parse("english-corpus.txt")
# training_corpus_fr = uni_parse("french-corpus.txt")
# training_corpus_es = uni_parse("spanish-corpus.txt")

# Training Language Models
# train_unigram_model(training_corpus_en, 'EN')
# train_unigram_model(training_corpus_fr, 'FR')
# train_unigram_model(training_corpus_es, 'ES')


# Running the models on the input sentences
run_models("sentences.txt")