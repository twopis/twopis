# -*- coding: utf-8 -*-
# Group words into individual categories
import utils
import graphUtils
import numpy as np

from sklearn import cluster

from getWordCounts import loadWCData
import mainParams as mp

# ==============================================================================
# ==============================================================================

GROUP_SEED = 301 # This is my office number

# Group range for full run
GROUPS_SMALLEST = 9#3
GROUPS_LARGEST = 9#12

# Group range for analyzing grouping.
GROUPS_SMALLEST_TEST = 3
GROUPS_LARGEST_TEST = 12

# kelly colors of maximum contrast
KELLY_COLORS = [
    (253, 253, 253), #fdfdfd,
    (29, 29, 29), #1d1d1d,
    (235, 206, 43), #ebce2b, -1
    (112, 44, 140), #702c8c,
    (219, 105, 23), #db6917,
    (150, 205, 230), #96cde6,
    (186, 28, 48), #ba1c30,
    (192, 189, 127), #c0bd7f,
    (127, 126, 128), #7f7e80,
    (95, 166, 65), #5fa641,
    (212, 133, 178), #d485b2,
    (66, 119, 182), #4277b6, - 10
    (223, 132, 97), #df8461,
    (70, 51, 151), #463397,
    (225, 161, 26), #e1a11a,
    (145, 33, 140), #91218c,
    (232, 233, 72), #e8e948,
    (126, 21, 16), #7e1510,
    (146, 174, 49), #92ae31,
    (111, 52, 13), #6f340d,
    (211, 43, 30), #d32b1e,
    (43, 53, 20), #2b3514 - 20
]

# Number of runs of the sorting algorithm to compare
RUNS = 20

# Get ranges to run full analysis for
def getWordGroupsRange(numWords):
    start = GROUPS_SMALLEST
    end = min(GROUPS_LARGEST+1, numWords)
    groups = [-1]
    groups.extend(list(range(start, end)))
    return groups


# Get range to run grouping analysis on
def getWordGroupsRangeTest(numWords):
    start = GROUPS_SMALLEST_TEST
    end = min(GROUPS_LARGEST_TEST+1, numWords)
    groups = list(range(start, end))
    return groups

# Group words and generate a tSNE plot for them
def groupAndPlotWords(topName, topWords, wordToPOS, baseSaveDir, groupings=None):
    fname = baseSaveDir + "wordCountData/wordCountByText_%s.json" % (topName)
    rawCounts = np.array(utils.getContent(fname, True))
    tokensByItem = np.sum(rawCounts, axis=0)
    data = rawCounts/tokensByItem


    baseSaveDir = baseSaveDir + "textsOnlyTopWords/"


    if (groupings == None):
        groupings = getWordGroupsRange(len(topWords))
    #print(data)

    # cluster data
    for numGroups in groupings:
        startOffset = 1

        if (numGroups == -1):
            saveDir = "%spos_group/" % (baseSaveDir)
            print("    calculating for part of speech groups")

            wordLabels = []
            for word in topWords:
                if not(word in wordToPOS):
                    raise Exception("Word %s not in part of speech dictionary" % word)
                wordLabels.append(wordToPOS[word])
        else:
            saveDir = "%s%d_group/" % (baseSaveDir, numGroups)
            print("    calculating for %d groups" % numGroups)
            # Make deterministic using group seed
            kmeans = cluster.KMeans(n_clusters=numGroups, n_init=10000, random_state=GROUP_SEED)
            kmeans.fit(data)
            wordLabels = kmeans.labels_

        # rename groups and keep track of color associated with each word
        labelsSeen = 0
        labelConversion = {}
        target = []
        firstWords = []
        colorsUsed = []
        for i in range(len(topWords)):
            if not(wordLabels[i] in labelConversion):
                labelConversion[wordLabels[i]] = labelsSeen
                labelsSeen += 1
                firstWords.append(topWords[i])
            label = labelConversion[wordLabels[i]]
            target.append(label)
            colorsUsed.append(KELLY_COLORS[startOffset+label])

        # save used colors
        fname = "%s/colorByIndex.json" % (saveDir)
        utils.safeWrite(fname, colorsUsed, True)

        # create labels
        targetLabels = []
        for i in range(numGroups):
            targetLabels.append("Group %d (%s)" % (i+1, firstWords[i]))

        # group data and colors
        targetList = []
        targetList.append({
            "name": "Word_Groupings_",
            "target": np.array(target),
            "labels": targetLabels
        })

        dataSet = graphUtils.Dataset(data, targetList)

        # Save group labels
        groupLabels = firstWords
        if (numGroups == -1):
            origGroupLabels = ["noun", "verb", "adj", "adv", "pron", "article", "prep", "conj", "partic"]
            groupLabels = ["", "", "", "", "", "", "", "", ""]
            for i in range(len(origGroupLabels)):
                groupLabels[labelConversion[str(i)]] = origGroupLabels[i]

        utils.safeWrite(saveDir + "groupLabels.json", groupLabels, True)

        # graph the data
        tSNEDir = saveDir + "tSNE/"
        colors = KELLY_COLORS[startOffset:startOffset+numGroups]
        for u in [False]: # [False, True]:
            graphUtils.tSNE_2D(dataSet, topWords, 20.0, True, tSNEDir, True, predefinedColors=colors, verbose=False, useUMAP=u)

