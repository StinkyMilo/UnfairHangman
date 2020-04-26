import json
import threading
import time
words = json.loads(open("word_lengths.txt","r").read())
letters = "abcdefghijklmnopqrstuvwxyz"

def choose_guess(word_list,guessed_letters):
    letter_freq = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for word in word_list:
        for i in range(0,len(letters)):
            if letters[i] not in guessed_letters and letters[i] in word:
                letter_freq[i]+=1
    return letters[letter_freq.index(max(letter_freq))]

def evaluate_guess(guess, word, excluded_letters, known_letters):
    if guess in word:
        new_known = ""
        for i in range(0,len(word)):
            if known_letters[i]=="*" and word[i]==guess:
                new_known+=guess
            else:
                new_known+=known_letters[i]
        return True, new_known
    return False, excluded_letters + [guess]

def get_possible_words(known_letters, excluded_letters, eligible_words):
    op=[]
    for word in eligible_words:
        if is_valid_word(word,known_letters,excluded_letters):
            op.append(word)
    return op

def is_valid_word(word,known_letters,excluded_letters):
    for letter in excluded_letters:
        if letter in word:
            return False
    for i in range(0,len(known_letters)):
        if known_letters[i]!="*" and known_letters[i]!=word[i]:
            return False
    return True

def guess_word(word):
    wrong_guesses=0
    eligible_words = words[len(word)]
    excluded_letters = []
    known_letters = ""
    guessed_letters=[]
    for _ in range(0,len(word)):
        known_letters+="*"
    while True:
        guess = choose_guess(eligible_words,guessed_letters)
        guessed_letters.append(guess)
        success, response = evaluate_guess(guess, word, excluded_letters, known_letters)
        if success:
            known_letters = response
            if "*" not in response:
                return wrong_guesses
        else:
            wrong_guesses+=1
            excluded_letters=response
        eligible_words = get_possible_words(known_letters,excluded_letters,eligible_words)
        
all_words = words[0]
data = {}
class ThreadedGuesser(object):
    def __init__(self, all_words):
        self.all_words=all_words
        thread = threading.Thread(target=self.run,args=())
        thread.start()

    def run(self):
        global data
        for word in range(0,len(self.all_words)):
            data[self.all_words[word]]=guess_word(self.all_words[word])
            if word % 100 == 0:
                print("Completed " + self.all_words[word])
thread_count=10
guessers=[]
for i in range(0,thread_count-1):
    guessers.append(ThreadedGuesser(all_words[i*int(len(all_words)/10):(i+1)*int(len(all_words)/10)]))
guessers.append(ThreadedGuesser(all_words[(thread_count-1)*int(len(all_words)/10):]))
z=0
while True:
    time.sleep(120)
    open("word_data_"+str(z)+".json","w").write(json.dumps(data))
    z+=1
    print("Writing...")
