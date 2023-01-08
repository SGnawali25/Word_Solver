import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
,'*':0}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word_length = len(word)
    if not word_length:
        return 0
    first_component = 0
    for char in word:
        first_component += SCRABBLE_LETTER_VALUES[char.lower()]
    second_component = 7 * word_length - 3 * (n - word_length)
    if second_component < 1:
        second_component = 1
    return first_component * second_component


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3)) - 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    hand['*'] = 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    new_hand = hand.copy()
    for character in word:
        character = character.lower()
        if character in new_hand:
            new_hand[character] -= 1
            if new_hand[character] == 0:
                del(new_hand[character])
    return new_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word = word.lower()
    word_frequency = get_frequency_dict(word)
    # print(word_frequency)
    if '*' not in word:
        if word not in word_list:
            return False
    else:
        word_dict = {'first':'','second':'','third':'','fourth':'','fifth':''}
        vowel = {'first':'a','second':'e','third':'i','fourth':'o','fifth':'u'}
        for character in word:
            for part in word_dict:
                if character == '*':
                    word_dict[part] += vowel[part]
                else:
                    word_dict[part] += character
        possible_word = list(word_dict.values())
        condition_to_check_atleast_one_valid_word = False
        for element in possible_word:
            if element in word_list:
                condition_to_check_atleast_one_valid_word = True
        if not condition_to_check_atleast_one_valid_word:
            return False

    for character in word_frequency:
        if character != '*':
            if character not in hand or word_frequency[character] > hand[character]:
                return False

    return True




    new_dict = get_frequency_dict(word)
    for element in word_frequency:
        check_dict = get_frequency_dict(element)

    return True


# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    count = 0
    for item in hand:
        count += hand[item]
    return count

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """

    total_score = 0
    while True:
        print('Current hand:', end='')
        display_hand(hand)
        user_input = input('Enter word, or "!!" to indicate you are finished: ')
        if user_input == '!!':
            break
        if is_valid_word(user_input,hand,word_list):
            score = get_word_score(user_input, calculate_handlen(hand))
            total_score += score
            print(f'"{user_input}" earned {score}. Total: {total_score} points')
            hand = update_hand(hand, user_input)
        else:
            print("That is not a valid word. Please choose another word.")
        if not len(hand):
            break
        print()

    if len(hand) == 0:
        print()
        print(f"Ran out of letters. ")
    print(f'Total score for this hand: {total_score}')
    return total_score

def substitute_hand(hand, letter):
    """ 

    """
    if letter not in hand:
        return hand
    new_dict = hand.copy()
    all_characters = string.ascii_lowercase
    del(new_dict[letter])
    while True:
        character = random.choice(all_characters)
        if character not in hand:
            break
    new_dict[character] = hand[letter]
    return new_dict


    
def play_game(word_list):
    """

    """
    
    times = int(input('Enter total number of hands: '))
    final_score = 0
    replay_chance = 1
    substitute_chance = 1
    check = [{'d': 2, 'a': 1, '*': 1},{'d': 2, 'a': 1, 'o': 1, 'u': 1, 't': 1, '*': 1},{'a': 1, 'c': 1, 'i': 1, 'p': 1, 'r': 1, 't': 1, '*': 1},{'d': 2, '*': 1, 'l': 1, 'o': 1, 'u': 1, 't': 1}]
    for i in range(times):
        hand = deal_hand(7)
        if substitute_chance:
            print('Current hand:', end='')
            display_hand(hand)
            substitute = input("Would you like to substitue a letter? ")
            if substitute.lower() == 'yes':
                letter = input('Which letter would you like to replace: ')
                hand = substitute_hand(hand,letter)
                substitute_chance -= 1
            print()

        first_score = play_hand(hand,word_list)
        print('----------')
        if replay_chance:
            play_again = input("Would you like to replay the hand?")
            if play_again.lower() == 'yes':
                replay_chance -= 1
                second_score = play_hand(hand,word_list)
                print('----------')
                final_score += max(first_score,second_score)
            else:
                print()
                final_score += first_score

    print()
    print(f'Total score over all hands: {final_score}')


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