# Run the grouping algorithm multiple times to show how stable it is.
def groupWordsMultipleRuns(topName, topWords, baseSaveDir):
    fname = baseSaveDir + "wordCountData/wordCountByText_%s.json" % (topName)
    rawCounts = np.array(utils.getContent(fname, True))
    tokensByItem = np.sum(rawCounts, axis=0)
    data = rawCounts/tokensByItem

    baseSaveDir = baseSaveDir + "textsOnlyTopWords/"

    # cluster data
    for numGroups in getWordGroupsRangeTest(len(topWords)):


        fname = "%s%d_group/colorByIndex.json" % (baseSaveDir, numGroups)
        baseColorsRaw = utils.getContent(fname, True)

        baseColors = []
        colorIndices = {}
        indexToColor = {}
        indexToColorName = [
            "Black",
            "Yellow",
            "Purple",
            "Orange",
            "Blue",
            "Red",
            "Tan",
            "Gray",
            "Green"
        ]
        numColors = 0

        labelToIndicesBase = {}

        for i, c in enumerate(baseColorsRaw):
            colorString = "%d,%d,%d" % (c[0], c[1], c[2])
            baseColors.append(colorString)

            if not(colorString in colorIndices):
                colorIndices[colorString] = numColors
                indexToColor[numColors] = colorString
                numColors += 1

                labelToIndicesBase[colorString] = [i]
            else:
                labelToIndicesBase[colorString].append(i)


        saveDir = "%s%d_group/extra_runs/" % (baseSaveDir, numGroups)
        print("      calculating extra for %.2d groups..." % numGroups, end=" ", flush=True)

        # we already ran the 0th run
        for run in range(1, RUNS):
            print(run, end=" ", flush=True)
            startOffset = 1
            # Make deterministic using group seed
            # 10000
            kmeans = cluster.KMeans(n_clusters=numGroups, n_init=1000, random_state=GROUP_SEED+run)
            kmeans.fit(data)
            wordLabels = kmeans.labels_

            # rename groups and keep track of color associated with each word


            # get the indices for each label
            labelToIndices = {}
            maxLabel = -1
            for i in range(len(topWords)):
                label = wordLabels[i]
                if label in labelToIndices:
                    labelToIndices[label].append(i)
                else:
                    labelToIndices[label] = [i]

                if label > maxLabel:
                    maxLabel = label


            # store colors used already
            takenColors = {}

            # this will convert from label to color
            labelToColor = {}


            # store labels already assigned
            takenLabels = {}
            unassignedColors = []

            # Go through each color in original grouping, assign it to the
            # group in this grouping that most closely matches it.
            for i in range(maxLabel+1):
                labelCounts = np.full((numColors), 0)
                for j in labelToIndicesBase[indexToColor[i]]:
                    labelCounts[wordLabels[j]] += 1

                # find colors with highest overlap
                bestLabels = np.flipud(np.argsort(labelCounts))
                #print(labelCounts)
                #print(bestLabels)
                for j in bestLabels:
                    # If there an no longer any matches
                    if (labelCounts[j] == 0):
                        # print("No valid label for color %s" % indexToColorName[i])
                        unassignedColors.append(i)
                        break

                    # print("trying to assign color %s to best label %d" % (indexToColorName[i], j))
                    if not(j in takenLabels):
                        splt = indexToColor[i].split(",")
                        labelToColor[j] = (int(splt[0]), int(splt[1]), int(splt[2]))
                        takenLabels[j] = True
                        #print(labelToIndices[j])
                        break

                # print("---")

            # assing labels that aren't taken
            for i in range(maxLabel+1):
                # ignore taken colors
                if i in labelToColor:
                    continue
                freeColorIndex = unassignedColors[0]
                splt = indexToColor[freeColorIndex].split(",")
                labelToColor[i] = (int(splt[0]), int(splt[1]), int(splt[2]))
                unassignedColors = unassignedColors[1:]
            # print("========")



            colorsUsed = []
            for i in range(len(topWords)):
                colorsUsed.append(labelToColor[wordLabels[i]])

            # save used colors
            fname = "%s/groups_%.3d.json" % (saveDir, run)
            utils.safeWrite(fname, colorsUsed, True)

        print("")

# ===========================================================
# ===================== Run Everything ======================
# ===========================================================

# load texts and save the word count info
def groupWords(dataSplit, top, wordToPOS, saveDirBase):
    topName, _, _ = top
    authors, books, topWords = loadWCData(saveDirBase, dataSplit, topName)

    # calculate save directory based on input parameters
    saveDir = saveDirBase + "%s/" % (topName)

    groupAndPlotWords(topName, topWords, wordToPOS, saveDir)

if __name__ == "__main__":
    for top in mp.tops:
        name, topWords, poetryWords, subsetSize, splitParameter, includeBooks, includeGraphs, _, wordToPOS = top
        newTop = (name, topWords, poetryWords)
        saveDir = mp.getSaveDir(mp.language, mp.languageInfo, splitParameter)

        groupWords(splitParameter, newTop, wordToPOS, saveDir)
        print("======================")
