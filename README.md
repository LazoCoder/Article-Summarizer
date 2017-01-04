# Article-Summarizer
Uses frequency analysis to assign scores to sentences. Sentences that are rich with relevant words will have higher scores. The highest scoring sentences are then printed in chronological order to produce a summary.

## Sample Summaries

The following are all summaries of articles. If any of the links are dead, the content of each article can be found in the folder "sample_articles". These articles are all randomly selected and do not represent my opinions, views or what news websites I follow.

### [How Apple Alienated Mac Loyalists](https://www.bloomberg.com/news/articles/2016-12-20/how-apple-alienated-mac-loyalists)
Interviews with people familiar with Apple's inner workings reveal that the Mac is getting far less attention than it once did. People now have more options. There is now just one team, and most of the engineers are iOS first, giving the people working on the iPhone and iPad more power. In recent years, Apple managers have also become more likely to float two or more competing ideas, meaning designers and engineers must work on more than one concept at a time.

### [Inside the Eye](http://ngm.nationalgeographic.com/2016/02/evolution-of-eyes-text)
There are eyes with bifocal lenses, eyes with mirrors, and eyes that look up, down, and sideways all at the same time. Cup-shaped eyes with more receptors or compound eyes with additional cups can produce crude images of objects. This explains why animals don’t have eyes that are better than they need and why they lose eyes so readily if they no longer need them. Ultimately, to understand why they are the way they are, we need to know how they are used.

### [Solar Now Produces a Better Energy Return on Investment Than Oil](https://robertscribbler.com/2016/12/19/solar-now-produces-a-better-energy-return-on-investment-than-oil/)
In 2016, according to a trends analysis based on this report by the Royal Society of London, the energy return on energy investment (EROEI) for oil appears to have fallen below a ratio of 15 to 1 globally. Meanwhile, according to a new study by the Imperial College of London, solar energy’s return on investment ratio as of 2015 was 14 to 1 and rising. The higher energy returns for solar come as module efficiency, supply chain efficiency, and production and installation efficiency are all on the rise. Higher energy return on investment ratios for solar is one of the primary drivers enabling such low overall power prices.

## Usage
```

    Usage:
        main.py <article.txt> <summary length>

    Explanation:
        Parameter 1: the location and name of the text to summarize
        Parameter 2: the number of sentences for the summary to contain

```

## The Algorithm
1. Extract all the sentences from the text.
 1. Remove all the newlines (“\n”) from the text.
 2. Remove periods from all multi-period abbreviations.
    - Example: change “Y.M.C.A.” to “YMCA” but leave single-period abbreviations like “Dr.” and “Mr.” alone.
    - This reduces ambiguities and code complexity when it must be known if a period marks the end of a sentence.
 3. Split the text into sentences by dividing it in the locations where there are periods.
 4. Make sure no sentence has been incorrectly split in two due to abbreviations such as “Dr.”, “Mr.”, etc….
 5. Perform some more clean up such as whitespace removal and grouping words within quotes together.
2. Extract all the words from the text.
 1. Split the text into words by dividing it in the locations where there is whitespace (“ “).
 2. Trim words that have punctuation around it (“cat!” should be changed to “cat”).
 3. Group words that are technically the same (such as “berries” and “berry”).
 4. For each word, remove ownership (“schools’” and “school’s” should be changed to “school”).
 5. Convert plural words to singular.
3. Assign a score to each word.
 1. Word scores are based on their frequency in the text.
 2. Ignore common words such as “the”, “to”, “and”, etc….
4. Assign a score to each sentence.
 1. The sentence score is the sum of all the scores of its words divided by the number of words.
 2. Sentences with high information density will have high scores.
5. Put the sentences with the highest scores together in chronological order to produce the summary.

# Tools
While each module serves a function and contributes to the overall algorithm, they are also designed to work independently to serve their own particular function by themselves. For example, “extractor.py” is used by the Summarizer to extract sentences and words from text, but it can also be used independently to see exactly what it extracts. This is useful for debugging as it allows one to test each individual component separately.

## extractor.py
This is used to extract sentences and words from text. It can be used to check if the sentences are being divided up correctly. It can also provide info about the text such as the sentence and word count.

```

    Usage:
        extractor.py <article.txt> [parameter]

    Parameters:
        -i --info       display basic info about <article.txt>
        -s --sentences  extract sentences from <article.txt>
        -w --words      extract words from <article.txt>

```

Example:

```

$ python3.5 extractor.py "sample_articles/apple.txt" -i
Sentence count:     78
Word count:       1592

```

## parser.py
This module is used to manipulate words and sentences.

```

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

```

Example:

```

$ python3.5 parser.py berries -s
berry

```

## scoring.py
This module is used for scoring the words and sentences.

```

    Usage:
        scoring.py <article.txt> <parameter> <quantity>

    Parameters:
        -s      print the top scoring sentences
        -w      print the top scoring words

```

Example:

```

Example:
$ python3.5 scoring.py "sample_articles/apple.txt" -w 5
Rank: Score: Content:  
  #1. 35.0   apple     
  #2. 24.0   mac       
  #3. 17.0   with      
  #4. 15.0   company   
  #5. 15.0   more  

```

## tool.py
This module was used to create the abbreviation lists that are referenced in the algorithm so it is not part of the algorithm itself.

```

    Usage:
        tools.py [--options]

    Options:
        --create_abbr           create abbreviations.txt from words.txt
        --create_abbr_multi     create abbreviations_multi.txt from words.txt

```
