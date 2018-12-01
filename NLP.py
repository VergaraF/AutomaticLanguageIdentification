import math
import pickle

smoothing = 0.5
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
en_unigram_language_model = {}
fr_unigram_language_model = {}
es_unigram_language_model = {}

en_bigram_language_model = {}
fr_bigram_language_model = {}
es_bigram_language_model = {}


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
    actual_prob = ((character_prob + smoothing) / (total_values + smoothing * len(alphabet)))
    return actual_prob;


# Parse the file and make a list of all the characters in the file
def uni_parse(fname):
    char_list = [ch for ch in open('./Data/'+ fname).read().lower() if ch != '\n' if ch != ' ' if ch != '"' if ch != ',' if ch != '!' if ch != '-' if ch != ':' if ch != ';' if ch != '.']
    return char_list


# Function that takes a language model and a sentence and figures out the sum of probabilities of the sentence
def unigram_sentence(sentence):

    # Read the language models from a file
    fr_unigram_language_model = read_model("FR-unigram-model")
    en_unigram_language_model = read_model("EN-unigram-model")
    es_unigram_language_model = read_model("ES-unigram-model")

    unigram_probability_so_far_en = 0;
    unigram_probability_so_far_fr = 0;
    unigram_probability_so_far_es = 0;

    output = ''
    output += sentence + "\n"
    for index, ch in enumerate(sentence):
        if ch != '\n' and ch != ' ' and ch != '"' and ch != ',' and ch != '!' and ch != '-' and ch != ':' and ch != ';' and ch != '.' and ch != '?' and ch != '’' and ch != '\'':
            unigram_probability_so_far_en += (math.log(en_unigram_language_model[ch.lower()], 10))
            unigram_probability_so_far_fr += (math.log(fr_unigram_language_model[ch.lower()], 10))
            unigram_probability_so_far_es += (math.log(es_unigram_language_model[ch.lower()], 10))

            # Unigram Model
            output += "Unigram: " + ch.lower() + "\n"
            output += "FRENCH:  " + 'P(' + ch.lower() + ') = ' + str(fr_unigram_language_model[ch.lower()]) + ' ==> log prob of sentence so far: ' + str(math.exp(unigram_probability_so_far_fr)) + "\n"
            output += "ENGLISH: " + 'P(' + ch.lower() + ') = ' + str(en_unigram_language_model[ch.lower()]) + ' ==> log prob of sentence so far: ' + str(math.exp(unigram_probability_so_far_en)) + "\n"
            output += "SPANISH: " + 'P(' + ch.lower() + ') = ' + str(es_unigram_language_model[ch.lower()]) + ' ==> log prob of sentence so far: ' + str(math.exp(unigram_probability_so_far_es)) + "\n"

    #TODO: Return language accordning to probabilities
    if unigram_probability_so_far_en > unigram_probability_so_far_fr and unigram_probability_so_far_en > unigram_probability_so_far_es:
        output += "\nAccording to the unigram model, the sentence is in English\n"
    elif unigram_probability_so_far_fr > unigram_probability_so_far_en and unigram_probability_so_far_fr > unigram_probability_so_far_es:
        output += "\nAccording to the unigram model, the sentence is in French\n"
    elif unigram_probability_so_far_es > unigram_probability_so_far_en and unigram_probability_so_far_es > unigram_probability_so_far_fr:
        output += "\nAccording to the unigram model, the sentence is in Spanish\n"
    else:
        output += "\nCan't tell"

    return output


# Function that takes a language model and a sentence and figures out the sum of probabilities of the sentence
def bigram_sentence(sentence):

    # Read the language models from a file
    fr_bigram_language_model = read_model("FR-bigram-model")
    en_bigram_language_model = read_model("EN-bigram-model")
    es_bigram_language_model = read_model("ES-bigram-model")

    bigram_probability_so_far_en = 0;
    bigram_probability_so_far_fr = 0;
    bigram_probability_so_far_es = 0;

    output = ''
    output += sentence + "\n"

    for index, ch in enumerate(sentence):
        if ch != '\n' and ch != ' ' and ch != '"' and ch != ',' and ch != '!' and ch != '-' and ch != ':' and ch != ';' and ch != '.' and ch != '?' and ch != '’' and ch != '\'' \
                and sentence[index+1] != '\n' and sentence[index+1] != ' ' and sentence[index+1] != '"' and sentence[index+1] != ',' and sentence[index+1] != '!' and sentence[index+1] != '-' \
                and sentence[index+1] != ':' and sentence[index+1] != ';' and sentence[index+1] != '.' and sentence[index+1] != '?' and sentence[index+1] != '’' and sentence[index+1] != '\'':

            bigram_probability_so_far_en += (math.log(en_bigram_language_model[ch.lower() + '|' + sentence[index+1].lower()], 10))
            bigram_probability_so_far_fr += (math.log(fr_bigram_language_model[ch.lower() + '|' + sentence[index+1].lower()], 10))
            bigram_probability_so_far_es += (math.log(es_bigram_language_model[ch.lower() + '|' + sentence[index+1].lower()], 10))

            # Bigram Model
            output += "Bigram: " + ch.lower() + '|' + sentence[index+1] + "\n"
            output += "FRENCH:  " + 'P(' + ch.lower() + '|' + sentence[index+1] + ') = ' + str(fr_bigram_language_model[ch.lower() + '|' + sentence[index+1].lower()]) + ' ==> log prob of sentence so far: ' + str(math.exp(bigram_probability_so_far_fr)) + "\n"
            output += "ENGLISH: " + 'P(' + ch.lower() + '|' + sentence[index+1] + ') = ' + str(en_bigram_language_model[ch.lower() + '|' + sentence[index+1].lower()]) + ' ==> log prob of sentence so far: ' + str(math.exp(bigram_probability_so_far_en)) + "\n"
            output += "SPANISH: " + 'P(' + ch.lower() + '|' + sentence[index+1] + ') = ' + str(es_bigram_language_model[ch.lower() + '|' + sentence[index+1].lower()]) + ' ==> log prob of sentence so far: ' + str(math.exp(bigram_probability_so_far_es)) + "\n"

    # TODO: Return language accordning to probabilities
    if bigram_probability_so_far_en > bigram_probability_so_far_fr and bigram_probability_so_far_en > bigram_probability_so_far_es:
        output += "\nAccording to the bigram model, the sentence is in English\n"
    elif bigram_probability_so_far_fr > bigram_probability_so_far_en and bigram_probability_so_far_fr > bigram_probability_so_far_es:
        output += "\nAccording to the bigram model, the sentence is in French\n"
    elif bigram_probability_so_far_es > bigram_probability_so_far_en and bigram_probability_so_far_es > bigram_probability_so_far_fr:
        output += "\nAccording to the bigram model, the sentence is in Spanish\n"
    else:
        output += "\nCan't tell"

    return output


