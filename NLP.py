import math
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
    probability_so_far_en = 0;
    probability_so_far_fr = 0;
    # probability_so_far_es = 0;
    print(sentence)
    for ch in sentence:
        if ch != '\n' and ch != ' ' and ch != '"' and ch != ',' and ch != '!' and ch != '-' and ch != ':' and ch != ';' and ch != '.' and ch != '?' and ch != '’' and ch != '\'':
            probability_so_far_en += (math.log(en_language_model[ch.lower()], 10))
            probability_so_far_fr += (math.log(fr_language_model[ch.lower()], 10))
            # probability_so_far_es += (math.log(es_language_model[ch.lower()] + smoothing, 10))

            print("Unigram: " + ch.lower())
            print("FRENCH:  " + 'P(' + ch.lower() + ') = ' + str(fr_language_model[ch.lower()]) + ' ==> log prob of sentence so far: ' + str(math.exp(probability_so_far_fr)))
            print("ENGLISH: " + 'P(' + ch.lower() + ') = ' + str(en_language_model[ch.lower()]) + ' ==> log prob of sentence so far: ' + str(math.exp(probability_so_far_en)))
            # print("SPANISH: " + 'P(' + ch.lower() + ') = ' + es_language_model[ch] + ' ==> log prob of sentence so far: ' + probability_so_far_FR)

    #TODO: Return language accordning to probabilities
    if probability_so_far_en > probability_so_far_fr:
        return "\nAccording to the unigram model, the sentence is in English "
    elif probability_so_far_en < probability_so_far_fr:
        return "\nAccording to the unigram model, the sentence is in French "
    else:
        return "\nAccording to the unigram model, the sentence is in Spanish "

    return probability_so_far_en


# Function that will output the lamguage model and their probabilities for a unigram and a language
# Also returns the model after training
def train_unigram_model(model, language):
    language_model_output = ''

    for character in alphabet:
        if language == 'EN':
            en_language_model.update({character.lower(): probability(model, character)})
        elif language == 'FR':
            fr_language_model.update({character.lower(): probability(model, character)})
        elif language == 'ES':
            es_language_model.update({character.lower(): probability(model, character)})
        else:
            language_model_output += "ERROR"
        language_model_output +=  ("P(" + character + ") = " + str(probability(model, character))) + '\n'

    f = open("unigram" +language+ ".txt", "w")
    f.write(language_model_output)

    # TODO: need to be written to a file for every language
    if language == 'EN':
        #print(en_language_model)
        return en_language_model
    elif language == 'FR':
        print(fr_language_model)
        return fr_language_model
    elif language == 'ES':
        #print(es_language_model)
        return es_language_model


# First Attempt to Train an english model and predict if it's english.
training_corpora_en = uni_parse("en-moby-dick.txt")
training_corpora_fr = uni_parse("fr-vingt-mille-lieues-sous-les-mers.txt")
# training_corpora_es = uni_parse("el-principito.txt")

# Language Models
english_model = train_unigram_model(training_corpora_en, 'EN')
french_model = train_unigram_model(training_corpora_fr, 'FR')
# spanish_model = train_unigram_model(training_corpora_es, 'ES')

language = unigram_sentence("What will the Japanese economy be like next year?")
print(language)
language = unigram_sentence("She asked him if he was a student at this school. ")
print(language)
language = unigram_sentence("I'm OK.")
print(language)
language = unigram_sentence("I hate AI")
print(language)
language = unigram_sentence("Woody Allen parle.")
print(language)
language = unigram_sentence("Est-ce que l’arbitre est la?")
print(language)
language = unigram_sentence("Cette phrase est en anglais.")
print(language)
language = unigram_sentence("J’aime l’IA.")
print(language)