# Tool to count and score sentences and words.

import parser
import extractor
from sys import argv


def get_word_scores(all_words):
    # Return a dictionary where the key is the word and the value is its count.
    file = open("word_lists/words_to_ignore.txt")
    words_to_ignore = file.read().split("\n")
    file.close()
    dictionary = {}
    for word in all_words:
        if word in words_to_ignore:
            continue
        count = 1
        if word in dictionary:
            count += dictionary.get(word)
        temp = {word: count}
        dictionary.update(temp)
    return dictionary


def score(sentence, word_scores):
    # The scoring algorithm.
    denominator = 1.0
    score = 0.0
    words = sentence.split(" ")
    for word in words:
        if word not in word_scores:
            continue
        if sentence.count(word) == 1:
            denominator += 1.0
        word = parser.clean(word)
        score += word_scores.get(word)
    return score/denominator


def get_sentence_scores_dict(all_sentences, word_scores):
    # Return a dictionary where the key is the sentence and he value is its score.
    dictionary = {}
    for sentence in all_sentences:
        temp = {sentence: score(sentence, word_scores)}
        dictionary.update(temp)
    return dictionary


def get_sentence_scores_list(all_sentences, word_scores):
    # Return a list with the scores in the same order as the sentences.
    scores = []
    for sentence in all_sentences:
        scores.append(score(sentence, word_scores))
    return scores


def sort_dictionary(dictionary):
    # Sort the words from a dictionary in ascending order.
    sorted_ascending = sorted(dictionary, key=dictionary.__getitem__)
    sorted_descending = []
    for item in sorted_ascending:
        sorted_descending.insert(0, item)
    return sorted_descending


def print_popular(dictionary, sorted_items, top=10):
    # Print the most popular content in a dictionary, based on the order of sorted_items.
    if top >= len(sorted_items):
        top = len(sorted_items) - 1

    print("%-5s %-6s %-10s" % ("Rank:", "Score:", "Content:"))
    for i in range(0, top):
        word = sorted_items[i]
        count = dictionary.get(word)
        print("%5s %-6.1f %-10s" % ("#"+str(i+1)+".", count, word))


def x_highest_score(sentence_scores, x):
    # Find the xth highest score.
    list = []
    for score in sentence_scores:
        list.append(score)
    list.sort()
    return list[-x]


def top_sentences(all_sentences, sentence_scores, threshold):
    # Return the sentences chronologically which have equal to or above a certain score.
    result = []
    for i in range(0, len(all_sentences)):
        if sentence_scores[i] >= threshold:
            result.append(all_sentences[i])
    return result


def print_usage():
    # Print how to run the tool and use the parameters.
    print('''
    Usage:
        scoring.py <article.txt> <parameter> <quantity>

    Parameters:
        -s      print the top scoring sentences
        -w      print the top scoring words
    ''')


def handle_arguments():
    # Handle the command line arguments.
    if not argv[3].isdigit():
        print("The quantity parameter must be an integer.")
        return

    file = argv[1]
    parameter = argv[2]
    quantity = int(argv[3])

    if parameter != '-s' and parameter != '-w':
        print_usage()
        return

    words = extractor.get_words(file)
    words_scores = get_word_scores(words)
    sentences = extractor.get_sentences(file)
    sentences_scores = get_sentence_scores_dict(sentences, words_scores)

    if parameter == '-s':
        if quantity > len(sentences):
            print("Quantity specified is greater than the number of sentences.")
        else:
            print_popular(sentences_scores, sort_dictionary(sentences_scores), quantity)
    else:
        if quantity > len(words):
            print("Quantity specified is greater than the number of words.")
        else:
            print_popular(words_scores, sort_dictionary(words_scores), quantity)


if __name__ == '__main__':
    if len(argv) == 4:
        handle_arguments()
    else:
        print_usage()
