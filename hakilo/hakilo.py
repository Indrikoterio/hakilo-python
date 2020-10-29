#! -*- coding: utf-8
# hakilo.py
#
# Program to divide a text into sentences.
#
# Author: Klivo Lendon
# Last change: 2020-10-25
#

import os, sys
from .hakilo_sentence import split_sentence

HOW_TO_USE = """\nHakilo\n
    Divides a text into sentences, one sentence per line.
    Usage:
    $ python3 hakilo.py text_file.txt
"""

def is_pqx(text, index, length):
   """Return true if character at index is a period, question mark or exclamation mark."""
   if (index >= length): return False
   c = text[index]
   if (c == "." or c == "?" or c == "!"): return True
   return False

def is_line_break(text, index, length):
   """Determines whether the character at the index is a line break."""
   if (index >= length): return False
   c = text[index]
   if (c == "\n" or c == "\r" or c == "\f" or c == "\v"): return True
   return False

START_QUOTE_MARKS = "'\"«‹‘“❝〝❛❮"
END_QUOTE_MARKS   = "'\"»›’”❞〞❜❯"
def is_end_quote(text, index, length):
   """Return true if character at index is an end quote."""
   if (index >= length): return False
   return text[index] in END_QUOTE_MARKS

START_BRACKETS = "([{）］｝"
END_BRACKETS   = ")]}（［｛"
def is_end_bracket(text, index, length):
   """Return true if character at index is an end bracket."""
   if (index >= length): return False
   return text[index] in END_BRACKETS

OTHER = 0
PQX = 1   # Period, Question mark, eXclamation mark.
UC_LETTER = 2
LC_LETTER = 3
LINE_BREAK = 4
END_OF_FILE = 5
START_QUOTE = 6
END_QUOTE = 7
START_BRACKET = 8
END_BRACKET = 9
COMMA = 10
COLON = 12
SEMICOLON = 12
START_OF_FILE = 13
SPACE = 14


def what_follows(text, index, length):
    """Determines what sort of character comes after the given index.
    The method skips over space characters. It returns a tuple,
    which has a code for the type of character, and the new index."""
    i = index + 1
    while (i < length):
        c = text[i]
        if (c != " "):
            if (c == "." or c == "?" or c == "!"): return (PQX, i)
            if (c.isupper()): return (UC_LETTER, i)
            if (c.islower()): return (LC_LETTER, i)
            if (is_line_break(text, i, length)): return (LINE_BREAK, i)
            if (is_end_quote(text, i, length)): return (END_QUOTE, i)
            if (is_end_bracket(text, i, length)): return (END_BRACKET, i)
            return (OTHER, i)
        i += 1
    return (END_OF_FILE, i)

def initial_precedes(text, index, length):
    """Returns True if an initial precedes the current index.
    Initials do not indicate the end of a sentence, eg.: J. K. Rowling
    """
    if (index == 0): return False
    c = text[index - 1]
    if (c.isupper()):
        if (index == 1): return True
        c2 = text[index - 2]
        if (c2 == " " or c2 == "." or
            c2 == "\n" or c2 == "\r" or
            c2 == "\f" or c2 == "\v"): return True
    return False

ABBREV = ["cf.", "e.g.", "eg.", "i.e.", "ie.", "vs.", "viz."]

# Ref: https://sites.google.com/a/ngs.org/ngs-style-manual/home/M/military-ranks
HONORIFICS = [
             "Mr.", "mr.", "Mrs.", "mrs.", "Ms.", "ms.", "Messrs.", "messrs.",
             "Dr.", "dr.", "Prof.", "prof.", "St.", "st.", "Inĝ.", "inĝ.",
             "Rev.", "rev.", "Br.", "br.", "Sr.", "sr.", "Fr.", "fr.",
             "Adm.", "adm.", "Brig.", "brig."
             "Capt.", "capt.", "Cmdr.", "cmdr.",
             "Col.", "col.", "Cpl.", "cpl.",
             "Gen.", "gen.", "Lt.", "lt.", "Maj.", "maj.",
             "Pfc.", "pfc.", "Pvt.", "pvt.", "Pte.", "pte.",
             "Sgt.", "sgt.",
             "habil."]

def known_abbreviation(text, index, length):
    """Many titles, such as Mr., Mrs., Dr. etc., end with a period,
    and are followed by a capitalized name. The period after such
    a title does not mark the end of a sentence, so such titles
    need to be detected.
    """
    if (index == 0 or index >= length): return False
    i = index - 1
    # Go to previous space
    while (i >= 0):
        c = text[i]
        if (not c.isalpha()): break
        if (index - i > 7): break
        i -= 1
    i += 1
    for title in HONORIFICS:
        if (substring_at_index(text, i, length, title)): return True
    for abb in ABBREV:
        if (substring_at_index(text, i, length, abb)): return True
    return False

