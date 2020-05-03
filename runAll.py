# -*- coding: utf-8 -*-
# Run all parts of the pipeline
import subprocess
import random
import numpy as np

from getWordCounts import getWordCountInfo, getWordCounts
from calcTopWordOverlap import calcTopWordOverlapOverTime
from calcSimilarity import calculateSimilarity
from groupWords import groupWords
from makeBasicGraphs import basicGraphs
from predictCategories import predictCategories
from printKeyWords import printKeyWords
from gatherFiles import gatherFilesFull
from wordGroupTests import wordGroupTests
import mainParams as mp

USE_TEXT_COUNTS = False

for language in ["Greek", "English", "Icelandic"]:
    print("Language: %s" % language)
    textLocation = mp.languageInfo[language]["textLocation"]
    tops = mp.languageInfo[language]["tops"]

    # Precomputation to save computing time: since all currently used options
    # have a subsetSize and splitParamter of -1, we can calculate this info once
    # and use it many times.
    authors, books, tokenInfo, poetryTokenInfo = getWordCountInfo(-1, -1, language, USE_TEXT_COUNTS)

    print("Getting top word overlap over time info...")
    calcTopWordOverlapOverTime(language)

    for top in tops:
        # Set random seed for deterministic behavior
        random.seed(mp.SEED)
        np.random.seed(mp.SEED)

        name, topWords, poetryWords, subsetSize, splitParameter, includeBooks, includeGraphs, compSimOptions, wordToPOS = top
        print("%s (subset: %d, split: %d)" % (name, subsetSize, splitParameter))
        newTop = (name, topWords, poetryWords)

        saveDir = mp.getSaveDir(language, mp.languageInfo, splitParameter)

        print("  Getting word counts...")
        getWordCounts(authors, books, tokenInfo, poetryTokenInfo, newTop, language, saveDir)
        print("====================================")
        print("====================================")
        print("  Calculating similarities...")
        calculateSimilarity(splitParameter, newTop, subsetSize, compSimOptions, includeBooks, saveDir)
        print("====================================")
        print("====================================")

        if includeGraphs:
            print("Grouping Similar Words...")
            groupWords(splitParameter, newTop, wordToPOS, saveDir)
            print("====================================")
            print("====================================")
            print("Creating basic graphs...")
            basicGraphs(splitParameter, newTop, saveDir)
            print("====================================")
            print("====================================")
            print("Predicting Categories...")
            predictCategories(splitParameter, newTop, saveDir)
            print("====================================")
            print("====================================")

            if not(USE_TEXT_COUNTS):
                # Words in context doesn't make sense when we are using only
                # the word count per book.
                print("Getting Word Lists...")
                printKeyWords(splitParameter, newTop, subsetSize, language, saveDir)

            # This is a massive calculation that should only be done for the
            # one set we care about.
            if (mp.RUN_EVERYTHING and poetryWords > 0):
                print("====================================")
                print("====================================")
                print("Extra Word Group Info...")
                wordGroupTests(splitParameter, newTop, wordToPOS, saveDir)

        print("********************************************")
        print("********************************************")

# Move Files
print("====================================")
print("====================================")
print("Moving Files...")

gatherFilesFull(mp.topStr, mp.topNum, mp.comparableTopStr, mp.comparableTopNum, mp.poetryNum)

print("========================================================================")
print("========================================================================")
print("========================================================================")
print("========================================================================")
