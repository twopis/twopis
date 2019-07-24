# Run tests showing how grouping words look across multiple runs

import mainParams as mp
from getWordCounts import loadWCData

from groupWords import groupAndPlotWords, groupWordsMultipleRuns, getWordGroupsRange, getWordGroupsRangeTest
from makeBasicGraphs import getTokenColorMapMultiRun


def makeCharts(baseSaveDir, topWords, topName):
    baseSaveDir += "textsOnlyTopWords/"

    for numGroups in getWordGroupsRangeTest(len(topWords)):
        print("    %d groups..." % numGroups)
        saveDir = "%s%d_group/" % (baseSaveDir, numGroups)

        # get comparison of grouping across multiple runs
        getTokenColorMapMultiRun(saveDir, topWords, topName)



# ===========================================================
# ===================== Run Everything ======================
# ===========================================================


# Load texts and run the multiple runs
def wordGroupTests(dataSplit, top, wordToPOS, saveDirBase):
    topName, _, _ = top
    authors, books, topWords = loadWCData(saveDirBase, dataSplit, topName)

    # calculate save directory based on input parameters
    saveDir = saveDirBase + "%s/" % (topName)

    normalGroups = getWordGroupsRange(len(topWords))
    testGroups = getWordGroupsRangeTest(len(topWords))

    # For new groups, we have to do an initial run for them.
    newGroups = []
    for g in testGroups:
        if not(g in normalGroups):
            newGroups.append(g)
    groupAndPlotWords(topName, topWords, wordToPOS, saveDir, groupings=newGroups)


    # Compare multiple additional runs of grouping words
    groupWordsMultipleRuns(topName, topWords, saveDir)

    # Compare multiple additional runs of grouping words
    makeCharts(saveDir, topWords, topName)

if __name__ == "__main__":
    for top in mp.tops:
        name, topWords, poetryWords, subsetSize, splitParameter, includeBooks, includeGraphs, _, wordToPOS = top
        newTop = (name, topWords, poetryWords)
        saveDir = mp.getSaveDir(mp.language, mp.languageInfo, splitParameter)

        wordGroupTests(splitParameter, newTop, wordToPOS, saveDir)
        print("======================")
