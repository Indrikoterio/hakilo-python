# Hakilo - For splitting a text into sentences, and sentences into words.

Hakilo (meaning 'axe' in Esperanto) chops a text into sentences for analysis.

Sentences usually end with a period, a question mark, or an exclamation mark,
but not every period indicates the end of a sentence. For example:

&nbsp;&nbsp;&nbsp;&nbsp;Mrs. C. Bisset is 1.6 meters tall.

The above sentence has four periods, but only the last ends the sentence.

If there is an end quote mark or an end bracket after a period, the sentence will include the end mark. For example:

&nbsp;&nbsp;&nbsp;&nbsp;The tactical officer said, "Shields are down to 30 percent."

The last character of the above sentence is a quote mark.

When the program encounters a blank line, or any vertical space, it treats this as the end of a sentence.

Lines with a length of 0, and lines without any alphabetic characters, are excluded from output. Thus the line:

&nbsp;&nbsp;&nbsp;&nbsp;\- 2.7

will not be included in the output.

## Requirements

Hakilo was developed and tested on Python 3.7 .

## Links

Github: [https://github.com/Indrikoterio/hakilo-python](https://github.com/Indrikoterio/hakilo-python)

PyPi: [https://pypi.org/project/hakilo/1.1.1/](https://pypi.org/project/hakilo/1.1.1/)

## Installation

Try this:

```
$ python3 -m pip install hakilo
```

## Usage

### Importing

```
import hakilo
```

### read_file

This utility function reads in the entire file as a UTF-8 string.

```
the_text = hakilo.read_file("frankenstein.txt")
```

### split_text

This function splits the text and returns a list of sentences.

```
sentences = hakilo.split_text(the_text)
```

### split_sentence

This function splits the sentence into words and punctuation.

```
words = hakilo.split_sentence("You can do better.")
```

## Developer

Hakilo was developed by Cleve (Klivo) Lendon.

## Contact

To contact the developer, send email to indriko@yahoo.com . Preferred languages
are English and Esperanto. Comments, suggestions and criticism are welcomed.

## History

First release, October 2020.

Version 1.1.0 - Added split_sentence() - October 2020.

Version 1.1.1 - Fix bug in split_sentence() - October 2020.

## License

Hakilo is free software. It is distributed free of charge, without conditions, and without guarantees. You may use, modify and distribute it as you wish. There is no need to ask for permission. If you use Hakilo's code in your own project, and publish it, I request only that you acknowledge the source.
