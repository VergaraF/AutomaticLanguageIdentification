smoothing = 0.5

def probability(list, character):
    total_values = len(list)
    character_prob = 0;
    for i in list:
        if character == i:
            character_prob+=1
    actual_prob = (character_prob / total_values) + smoothing
    return actual_prob;

def conditional_probability(list, character, given_character):
    total_values = len(list)
    character_prob = 0;
    previous_char  = ''
    for i in list:
        if character == i and given_character == previous_char:
            character_prob+=1
        previous_char = i
    actual_prob = (character_prob / total_values) + smoothing
    return actual_prob;

def uni_parse(fname):
    char_list = [ch for ch in open('./Data/'+ fname).read().lower() if ch != '\n' if ch != ' ' if ch != '"' if ch != ',' if ch != '!' if ch != '-' if ch != ':' if ch != ';' if ch != '.']
    #print(char_list)
    return char_list

def bi_parse(fname):
    char_list = [ch for ch in open('./Data/'+ fname).read().lower() if ch != '\n' if ch != ' ' if ch != '"' if ch != ',' if ch != '!' if ch != '-' if ch != ':' if ch != ';' if ch != '.']
    #print(char_list)
    return char_list

def unigram(model, sentence):
    probability_so_far = 0.5;
    for ch in sentence:
        if ch != '\n' and ch != ' ' and ch != '"' and ch != ',' and ch != '!' and ch != '-' and ch != ':' and ch != ';' and ch != '.' and ch != '?':
            probability_so_far *= probability(model, ch)
            print("P("+ch+") = " + str(probability_so_far))
    return probability_so_far



uni_model = uni_parse("en-the-little-prince.txt")
final_prob = unigram(uni_model,"What will the Japanese economy be like next year?")
print(final_prob)
