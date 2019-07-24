# -*- coding: utf-8 -*-
# Create charts that show how similarity metrics perform as books change.

import utils
import graphUtils
import numpy as np
import scipy.stats as stats
import scipy.spatial.distance as dist
import re
import random

#from getWordCounts import loadWCData
import mainParams as mp

from calcSimilarity import SIMILARITY_METRICS
from getWordCounts import loadTexts, loadWCData


# ==============================================================================
# ==============================================================================

NAME_CONVERSION = {
    "jensen-shannon": "Jensen-Shannon",
    "cosine": "Cosine",
    "canberra": "Canberra",
    "cityblock": "Manhattan",
    "burrowsdelta": "Burrows' Delta",
}

# Get the counts given the top words
def calculateCounts(book, countLength, wordToIndex):
    # initialize counts
    counts = np.zeros(countLength, dtype=np.int32)
    for t in book.tokens:
        if t in wordToIndex:
            counts[wordToIndex[t]] += 1
        else:
            counts[-1] += 1
    return counts

# calculate counts as we randomly swap words from one book to the next
def calculateIntermediateCounts(b1, b2, countLength, wordToIndex):
    b1Len = len(b1.tokens)
    b2Len = len(b2.tokens)
    if (b1Len != b2Len):
        raise Exception("Books have unequal length!")
    start = calculateCounts(b1, countLength, wordToIndex)
    end = calculateCounts(b2, countLength, wordToIndex)

    randomIndices = np.array(range(b1Len))
    np.random.shuffle(randomIndices)

    intermediates = []
    intermediates.append(start)
    current = start
    for i in range(b1Len):
        current = np.copy(current)

        # Replace token at index in book 1 with token at index in book 2
        index = randomIndices[i]
        t1 = b1.tokens[index]
        t2 = b2.tokens[index]

        # t1 is no longer in text
        if t1 in wordToIndex:
            current[wordToIndex[t1]] -= 1
        else:
            current[-1] -= 1

        # t2 now is in the text
        if t2 in wordToIndex:
            current[wordToIndex[t2]] += 1
        else:
            current[-1] += 1

        intermediates.append(current)

    return intermediates


# create the chart based on given info
def createChart(fname, saveDir, intermediateSets, precompSims, compSims, useRemainder, metricName, t1Counts, startTextName, endTextName):
    # get baseline info for our baseline text (Thucydides Peloponnesian War Book 1)
    if useRemainder:
        base = np.zeros(len(t1Counts))
        base[:-1] = t1Counts[:-1]
        base[-1] = np.sum(t1Counts[-1])
    else:
        # frequencies
        base = t1Counts[:-1]/(np.sum(t1Counts))

    y = []
    sum = np.zeros(len(intermediateSets[0]))
    boundries = []
    for j, intermediates in enumerate(intermediateSets):
        print(j, end=" ", flush=True)
        sims = []
        # for each point between thuc2, nonnus2
        for i, counts in enumerate(intermediates):
            # get count info for our comparison text (some hybrid between
            # Thucydides Peloponnesian War Book 1 and Nonnus Books 1-6)
            if useRemainder:
                compare = np.zeros(len(counts))
                compare[:-1] = counts[:-1]
                compare[-1] = np.sum(counts[-1])
            else:
                # frequencies
                compare = counts[:-1]/(np.sum(counts))

            b_data = [base, compare]
            b_target = [0, 1]
            a_names = ["Thucydides", "Hybrid"]
            b_names = ["PW1", "Chimera"]

            # compare thuc1 to these counts using the similarity metric
            similarity = compSims(precompSims(b_data))[0][1]
            sims.append(similarity)
            #print("%.5d %f" % (i, similarity))

        boundries = [
            (startTextName, sims[0]),
            (endTextName, sims[-1])
        ]
        name = "%s %d" % (metricName, j)
        y.append((name, sims))
        sum += np.array(sims)

    # Create chart using the different runs
    name = "%s (average across %d runs)" % (NAME_CONVERSION[metricName], len(intermediateSets))
    avg = sum/len(intermediateSets)
    all = y
    avgLine = [(name, avg)]
    graphUtils.metricIntuitionChart(avgLine, True, saveDir, fname, boundries=boundries, allLines=all)


# ==============================================================================
# ==============================================================================

