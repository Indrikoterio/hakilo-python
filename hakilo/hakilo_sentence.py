#! -*- coding: utf-8
# hakilo_sentence.py
#
# Program to divide a sentence into words and punctuation.
#
# Author: Cleve (Klivo) Lendon
# Last change: 2020-10-29
#

import os, sys

HOW_TO_USE = """\nhakilo_sentence\n
    Divides a sentence into words and punctuation.
    Usage:
    $ python3 hakilo_sentence.py "This is a sentence."
"""


def is_punctuation(ch):
    """Determines whether the character is punctuation.
    EXCEPT if the character is a period (.).
    A period could be part of an abbreviation or number (eg. 37.49).
    Return True or False.
    """
    if (ch == '.'): return False
    if (ch >= '!' and ch <= '/'): return True
    if (ch >= ':' and ch <= '@'): return True
    if (ch == '\u2013'): return True  # en-dash
    if (is_quote_mark(ch)): return True
    return False


LEFT_QUOTES  = ['\'', '"', '\u00ab', '\u2018', '\u201c']
RIGHT_QUOTES = ['\'', '"', '\u00bb', '\u2019', '\u201d']
def is_quote_mark(ch):
    """Checks whether the character is a quote mark ("'«).
    If yes, return the index of the quote mark.
    If no, return -1.
    param:   ch - character to test
    return:  True or False
    """
    if (ch in LEFT_QUOTES): return True
    if (ch in RIGHT_QUOTES): return True
    return False


def is_word_character(ch):
    """Determines whether the character is part of a word.
    Generally, words consist of Latin letters, but sometimes
    other characters are parts of words, eg.: 1st, 2nd, 3rd
    Returns True or False.
    """
    if (ch >= 'a' and ch <= 'z'): return True
    if (ch >= 'A' and ch <= 'Z'): return True
    if (ch >= '0' and ch <= '9'): return True
    if (ch >= 'À' and ch < 'ˀ'): return True
    if (ch == '-' or ch == '0xAD'): return True   # hyphen or soft hyphen
    if (ch >= 'Ά' and ch <= 'ԓ'): return True
    return False

def is_apostrophe(ch):
    """Tests if a character is an apostrophe."""
    if (ch == '\'' or ch == '\u2019' or ch == '\u02bc'): return True
    return False

def end_of_sentence(sentence, index, length):
    """Determines whether a period is at the end of a sentence.
    (If it is at the end, it must be punctuation.)
    Returns True or False
    """
    if (index >= length - 1): return True
    while (index < length):
        ch = sentence[index]
        index += 1
        if (is_word_character(ch)): return False
    return True


def split_sentence(sentence):
    """Splits a sentence. Returns an array of words."""

    words = []  # An array of words and punctuation.
    number_of_words = 0
    length = len(sentence)
    start_index = 0

    while (start_index < length):

        ch = ' '

        # Skip spaces, etc.
        while (start_index < length):
            ch = sentence[start_index]
            if (ch > ' '): break
            start_index += 1

        if (start_index >= length): break

        # A period at the end of a sentence is punctuation.
        # A period in the middle is probably part of an abbreviation
        # or number, eg.: 7.3
        if (ch == '.' and end_of_sentence(sentence, start_index, length)):
            words.append('.')
            start_index += 1
        elif (is_punctuation(ch)):
            words.append(ch)
            start_index += 1
        elif (is_word_character(ch)):
            last_index = start_index + 1
            while (last_index < length):
                ch = sentence[last_index]
                if (ch == '.'):
                    if (end_of_sentence(sentence, last_index, length)): break
                else:
                    if (is_apostrophe(ch)):
                        if (last_index < length - 1):
                            ch2 = sentence[last_index + 1]
                            if (not is_word_character(ch2)): break
                    else:
                        if (not is_word_character(ch)): break
                last_index += 1
            word = sentence[start_index : last_index]
            words.append(word)

            number_of_words += 1
            start_index = last_index

    return words

# ----------------------------------------------------
# Program runs from here.

if __name__ == '__main__':

    major = sys.version_info.major
    minor = sys.version_info.minor
    if major < 3:
        print("hakilo_sentence requires Python 3. " +
              "Your version is {}.{}.".format(major, minor))
        sys.exit(0)

    if (len(sys.argv) < 2):      # If no parameters.
        print(HOW_TO_USE)
        sys.exit(0)

    result = split_sentence(sys.argv[1])
    for word in result:
        print(word)
