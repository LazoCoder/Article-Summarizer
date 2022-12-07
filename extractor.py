# Tool to extract sentences & words from a file.

from sys import argv
import ASparser


def get_sentences(file_name):
    # Extract sentences from a text file.
    reader = open(file_name, "r",encoding='utf-8')
    sentences = reader.read()
    reader.close()
    sentences = sentences.replace("\n", "")
    sentences = ASparser.convert_abbreviations(sentences)
    sentences = sentences.replace("?", ".")
    sentences = sentences.replace("!", ".")
    sentences = sentences.split(".")
    sentences = ASparser.fix_broken_sentences(sentences)
    sentences = ASparser.remove_whitespace_list(sentences)
    sentences = ASparser.remove_blanks(sentences)
    sentences = ASparser.add_periods(sentences)
    sentences = ASparser.clean_up_quotes(sentences)
    sentences = ASparser.group_quotes(sentences)
    sentences = ASparser.comma_handler(sentences)
    return sentences


def get_words(file_name):
    # Extract words from a text file. Clean the words by removing surrounding
    # punctuation and whitespace, and convert the word to singular.
    reader = open(file_name, "r",encoding='utf-8')
    words = reader.read()
    reader.close()
    words = words.replace("\n", " ")
    words = ASparser.convert_abbreviations(words)
    words = words.split(" ")
    words = ASparser.remove_blanks(words)
    for i in range(0, len(words)):
        words[i] = ASparser.clean(words[i])
    return words


def print_usage():
    # Print how to run the tool and use the parameters.
    print('''
    Usage:
        extractor.py <article.txt> [parameter]

    Parameters:
        -i --info       display basic info about <article.txt>
        -s --sentences  extract sentences from <article.txt>
        -w --words      extract words from <article.txt>
    ''')


def handle_arguments():
    # Handle the command line arguments.
    if argv[2] == "-i" or argv[2] == "--info":
        print("Sentence count: %6d" % len(get_sentences(argv[1])))
        print("Word count:     %6d" % len(get_words(argv[1])))
    elif argv[2] == "-s" or argv[2] == "--sentences":
        sentences = get_sentences(argv[1])
        for sentence in sentences:
            print(sentence)
    elif argv[2] == "-w" or argv[2] == "--words":
        words = get_words(argv[1])
        for word in words:
            print(word)
    else:
        print_usage()


if __name__ == "__main__":
    if len(argv) == 3:
        handle_arguments()
    else:
        print_usage()