# Main function to run comparison
def metricCapture():
    # Set random seed for deterministic behavior
    random.seed(mp.SEED)
    np.random.seed(mp.SEED)

    language = "Greek"
    textLocation = mp.languageInfo[language]["textLocation"]

    available = utils.getContent(textLocation + "available.json", True)

    # Only grab Thucydides and Nonnus texts
    newAvailable = []
    for i, o in enumerate(available):
        authorName = o["author"]
        if (authorName == "Thucydides" or authorName == "Nonnus"):
            newAvailable.append(o)

    mySaveDir = "output/greek/nonnusThucCompare/"
    utils.safeWrite(mySaveDir + "available.json", newAvailable, True)


    authors, books = loadTexts(-1, -1, mySaveDir, language, "")

    # Baseline comparison text and ending text are both PW book 1
    thuc1 = None
    thuc2 = None
    for b in books:
        if (b.textName == "The Peloponnesian War"):
            if (b.bookNumber == 1):
                thuc1 = b
                thuc2 = b
            # elif (b.bookNumber == 2):
            #     thuc2 = b


    thuc2Len = len(thuc2.tokens)

    # Create a fake book based on the same amount of Nonnus as in the thucydides book.
    raw = {
        "bookNumber": 1,
        "bookText": ""
    }
    nonnus1 = utils.Book(raw, "Test", "Nonnus")
    nonnus1.tokens = authors[0].allTokens[:thuc2Len]
    nonnus1.numTokens = len(nonnus1.tokens)

    # Print 2000th tokens for the paper
    print("2000th tokens:")
    print("Thucydides: %s" % thuc2.tokens[1999])
    print("Nonnus: %s" % nonnus1.tokens[1999])
    print("---")

    # comparing book 1 of Peloponnesian War to book 1 vs first 6 books of Nonnus' Dionysiaca
    books = [thuc1, thuc2, nonnus1]

    startTextName = "Nonnus Dionysiaca 1-6"
    endTextName = "Thucydides Peloponnesian War 1"


    # For each set of top words
    for top in mp.languageInfo[language]["tops"]:
        name, topWords, poetryWords, subsetSize, splitParameter, includeBooks, includeGraphs, _, wordToPOS = top
        if (topWords == 0 or subsetSize != -1 or splitParameter != -1):
            continue


        saveDirBase = mp.getSaveDir(language, mp.languageInfo, splitParameter)
        saveDir = saveDirBase + "%s/" % (name)

        # get top words from appropriate folder; if they don't exist, skip
        try:
            topWords = utils.getContent(saveDir + "topWords.txt", False).split(",")
        except:
            print("Failed to get top words for %s" % name)
            continue


        # Get information on all books for burrows delta calculations
        saveDirBase = mp.getSaveDir(language, mp.languageInfo, splitParameter)
        _, books, _ = loadWCData(saveDirBase, -1, name)


        # Each of top words plus remainder
        countLength = len(topWords) + 1

        # Index of each word
        wordToIndex = {}
        for i, w in enumerate(topWords):
            wordToIndex[w] = i


        # get counts of the top words for thuc1, thuc2, nonnus1
        t1Counts = calculateCounts(thuc1, countLength, wordToIndex)

        # get counts of top words for each intermediate step between thuc2, nonnus2
        intermediateSets = []
        for i in range(10):
            intermediates = calculateIntermediateCounts(nonnus1, thuc2, countLength, wordToIndex)
            intermediateSets.append(intermediates)


        saveDir += "nonnusThucCompare/"

        # for each sim metric
        for simInfo in SIMILARITY_METRICS:
            print("  %s" % simInfo["name"], end=" ")
            precompSims = simInfo["precompute"] # lambda x: x for most
            compSims = simInfo["compute"]
            useRemainder = simInfo["useRemainder"]

            fname = "metric_%s" % simInfo["name"]
            createChart(fname, saveDir, intermediateSets, precompSims, compSims, useRemainder, simInfo["name"], t1Counts, startTextName, endTextName)

            print("")

        # for burrows' delta, normalize based on all data in addition to just
        # the two texts
        for simInfo in SIMILARITY_METRICS:
            if simInfo["name"] != "burrowsdelta":
                continue

            useRemainder = simInfo["useRemainder"]

            print("  %s (full)" % simInfo["name"], end=" ")



            all_books = []
            for book in books:
                if (book.numTokens >= mp.MIN_TOKENS_NECESSARY):
                    if useRemainder:
                        base = np.zeros(len(book.counts))
                        base[:-1] = book.counts[:-1]
                        base[-1] = np.sum(book.counts[-1])
                    else:
                        base = book.counts[:-1]/(np.sum(book.counts))
                    all_books.append(base)
            all_books = np.array(all_books)


            full_std = np.std(all_books, axis=0)
            # if any of these values are equal to 0, that means all
            # associated values are 0, so instead of dividing by 0, divide by 1
            # (std == 0) has 1s where the value is 0
            full_std = full_std + (full_std == 0)
            full_mean = np.mean(all_books, axis=0)

            # Define our own calculation functions using full data
            precompSims = lambda d: (d - full_mean)/full_std
            compSims = lambda d: 1 - (1/len(d[0]))*dist.squareform(dist.pdist(d, 'cityblock'))


            fname = "metric_%s_full_norm" % simInfo["name"]

            createChart(fname, saveDir, intermediateSets, precompSims, compSims, useRemainder, simInfo["name"], t1Counts, startTextName, endTextName)
            print("")

if __name__ == "__main__":
    metricCapture()
