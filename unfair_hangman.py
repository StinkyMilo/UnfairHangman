from random import randint
import json
# Rules for word formatting (editable in word_formatting.py): Must have vowels (this does exclude some but it feels too unfair otherwise), can't be an acronym, can't have special characters. Taken from https://github.com/dwyl/english-words
# Initialize words
words = json.loads(open("word_lengths.txt","r").read())
length = int(input("Enter Word Length (0 for random, max " + str(len(words)-1) + "):\n"))
if length == 0:
    length = randint(1,len(words)-1)
def select_word(length=0):
    return words[length][randint(0,len(words[length])-1)]

excluded_letters=""
guessed_letters = ""
possible_words=words[length]
for _ in range(0,length):
    guessed_letters+="*"

# Initialize Hangmen
hangmen_txt = open("hangmen.txt","r").read().split("!end\n")
hangmen=[]
for string in hangmen_txt:
    images = string[string.index("\n"):].split("!next")
    hangmen.append({"guesses":string[string.index("guesses=")+8:string.index("\n")],"images":images})

def all_valid_words():
    possibilities = []
    for word in possible_words:
        word = word.lower()
        if is_valid_word(word):
            possibilities.append(word)
    return possibilities

def is_valid_word(word):
    for letter in excluded_letters:
        if letter in word:
            return False
    for i in range(0,len(word)):
        if (guessed_letters[i] != "*" and word[i] != guessed_letters[i]) or (guessed_letters[i] == "*" and word[i] in guessed_letters):
            return False
    return True

def get_revealed_letters(word, guessed, guess):
    op = ""
    for i in range(0,len(word)):
        if guessed[i]!="*":
            op += guessed[i]
        elif word[i]==guess:
            op+=guess
        else:
            op+="*"
    return op

def evaluate_guess(guess):
    global excluded_letters
    global guessed_letters
    global possible_words
    # If it can fail you, it will.
    possible_words=all_valid_words()
    for word in possible_words:
        if guess not in word:
            excluded_letters+=guess
            return False, guessed_letters
    # If all remaining words contain the guess, takes the most common combination
    # Step 0: Find what would be revealed for all possible words
    combos = {}
    for word in possible_words:
        combo = get_revealed_letters(word,guessed_letters,guess)
        # If not already in combos, add a new combo with this as one of its words
        if not combo in combos:
            combos[combo] = [word]
        #If combo already exists, add to word list
        else:
            combos[combo].append(word)
    # Step 1: Find most numerous reveal
    max_count = 0
    max_combo=None
    candidates = []
    for combo in combos:
        if len(combos[combo])>max_count:
            max_count=len(combos[combo])
            candidates = combos[combo]
            max_combo=combo
    guessed_letters = max_combo
    return True, max_combo

def format_response(response):
    op = ""
    for i in response:
        if i=="*":
            op+="_ "
        else:
            op+= i + " "
    return op
def play_game(max_guesses=6):
    guesses = max_guesses
    print(format_response(guessed_letters))
    has_hangman = False
    this_man=None
    for hangman in hangmen:
        if hangman["guesses"]==str(max_guesses):
            has_hangman=True
            this_man=hangman["images"]
            break
    while True:
        success, response = evaluate_guess(input("Guess:\n").lower())
        if has_hangman:
                print(this_man[max_guesses-guesses])
        print(format_response(response))
        if not success:
            guesses-=1
            if guesses<=0:
                print("Game over. The word was " + possible_words[randint(0,len(possible_words)-1)])
                return False
        elif "*" not in response:
            print("You won!")
            return True
        print("Guesses remaining: " + str(guesses))
play_game(7)
            
        
        
        
