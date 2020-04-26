from random import randint
import json
words = open("dict.txt","r").read().split("\n")
letters = "abcdefghijklmnopqrstuvwxyz"
vowels = "aeiouy"
def has_vowels(word):
    for letter in vowels:
        if letter in word:
            return True
    return False
def is_valid(word):
    if not word.islower():
        return False
    for letter in word:
        if not letter.lower() in letters:
            return False
    if (len(word)>1 and word.isupper()) or not has_vowels(word):
        return False
    return True
def words_of_length(length=0):
    if length==0:
        op = []
        for word in words:
            if is_valid(word):
                op.append(word)
        return op
    else:
        op = []
        for word in words:
            if len(word)==length and is_valid(word):
                op.append(word)
        return op
def select_word(length=0):
    candidates = words_of_length(length)
    if len(candidates)==0:
        return None
    return candidates[randint(0,len(candidates)-1)]
# speed things up by saving words of different lengths to JSON
words_obj = []
i=0
while True:
    word_list = words_of_length(i)
    if len(word_list)==0:
        break
    words_obj.append(word_list)
    i+=1
open("word_lengths.txt","w").write(json.dumps(words_obj))