# Function that will output the lamguage model and their probabilities for a unigram and a language
# Also returns the model after training
def train_unigram_model(model, language):
    language_model_output = ''

    for character in alphabet:
        if language == 'EN':
            en_unigram_language_model.update({character.lower(): probability(model, character)})
            save_model(en_unigram_language_model, language + '-unigram-model')
        elif language == 'FR':
            fr_unigram_language_model.update({character.lower(): probability(model, character)})
            save_model(fr_unigram_language_model, language + '-unigram-model')
        elif language == 'ES':
            es_unigram_language_model.update({character.lower(): probability(model, character)})
            save_model(es_unigram_language_model, language + '-unigram-model')
        else:
            language_model_output += "ERROR"
        language_model_output += ("P(" + character + ") = " + str(probability(model, character))) + '\n'

    f = open("unigram" +language+ ".txt", "w")
    f.write(language_model_output)


# Function that will output the lamguage model and their probabilities for a unigram and a language
# Also returns the model after training
def train_bigram_model(model, language):
    language_model_output = ''

    # Nested loop through get conditional probabilities
    for given in alphabet:
        given_character = given
        for character in alphabet:
            if language == 'EN':
                en_bigram_language_model.update({character.lower() + "|" + given_character: conditional_probability(model, character, given_character)})
                save_model(en_bigram_language_model, language + '-bigram-model')
                language_model_output += ("P(" + character + "|" + given_character + ") = " + str(en_bigram_language_model[character.lower() + "|" + given_character]) + '\n')
            elif language == 'FR':
                fr_bigram_language_model.update({character.lower() + "|" + given_character: conditional_probability(model, character, given_character)})
                save_model(fr_bigram_language_model, language + '-bigram-model')
                language_model_output += ("P(" + character + "|" + given_character + ") = " + str(fr_bigram_language_model[character.lower() + "|" + given_character]) + '\n')
            elif language == 'ES':
                es_bigram_language_model.update({character.lower() + "|" + given_character: conditional_probability(model, character, given_character)})
                save_model(es_bigram_language_model, language + '-bigram-model')
                language_model_output += ("P(" + character + "|" + given_character + ") = " + str(es_bigram_language_model[character.lower() + "|" + given_character]) + '\n')
            else:
                language_model_output += "ERROR"

            f = open("bigram" + language + ".txt", "w")
            f.write(language_model_output)


# Main Function to run the models given an input of sentences
def run_models(filename):
    sentences = [line.rstrip('\n') for line in open(filename)]
    filenum = 0;
    for sentence in sentences:
        filenum += 1
        unigram_output = unigram_sentence(sentence)
        bigram_output = bigram_sentence(sentence)
        f = open("output/out" + str(filenum) + ".txt", "a")
        f.write(unigram_output + '\n' + bigram_output)


# Saves models to a file for easier accessing
def save_model(model, name):
    pickle.dump(model, open('models/' + name + ".p", "wb"))


# Read language models from a file (loads a list of probabilities
def read_model(filename):
    return pickle.load(open('models/' + filename + ".p", "rb"))


# Get Training corpus in EN, FR, ES
training_corpus_en = uni_parse("english-corpus.txt")
training_corpus_fr = uni_parse("french-corpus.txt")
training_corpus_es = uni_parse("spanish-corpus.txt")

# Training Unigram Language Models
#train_unigram_model(training_corpus_en, 'EN')
#train_unigram_model(training_corpus_fr, 'FR')
#train_unigram_model(training_corpus_es, 'ES')

# Training Bigram Language Models
#train_bigram_model(training_corpus_en, 'EN')
#train_bigram_model(training_corpus_fr, 'FR')
#train_bigram_model(training_corpus_es, 'ES')

# Running the models on the input sentences
run_models("sentences.txt")