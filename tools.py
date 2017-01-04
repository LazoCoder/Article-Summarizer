# A set of tools for debugging and creating Summarizer.

from sys import argv


def create_abbreviations():
    # Create the file abbreviations.txt.
    # Each abbreviation contains one period only, example: Mr. Mrs. Dr.
    reader = open("word_lists/words.txt")
    writer = open("word_lists/abbreviations.txt", "w")
    for line in reader:
        line = line[:-1]
        if line.endswith(".") and line.count(".") == 1:
            writer.write(line)
            writer.write("\n")
    reader.close()
    writer.close()


def create_abbreviations_multi():
    # Create the file abbreviations_multi.txt.
    # Each abbreviation contains multiple periods only, example: Y.M.C.A
    reader = open("word_lists/words.txt")
    writer = open("word_lists/abbreviations_multi.txt", "w")
    for line in reader:
        line = line[:-1]
        if line.endswith(".") and line.count(".") != 1:
            writer.write(line)
            writer.write("\n")
    reader.close()
    writer.close()


def print_usage():
    # Display the parameters.
    print('''
    Usage:
        tools.py [--options]

    Options:
        --create_abbr           create abbreviations.txt from words.txt
        --create_abbr_multi     create abbreviations_multi.txt from words.txt
    ''')


def handle_arguments():
    # Handle the command line arguments.
    if argv[1] == "--create_abbr":
        create_abbreviations()
    elif argv[1] == "--create_abbr_multi":
        create_abbreviations_multi()
    else:
        print_usage()


if __name__ == "__main__":
    if len(argv) == 2:
        handle_arguments()
    else:
        print_usage()
