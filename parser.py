# Tool to trim and manipulate words and sentences.

from sys import argv


def comma_handler(sentences):
    # If a sentence starts with a comma it is probably part of the sentence before it.
    new_list = []
    skip = False
    for i in range(0, len(sentences)):
        if skip:
            skip = False
            continue
        if i+1 < len(sentences) and sentences[i+1][0] == ",":
            new_list.append(sentences[i] + sentences[i+1])
            skip = True
        else:
            new_list.append(sentences[i])
    return new_list


def group_quotes(sentences):
    # Quotes should be in a single sentence, even if there are periods in the quote.
    new_list = []
    skip = 0
    for i in range(0, len(sentences)):
        if skip > 0:
            skip -= 1
            continue
        sentence = sentences[i]
        while sentence.count("\"") % 2 == 1:
            skip += 1
            if i+skip >= len(sentences):
                break
            if sentences[i+skip][0].isalnum():
                sentence += " " + sentences[i+skip]
            else:
                sentence += sentences[i+skip]
        new_list.append(sentence)
    return new_list


def clean_up_quotes(sentences):
    # If a quotation follows a period, make sure it is in the same sentence.
    generified = []
    for sentence in sentences:  # Convert fancy quotes to generic quotes.
        sentence = sentence.replace('“', '\"')
        sentence = sentence.replace('”', '\"')
        generified.append(sentence)

    new_list = [generified[0]]
    for i in range(1, len(generified)):
        sentence = generified[i]
        isolated_quotation = generified[i][0] == "\"" and generified[i][1] == " "
        quotation_with_period = generified[i][0] == "\"" and generified[i][1] == "."
        if isolated_quotation and quotation_with_period:
            sentence = sentence[2:]
            new_list[-1] += "\""
        new_list.append(sentence)
    return new_list


def add_periods(sentences):
    # Add a period to each element in the list.
    new_list = []
    for sentence in sentences:
        new_list.append(sentence + ".")
    return new_list


def remove_blanks(sentences):
    # Remove all empty elements.
    new_list = []
    for sentence in sentences:
        if sentence != "":
            new_list.append(sentence)
    return new_list


def fix_broken_sentences(sentences):
    # Combine sentences in a list where periods from abbreviations where
    # mistaken for the end of a sentence.
    file = open("word_lists/abbreviations.txt")
    abbreviations = str(file.read()).split("\n")
    file.close()

    new_list = []
    flag = False
    for i in range(0, len(sentences)):
        if flag:
            flag = False
            continue

        last_word = sentences[i].split(" ")[-1]
        last_word = remove_punctuation(last_word)
        last_word = to_singular(last_word)
        last_word = remove_punctuation(last_word)
        last_word += "."

        new_list.append(sentences[i])
        for abbreviation in abbreviations:
            if abbreviation == last_word:
                new_list[-1] += "." + sentences[i+1]
                flag = True
                break
    return new_list


def convert_abbreviations(string):
    # Remove all periods in all multi period abbreviations. Example: Y.M.C.A -> YMCA
    file = open("word_lists/abbreviations_multi.txt")
    abbreviations = str(file.read()).split("\n")
    file.close()
    new_string = string
    abbreviations_in_string = []

    # Get all the abbreviations that are in the string.
    for abbreviation in abbreviations:
        if abbreviation in string:
            abbreviations_in_string.append(abbreviation)

    # Sort the abbreviations from longest to shortest.
    # Some abbreviations overlap so its important to check the longest ones first.
    # Example: "Y.M.C.A." contains "M.C." and "C.A." and "Y.M.C.A". If the "C.A."
    # is handled first then it becomes "Y.M.CA", which is incorrect.
    abbreviations_in_string.sort(key=str.__len__)
    abbreviations_in_string.reverse()

    for abbreviation in abbreviations_in_string:
        if abbreviation in new_string:
            new_string = str(new_string).replace(abbreviation, abbreviation.replace(".", ""))
    return new_string


def clean(word):
    # Remove punctuation from a word and convert it to lowercase singular.
    new_word = remove_punctuation(word)
    new_word = to_singular(new_word)
    new_word = remove_punctuation(new_word)
    new_word = str(new_word).lower()
    return new_word


def to_singular(word):
    # Convert a plural word to singular, otherwise return the original word.
    new_word = word
    if word.endswith("'s") or word.endswith("s'"):
        new_word = word[:-2]
    elif word.endswith("ies"):
        new_word = word[:-3] + "y"
    return new_word


def remove_punctuation(word):
    # Remove non alphabetic & non numeric letters on either side of a word.
    new_word = word
    while new_word is not "" and not str(new_word)[0].isalnum():
        new_word = new_word[1:]
    while new_word is not "" and not str(new_word)[-1].isalnum():
        new_word = new_word[:-1]
    return new_word


def remove_whitespace_list(sentences):
    # Remove whitespace on either side of each sentence in a list.
    new_list = []
    for sentence in sentences:
        new_list.append(remove_whitespace(sentence))
    return new_list


def remove_whitespace(word):
    # Remove whitespace on either side of the a word.
    new_word = word
    while new_word is not "" and str(new_word).startswith(" "):
        new_word = new_word[1:]
    while new_word is not "" and str(new_word).endswith(" "):
        new_word = new_word[:-1]
    return new_word


def print_usage():
    # Display the parameters.
    print('''
    Usage:
        parser.py <word> [--parameter]
        parser.py <sentence> [--parameter]

    Parameters for <word>:
        -a --abbreviation   remove all periods from an abbreviation
        -s --singular       convert most words to singular and remove ownership
        -p --punctuation    remove the surrounding punctuation
        -w --whitespace     remove the surrounding whitespace

    Parameters for <sentence>:
        -a --abbreviation   remove all periods from an abbreviation
    ''')


def word_parameter():
    # Handles the logic for when the user inputs two parameters where the first is a word.
    if argv[2] == "-a" or argv[2] == "--abbreviation":
        print(str(argv[1]).replace(".", ""))
    elif argv[2] == "-s" or argv[2] == "--singular":
        print(to_singular(argv[1]))
    elif argv[2] == "-p" or argv[2] == "--punctuation":
        print(remove_punctuation(argv[1]))
    elif argv[2] == "-w" or argv[2] == "--whitespace":
        print(remove_whitespace(argv[1]))
    else:
        print_usage()


def sentence_parameter():
    # Handles the logic for when a user inputs two parameters where the first is a sentence.
    if argv[2] == "-a" or argv[2] == "--abbreviation":
        print(convert_abbreviations(argv[1]))
    else:
        print_usage()


def handle_two_parameters():
    if str(remove_whitespace(argv[1])).count(" ") == 0:
        word_parameter()
    else:
        sentence_parameter()


if __name__ == "__main__":
    if len(argv) == 3:
        handle_two_parameters()
    else:
        print_usage()
