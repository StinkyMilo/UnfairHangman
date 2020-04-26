What each file does:
word_fomatting.py determines what words to include and exports them to word_lengths.txt as an array first of all words, then all words of a specific length.
unfair_hangman.py lets you play hangman against your cheating opponent.
hangman_guess.py iterates through words and guesses them with the theoretical best strategy.
threaded_guess creates 10 threads and tries to do the same thing, but will eventually run into an error that I haven't bothered to fix, but it will, exporting every two minutes, give you the number of guesses required to get the number of guesses needed for most words in English.
grapher.py uses matplotlib to graph the number of words that took each amount of incorrect guesses.
word_data_652.json contains most English words and the number of guesses required to guess them by the theoretical best guessing strategy.
English words downloaded from here:
https://github.com/dwyl/english-words