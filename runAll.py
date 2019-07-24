# -*- coding: utf-8 -*-
# Run all parts of the pipeline
import subprocess
import random
import numpy as np

from getWordCounts import getWordCounts
from calcSimilarity import calculateSimilarity
from groupWords import groupWords
from makeBasicGraphs import basicGraphs, normalizedGraphs
from predictCategories import predictCategories
from printKeyWords import printKeyWords
from metricCapture import metricCapture
from gatherFiles import gatherFiles, gatherFilesFull
from wordGroupTests import wordGroupTests
import mainParams as mp


for language in ["Greek", "English", "Icelandic"]:
    print("Language: %s" % language)
    textLocation = mp.languageInfo[language]["textLocation"]
    tops = mp.languageInfo[language]["tops"]

    for top in tops:
        # Set random seed for deterministic behavior
        random.seed(mp.SEED)
        np.random.seed(mp.SEED)

        name, topWords, poetryWords, subsetSize, splitParameter, includeBooks, includeGraphs, compSimOptions, wordToPOS = top
        print("%s (subset: %d, split: %d)" % (name, subsetSize, splitParameter))
        newTop = (name, topWords, poetryWords)

        saveDir = mp.getSaveDir(language, mp.languageInfo, splitParameter)

        print("  Getting word counts...")
        getWordCounts(splitParameter, newTop, subsetSize, textLocation, language, mp.addPoetry, saveDir)
        print("====================================")
        print("====================================")
        print("  Calculating similarities...")
        calculateSimilarity(splitParameter, newTop, subsetSize, compSimOptions, mp.addPoetry, includeBooks, saveDir)
        print("====================================")
        print("====================================")

        if includeGraphs:
            print("Grouping Similar Words...")
            groupWords(splitParameter, newTop, wordToPOS, saveDir)
            print("====================================")
            print("====================================")
            print("Creating basic graphs...")
            basicGraphs(splitParameter, newTop, saveDir)
            print("Creating normalized graphs...")
            normalizedGraphs(splitParameter, newTop, saveDir)
            print("====================================")
            print("====================================")
            print("Predicting Categories...")
            predictCategories(splitParameter, newTop, saveDir)
            print("====================================")
            print("====================================")
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


# Get additional charts for metric usage
print("====================================")
print("====================================")
print("Gathering additional metric stats...")
metricCapture()

# Move Files
print("====================================")
print("====================================")
print("Moving Files...")

#gatherFiles(mp.topStr, mp.topNum, mp.comparableTopStr, mp.comparableTopNum, mp.poetryNum)
gatherFilesFull(mp.topStr, mp.topNum, mp.comparableTopStr, mp.comparableTopNum, mp.poetryNum)

print("========================================================================")
print("========================================================================")
print("========================================================================")
print("========================================================================")
