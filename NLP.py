
#uni gram
char_list = [ch for ch in open('./Data/en-the-little-prince.txt').read().lower() if ch != '\n' if ch != ' ' if ch != '"' if ch != '-' if ch != ':' if ch != ';' if ch != '.']
print(char_list)