def alpha_immediately_after(text, index, length):
    """Returns True if an alphanumeric (letter/number) occurs
    immediately after the given index."""
    if (index >= length -1): return False
    a = text[index + 1]
    if (a.isalpha()): return True
    return False

def substring_at_index(text, index, length, substr):
    """Determines whether the given string contains the substring at the given index."""
    if (index + len(substr) > length):
        return False
    i = 0
    for chr in substr:
        if (text[index + i] != chr): return False
        i += 1
    return True

def blank_line_or_ff(text, index, length):
    """A blank line (two consecutive new lines) or form feed terminates a sentence.
    It is necessary to return the t/f flag and the next index as a tuple.""" 
    if (substring_at_index(text, index, length, "\n\n")): return (True, index + 2)
    if (substring_at_index(text, index, length, "\r\n\r\n")): return (True, index + 4)
    if (substring_at_index(text, index, length, "\r\r")): return (True, index + 2)
    if (substring_at_index(text, index, length, "\n\t")): return (True, index + 2)
    c = text[index]
    if (c == "\f" or c == "\v"): return (True, index + 1)  # Form feed, vertical tab.
    return (False, index + 1)


def is_eos(text, index, length):
    """Determines whether the character at the given index represents the end of
    a sentence (eos). A period, question mark, or exclamation mark indicate the
    end of a sentence in many, but not all, contexts. A single new line character
    does not mark the end of a sentence, but if two consecutive new lines occur,
    it will be assumed that the previous line has ended. This method returns
    a tuple of two values. The first is a boolean which is True when the indexed
    character marks the end of a sentence. The second is the next index. This is
    necessary because "..." does not necessarily mark the end of a sentence.
    Returning the next index helps to skip over such punctuation. Eg.
        eos, index = is_eos("I think... perhaps", 7, 18)
        #eos is False and index is 10)
    """
    if (index >= length): return (True, index)   # Don't overrun end of file.

    if (is_pqx(text, index, length)):

      # Check for periods in abbreviations, such as 'U.S.A.'
      # The first two periods cannot be end of sentence.
      if (alpha_immediately_after(text, index, length)): return (False, index + 1)
      what, new_index = what_follows(text, index, length)
      if (what == LINE_BREAK): return (True, new_index)
      if (what == UC_LETTER):
        if (initial_precedes(text, index, length)): return (False, new_index)
        if (known_abbreviation(text, index, length)): return (False, new_index)
        return (True, new_index)
      if (what == END_QUOTE or what == END_BRACKET):
        what, new_index = what_follows(text, new_index, length)
        if (what == UC_LETTER):
          return (True, new_index)
        return (False, new_index)

    elif (text[index] < " "):
      return blank_line_or_ff(text, index, length)

    return (False, index + 1)

def find_end_of_sentence(text, start_index, length):
    """Searches for the end of a sentence, starting from start_index.
    Return -1 if length of the text is exceeded.
    """
    if (start_index >= length): return -1
    end_of_sentence, i = is_eos(text, start_index, length)
    while (not end_of_sentence):
        # is_eos increments the index
        end_of_sentence, i = is_eos(text, i, length)
        if (i >= length): break
    return i

def count_alpha(text):
    """Count alphabetic characters."""
    num_alpha = 0
    for c in text:
      if c.isalpha(): num_alpha += 1
    return num_alpha

def read_file(file_name):
    """Reads in the entire utf-8 text file and returns it as a string."""

    if os.path.exists(file_name):   # If there is a file.
        with open(file_name, encoding='utf-8') as fp:
            all_of_it = fp.read()
            return all_of_it
    else:
        print("Unknown file: {}".format(file_name))
        sys.exit(0)

def split_text(the_text):
    """Splits the text. Return an array of sentences."""

    index = 0
    length = len(the_text)
    all_sentences = []
    while(index < length):
        index_punctuation = find_end_of_sentence(the_text, index, length)
        if (index_punctuation == -1): break
        sentence = the_text[index: index_punctuation].strip()
        if (len(sentence) > 0):
          if count_alpha(sentence) > 0:
            all_sentences.append(sentence)
        index = index_punctuation
    return all_sentences

# ----------------------------------------------------
# Program runs from here.

if __name__ == '__main__':

    major = sys.version_info.major
    minor = sys.version_info.minor
    if major < 3:
        print("Hakilo requires Python 3. Your version is {}.{}.".format(major, minor))
        sys.exit(0)

    if (len(sys.argv) < 2):      # If no parameters.
        print(HOW_TO_USE)
        sys.exit(0)

    the_text = read_file(sys.argv[1])  # Read in file.
    result = split_text(the_text)
    for sentence in result:
        print(sentence)
    print("Original size of file: {}".format(len(the_text)))
    print("Number of sentences: {}".format(len(result)))

