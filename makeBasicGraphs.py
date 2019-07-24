# -*- coding: utf-8 -*-
import re
import copy
import bisect

from PIL import Image, ImageDraw, ImageFont
import numpy as np

import utils
import graphUtils
import mainParams as mp
import genre
from getWordCounts import loadWCData, wordPCAFitTransform
from groupWords import getWordGroupsRange
from calcSimilarity import centDiff

# ==============================================================================
# ==============================================================================

# Visualize information about the items with scatter plots
#   data: The list of features for the books
#   target: the labels for the books
#   authornames: names for the items
#   authornames: names for each author
#   typeName: Books or Authors
#   saveDir: place to save data
def visualizeItemData(data, target, names, authornames, typeName, saveDir):
    targetList = []
    targetList.append({
        "name": "",
        "target": np.array(target),
        "labels": []
    })

    # go through all grouping options
    for fun in genre.labelList:
        targetList.append(fun(authornames))

    # visualize author data
    dataSet = graphUtils.Dataset(np.array(data), targetList)

    # Dummy test data
    testSet = graphUtils.Dataset([], [])
    testNames = []
    saveOutput = True
    oneThree = False

    pcaDir = "pca/"

    # Do PCA
    for includeNames in [True, False]:
        try:
            graphUtils.pca2Viz(dataSet, names, includeNames, saveOutput, saveDir + pcaDir, oneThree)
        except IndexError:
            print("Could not run visualization of PCA for 2: not enough dimensions in PCA.")
        if (False):
            try:
                graphUtils.pca3Viz(dataSet, names, includeNames, False     , saveDir + pcaDir)
            except IndexError:
                print("Could not run visualization of PCA for 3: not enough dimensions in PCA.")
        try:
            graphUtils.pca4Viz(dataSet, names, includeNames, saveOutput, saveDir + pcaDir)
        except IndexError:
            print("Could not run visualization of PCA for 4: not enough dimensions in PCA.")

    perplexity = 20.0


    baseSaveDir = saveDir
    # I have some state carrying over that I can't figure out, so only one of
    # these can run at a time, but umap results look roughly the same as tSNE.
    for u in [False]:
        algorithmName = "tSNE"
        if u:
            algorithmName = "umap"
        print("Visualizing using %s" % algorithmName)

        tSNEDir = baseSaveDir + algorithmName + "/"


        graphUtils.tSNE_2D(dataSet, names, perplexity, saveOutput, tSNEDir, True, useUMAP=u)

        if (typeName == "Authors"):
            #graphUtils.tSNE_2D_2color(dataSet, names, perplexity, saveOutput, tSNEDir, True)

            # load tsne data
            saveDir = tSNEDir
            precalcFilename = saveDir + ("%s_2D_data.txt" % algorithmName)

            precalculated = utils.getContent(precalcFilename, True)
            tsneX = np.array(precalculated["x"], dtype=np.float64)

            # skip first and last target
            dataSet = graphUtils.Dataset(tsneX, targetList[1:-1])

            graphUtils.tSNE_2D_4Up(dataSet, names, False, saveOutput, saveDir, "info_no_labels_4Up", False, useUMAP=u)

        # Create fourup containing books
        if (typeName == "Books"):
            saveDir = tSNEDir
            precalcFilename = saveDir + ("%s_2D_data.txt" % algorithmName)

            precalculated = utils.getContent(precalcFilename, True)
            tsneX = np.array(precalculated["x"], dtype=np.float64)
            preY = np.array(precalculated["y"], dtype=np.float64)
            names = precalculated["names"]

            #print("Precalculateds loaded")

            targets = []
            targets.append({"name":"_", "target":preY!=30, "labels":["Demosthenes", "Others"]}) # Demosthenes
            targets.append({"name":"_", "target":preY!=55, "labels":["Isocrates", "Others"]}) # Isocrates
            targets.append({"name":"_", "target":preY!=91, "labels":["Xenophon", "Others"]}) # Xenophon
            targets.append({"name":"_", "target":preY!=76, "labels":["Plato", "Others"]}) # Plato
            #targets.append(genre.labelList[]())

            dataSet = graphUtils.Dataset(tsneX, targets)

            #graphUtils.clickable_tSNE_2D(dataSet, names, -1, saveDir, False)
            graphUtils.tSNE_2D_4Up(dataSet, names, True, saveOutput, saveDir, "outliers4Up", False, useUMAP=u)

# ===========================================================
# ============== Normalize Features By Category =============
# ===========================================================

# Normalize features by genre
def normalizeFeatures(authors, books, norm):
    groupConvert = genre.toGenre
    groupLabels = genre.genreLabels

    zeroOutFeatures = False;

    ## ---

    if (zeroOutFeatures):
        gConvert2 = genre.toGenrePlaysBM

    # make a mask based on the indices given in norm
    dims = authors[0].unNormalizedFeatureData.shape[0]
    normMask = np.zeros(dims)
    for i in norm:
        normMask[i] = 1

    if (zeroOutFeatures):
        # for zeroing out all features that don't match certain criteria
        specialGroupNorm = np.zeros(dims)

    # create norms for each group
    groupNorms = []
    for i, l in enumerate(groupLabels):
        groupNorms.append({
            "sum": np.zeros(dims),
            "num": 0
        })

    # add each author's info to the proper group
    for i, a in enumerate(authors):
        if (a.authorName[-2:] == "_2"):
            aName = a.authorName[:-2]
        else:
            aName = a.authorName

        group = groupConvert(aName)
        if (zeroOutFeatures):
            isBM = gConvert2(aName) == 3

        gN = groupNorms[group]
        gN["sum"] = gN["sum"] + a.unNormalizedFeatureData
        gN["num"] = gN["num"] + 1
        if (zeroOutFeatures and isBM):
            specialGroupNorm = specialGroupNorm + a.unNormalizedFeatureData

    if (zeroOutFeatures):
        specialGroupMask = np.sign(specialGroupNorm)

    # determine mean for each group
    for i, l in enumerate(groupLabels):
        gN = groupNorms[i]
        gN["final"] = (gN["sum"]/gN["num"])*normMask


    # normalize authors and books
    for a in authors:
        group = groupConvert(a.authorName)
        a.featureData = (a.unNormalizedFeatureData - groupNorms[group]["final"])

        if (zeroOutFeatures):
            a.featureData = a.featureData*specialGroupMask

    for b in books:
        group = groupConvert(b.author)
        b.featureData = (b.unNormalizedFeatureData - groupNorms[group]["final"])

        if (zeroOutFeatures):
            a.featureData = a.featureData*specialGroupMask


# ===========================================================
# =============== Store the frequency results ===============
# ===========================================================

def storeFreqResults(authors, books, saveDir, topWords):
    # store frequencies
    authorOutput = []
    for author in authors:
        authorOutput.append(author.authorName + "," + ",".join(map(str, author.featureData)))

    utils.safeWrite(saveDir+"authorFreqs.txt", "\n".join(authorOutput))

    bookOutput = []
    for book in books:
        if (book.numTokens >= mp.MIN_TOKENS_NECESSARY):
            bookOutput.append(book.getShortName() + "," + ",".join(map(str, book.featureData)))

    utils.safeWrite(saveDir+"bookFreqs.txt", "\n".join(bookOutput))

    utils.safeWrite(saveDir+"topWords.txt", ",".join(topWords))

# ===========================================================
# ============= Compare different author groups =============
# ===========================================================

# Create histograms comparing frequencies between different authors.
def histogramComparison(authors, books, saveDir, topWords):
    groupList = genre.namesToDialect;
    groupConversion = genre.toDialect#genre.toGenre#genre.toGenrePlaysBM#
    dataLabels = genre.dialectLabels#genre.genrePlaysBMLabels#genre.genreLabels

    groupData = {}

    for name in groupList:
        group = groupConversion(name)
        if not(group in groupData):
            groupData[group] = []

    # authorOutput = []
    for author in authors:
        authGroup = groupConversion(author.authorName)
        groupData[authGroup].append(author.featureData[:-1]);


    data = []
    dataErr = []
    for group in groupData:
        gList = np.array(groupData[group])
        data.append(np.mean(gList, axis=0))
        dataErr.append(np.std(gList, axis=0))


    saveDir = saveDir + "Authors/"

    graphUtils.comparisonHistogram(data, dataErr, dataLabels, topWords, "Comparison of Frequencies", "Freqs", saveDir, "topWordHistogram", True)

# get information for comparing key authors
def getKeyAuthorData(authors, books):
    groupList = genre.namesToGenre
    groupConversion = genre.toGenre
    baseDataLabels = genre.genreLabels

    groupData = {}

    for name in groupList:
        group = groupConversion(name)
        if not(group in groupData):
            groupData[group] = []

    authSets = [
        [1, "ApolloniusRhodius", "Homer", "Pindar"],
        #[1, "ApolloniusRhodius", "QuintusSmyrnaeus", "Pindar"],
        [0, "AeliusAristides", "Demosthenes", "Aristotle"],
        #[0, "ClementOfAlexandria", "JohnOfDamascus", "Aristotle"],
        #[0, "Arrian", "Thucydides", "Polybius"],
        [0, "Appian", "Thucydides", "Polybius"],
        [0, "Aristotle", "Pindar", "Homer"]
    ]
    res = []
    for auths in authSets:
        genr = auths[0]
        a1 = auths[1]
        a2 = auths[2]
        a3 = auths[3]

        # Go through authors, adding them to their groups and
        # selecting our targets
        for author in authors:
            aName = author.authorName
            if (author.authorName[-2:] == "_2"):
                aName = author.authorName[:-2]

            if (aName == a1 or aName == a2 or aName == a3):
                groupData[aName] = [author.featureData]

            authGroup = groupConversion(aName)
            groupData[authGroup].append(author.featureData)

        data = []
        dataErr = []
        for group in [a1, a2, a3, genr]:
            gList = np.array(groupData[group])
            avg = np.mean(gList, axis=0)
            data.append(avg)
            dataErr.append(np.zeros(avg.shape))

        dataLabels = [
            a1,
            a2,
            a3,
            baseDataLabels[genr]
        ]
        chartFileName = "%s_%s" % (a1, a2)
        res.append((data, dataErr, dataLabels, chartFileName))
    return res



# graph key author comparison information
def keyAuthorComparison(authors, books, saveDir, topWords):
    keyAuthData = getKeyAuthorData(authors, books)
    saveDir = saveDir + "Authors/"
    for dat in keyAuthData:
        data, dataErr, dataLabels, chartFileName = dat
        chartFileName += "-Histogram"
        graphUtils.comparisonHistogram(data, dataErr, dataLabels, topWords, "Comparison of Frequencies", "Freqs", saveDir, chartFileName, True)


# graph comparison of key authors with information about word importance
def keyAuthorComparisonWithImportance(authors, books, baseSaveDir, splitParam, topWords):
    makeWordImportanceGraphs = False
    keyAuthData = getKeyAuthorData(authors, books)
    saveDir = baseSaveDir + "wordImportance/"
    allDiffLineData = {}
    allCumulDiffLineData = {}
    allRCumulDiffLineData = {}
    allPercentageLineData = {}



    # load diffs for plotting internal similarities
    allDiffsFilename = baseSaveDir + "dists/diffLists.json"
    allDiffs = utils.getContent(allDiffsFilename, True)

    # For each set of key authors, make necessary visaulizations
    for dat in keyAuthData:
        data, _, dataLabels, chartFileName = dat

        print("    %s..." % chartFileName)
        numWords = len(topWords)
        numTexts = len(dataLabels)
        tickLabels = topWords
        distsFilename = baseSaveDir + "dists/" + chartFileName + ".json"
        dists = utils.getContent(distsFilename, True)
        # dists = [
        #     {"name": "D1", "vals": (np.random.random((numWords))*1.5 - 0.5)},
        #     {"name": "D2", "vals": (np.random.random((numWords))*1.5 - 0.5)}
        # ]
        for d in dists:
            d["vals"] = np.array(d["vals"])

        if (makeWordImportanceGraphs):
            graphUtils.wordImportanceComparison(data, dataLabels, tickLabels, dists, saveDir + "unsorted/", chartFileName, True)

        # display versions sorted by each metric
        for d in dists:
            sortedSaveDir = saveDir + d["name"] + "-sorted/"
            fname = chartFileName
            sortedInds = np.array(list(map(lambda x: x[0], sorted(enumerate(d["vals"]), key=lambda x: x[1][0], reverse=True))))


            data1 = copy.deepcopy(data)
            tickLabels1 = copy.deepcopy(tickLabels)
            wordsUsed = len(topWords)
            # If the similarity metric includes remainder, we have to add it
            if (len(dists[0]["vals"]) == len(data[0]) + 1):
                newData = []
                for row in data1:
                    r = np.append(row, 1 - np.sum(row))
                    newData.append(r)
                data1 = newData

                tickLabels1.append("Remainder")
                wordsUsed += 1



            data2 = list(map(lambda x: np.array(x)[sortedInds], data1))
            tickLabels2 = np.array(tickLabels1)[sortedInds]
            dists2 = copy.deepcopy(dists)
            percentiles = []
            for d2 in dists2:
                d2["vals"] = np.copy(d2["vals"])[sortedInds]

            if (makeWordImportanceGraphs):
                graphUtils.wordImportanceComparison(data2, dataLabels, tickLabels2, dists2, sortedSaveDir, fname, True)

            # save all words
            if d["name"] == "Jensen-shannon":
                fname = saveDir + "keyWords/" + chartFileName + ".json"
                SimDiff = {}
                for i, val in enumerate(d["vals"][sortedInds]):
                    if (True):
                        SimDiff[tickLabels2[i]] = [i, val[1]]
                utils.safeWrite(fname, SimDiff, True)

            # Diff data
            trueDiffs = np.array(list(map(lambda x: x[0], d["vals"][sortedInds])))
            y = (chartFileName, trueDiffs)
            y_cumul = (chartFileName, np.cumsum(trueDiffs))
            linesToGraphDiff = [y]
            linesToGraphDiffCumul = [y_cumul]


            # store info for the chart with all authors
            if d["name"] in allDiffLineData:
                allDiffLineData[d["name"]].extend([y])
            else:
                allDiffLineData[d["name"]] = [y]
            if d["name"] in allCumulDiffLineData:
                allCumulDiffLineData[d["name"]].extend([y_cumul])
            else:
                allCumulDiffLineData[d["name"]] = [y_cumul]

            # dif percentile data
            percentiles = list(map(lambda x: x[1], d["vals"][sortedInds]))
            y = (chartFileName, percentiles)
            linesToGraphPct = [y]

            # store info for the chart with all authors
            if d["name"] in allPercentageLineData:
                allPercentageLineData[d["name"]].append(y)
            else:
                allPercentageLineData[d["name"]] = [y]

            if splitParam == -1:
                # get percentiles for internal consistency of second author
                author1 = dataLabels[0]
                author2 = dataLabels[1]

                authorInternalConsistencies = [
                    # ["split5", author1, "-split5"],
                    # ["split-2", author1, "-splitHalf"],

                    # ["split5", author2, "-split5"],
                    # ["split-2", author2, "-splitHalf"]
                ]

                # Gen information comparing consistencies within given authors.
                for aic in authorInternalConsistencies:
                    a2DiffsFilename = baseSaveDir.replace("no_split", aic[0]) + "dists/%s_%s_2.json" % (aic[1], aic[1])
                    if (utils.fileExists(a2DiffsFilename)):
                        a2Diffs = utils.getContent(a2DiffsFilename, True)
                        diffNums = None
                        for ad in allDiffs:
                            if ad["name"] == d["name"]:
                                diffNums = ad["allDiffs"]

                        a2RawDiffs = None
                        for ad in a2Diffs:
                            if ad["name"] == d["name"]:
                                a2RawDiffs = ad["vals"]

                        if (diffNums != None and a2RawDiffs != None):
                            # Add difference data
                            aicName = aic[1]+aic[2]
                            a2SortedInds = np.array(list(map(lambda x: int(x[0]), sorted(enumerate(a2RawDiffs), key=lambda x: x[1][0], reverse=True))))
                            trueDiffs = np.array(list(map(lambda x: x[0], np.array(a2RawDiffs)[a2SortedInds])))
                            y_diff = (aicName, trueDiffs)
                            y_diff_cumul = (aicName, np.cumsum(trueDiffs))
                            linesToGraphDiff.append(y_diff)
                            linesToGraphDiffCumul.append(y_diff_cumul)

                            # Add Percentile data
                            a2Percentiles = []
                            for rd in a2RawDiffs:
                                index = bisect.bisect_left(diffNums, rd[0])
                                a2Percentiles.append((100.0*index)/len(diffNums))

                            a2Percentiles = sorted(a2Percentiles, reverse=True)
                            y2 = (aicName, a2Percentiles)
                            linesToGraphPct.append(y2)
                    else:
                        print("File does not exist: \"%s\"" % a2DiffsFilename)

            # Create charts showing differences for various authors
            graphUtils.lineChart(range(wordsUsed), linesToGraphDiff, True, sortedSaveDir, chartFileName+"_diff-chart", yLim=None)#[-0.002, 0]
            graphUtils.lineChart(range(wordsUsed), linesToGraphDiffCumul, True, sortedSaveDir, chartFileName+"_diff-cumul-chart", yLim=None, yAdjust=1)#[-0.002, 0]
            #graphUtils.lineChart(range(wordsUsed), linesToGraphPct, True, sortedSaveDir, chartFileName+"_pct-chart")

            linesToGraphDiffRCumul = []
            for name, c in linesToGraphDiffCumul:
                name = name.replace("-split5", " Local Split")
                name = name.replace("-splitHalf", " Global Split")
                linesToGraphDiffRCumul.append((name, c[-1] - np.array(c)))

            if d["name"] in allRCumulDiffLineData:
                allRCumulDiffLineData[d["name"]].extend([linesToGraphDiffRCumul])
            else:
                allRCumulDiffLineData[d["name"]] = [linesToGraphDiffRCumul]
            graphUtils.lineChart(range(wordsUsed), linesToGraphDiffRCumul, True, sortedSaveDir, chartFileName+"_diff-r-cumul-chart", yLim=None, yAdjust=1)#[-0.002, 0]


    for d in dists:
        # 4-Up Chart for these authors
        sortedSaveDir = saveDir + d["name"] + "-sorted/"
        graphUtils.lineChart4Up(range(wordsUsed), allRCumulDiffLineData[d["name"]], True, sortedSaveDir, "4up-r-cumul", yLim=None, yAdjust=1)


    # Create graph charts for all data in a cloud
    graphTypes = [
        ("all-diffs", allDiffLineData, None, 0),
        ("all-diffs-cumul", allCumulDiffLineData, None, 1),
        #("all-pcts", allPercentageLineData, [0, 100], 0)
    ]
    alls = {}
    for graphType, lineList, yLim, adjust in graphTypes:
            medFilename = baseSaveDir + "dists/median-%s.json" % graphType
            med = utils.getContent(medFilename, True)

            alls[graphType] = {}
            for d in med:
                lineList[d["name"]].append(["Median", d["line"]])
                alls[graphType][d["name"]] = d["all"]

            for name in allPercentageLineData:
                sortedSaveDir = baseSaveDir + "wordImportance/" + name + "-sorted/"
                for log in [False]:#, True]:
                    print("  %s..." % graphType)
                    graphUtils.lineChart(range(wordsUsed), lineList[name], True, sortedSaveDir, graphType, yLim=yLim, log=log, yAdjust=adjust)
                    print("  %s cloud..." % graphType)
                    graphUtils.lineChart(range(wordsUsed), lineList[name], True, sortedSaveDir, graphType + "-cloud", yLim=yLim, allLines=alls[graphType][name], log=log, yAdjust=adjust)



    # Create chart showing ignored top words
    n = "Jensen-shannon"
    sortedSaveDir = baseSaveDir + "wordImportance/" + n + "-sorted/"

    # Cumulative
    data = allCumulDiffLineData[n]

    # Add lines
    res = []
    targetSim = -1
    for item in alls["all-diffs-cumul"][n]:
        name, c = item
        # "Aristotle_Pindar" in name or

        if ("AeliusAristides_Demosthenes" in name or
            "DioChrysostom_Plato" in name):
            res.append((name, "-", 1 + c[-1] - np.array(c)))

        # Lowest of our top authors
        if ("DioChrysostom_Plato" in name):
            targetSim = c[-1]

    # add median
    # for item in allCumulDiffLineData[n]:
    #     name, c = item
    #     if ("Median" in name):
    #         res.append((name, "-", 1 + c[-1] - np.array(c)))

    # Add line cloud
    resAll = []
    for item in alls["all-diffs-cumul"][n]:
        name, c = item
        if not("Hymns_Dionysus" in name or "Euclid" in name):
            n1, n2 = name.replace("Hymns_", "Hymns").split("_")
            n1 = n1.replace("Hymns", "Hymns_")
            n2 = n2.replace("Hymns", "Hymns_")
            centuryDiff = centDiff(genre.toCent(n1), genre.toCent(n2))
            #print("%s, %s: %d" % (n1, n2, centuryDiff))
            if (centuryDiff >= 4):
                # color top sims differently
                color = "k-"

                resAll.append((name, color, 1 + c[-1] - np.array(c)))

    # for name, c in data:
    #     y = c[-1] - np.array(c)
    #     res.append((name, y))

    #resAll = map(lambda n, c: (n, c[-1] - np.array(c)))
    graphUtils.compareWordUsageChart(res, True, sortedSaveDir, "ignoreBestWords", yLim=None, allLines=resAll)


# ===========================================================
# ================ View top words as pixels =================
# ===========================================================

# given an array, create an image for it and save it at fname
def imageFromRGBArray(arr, fname):
    width = 300
    height = int(np.ceil(len(arr)/width))

    # default to transparent
    im = Image.new("RGBA", (width, height), "#00000000")
    pixels = im.load()

    for i, rgb in enumerate(arr):
        x = i % width
        y = int(np.floor(i/width))
        pixels[x, y] = rgb

    utils.check_and_create_path(fname)
    im.save(fname)

# given an array of arrays, create an image for it and save it at fname
# where each array is separated by a single line
def imageFromRGBArrays(arrs, fname):
    gapWidth = 8
    width = 100
    height = 1
    for arr in arrs:
        height += int(np.ceil((len(arr) + gapWidth)/width))

    # default to transparent
    im = Image.new("RGBA", (width, height), "#00000000")
    pixels = im.load()

    trueIndex = 0;
    for arr in arrs:
        for i, rgb in enumerate(arr):
            x = trueIndex % width
            y = int(np.floor(trueIndex/width))
            pixels[x, y] = rgb
            trueIndex += 1
        trueIndex += gapWidth

    utils.check_and_create_path(fname)
    im.save(fname)

# given an array of colors, group the colors into bars
def barsFromRGBArray(arr, totalTokens, baseColors):
    countedTokens = 0
    colorCounts = {}

    for color in baseColors:
        str = "%d_%d_%d" % color
        colorCounts[str] = 0

    for c in arr:
        countedTokens += 1
        str = "%d_%d_%d" % c
        if str in colorCounts:
            colorCounts[str] += 1
        else:
            colorCounts[str] = 1

    counts = []
    for c in baseColors:
        str = "%d_%d_%d" % c
        counts.append(colorCounts[str]/totalTokens)

    #graphUtils.wordUseBarChart(counts, baseColors, fname)

    return counts


# generate color map and produce key
def getTokenColorMap(saveDir, topWords, topName):
    numTops = len(topWords)
    tokenMap = []

    usePrecomputed = True
    if (usePrecomputed):
        fname = "%scolorByIndex.json" % (saveDir)
        colors = utils.getContent(fname, True)
        for c in colors:
            tokenMap.append((c[0], c[1], c[2]))
    else:
        fname = "%s../wordCountData/wordPrincipalComponents_%d.json" % (saveDir, topName)
        components = np.array(utils.getContent(fname, True))
        skipFirst = 4
        minVals = np.min(wordPCAFitTransform(components), axis=0)
        valRange = np.max(wordPCAFitTransform(components), axis=0) - minVals
        normalizedComponents = np.round(255*np.clip((components - minVals)/valRange, 0, 1))

        for i in range(numTops):
            comps = normalizedComponents[i]
            rgb = (int(comps[0]), int(comps[1]), int(comps[2]))
            tokenMap.append(rgb)

    width = 400
    height = 20*numTops
    im = Image.new("RGB", (width, height), "#FFFFFF")
    # get drawing context
    d = ImageDraw.Draw(im)
    # get a font
    fnt = ImageFont.truetype('fonts/DejaVuSans.ttf', 16)

    includedColors = {}
    colorList = []

    for i in range(numTops):
        rgb = tokenMap[i]

        baseY = 20*i
        colorValuesText = "(%03d,%03d,%03d) " % rgb

        # keep track of each new color
        if not(colorValuesText in includedColors):
            includedColors[colorValuesText] = True
            colorList.append(rgb)

        text = colorValuesText + topWords[i]
        d.text((50,baseY+2), text, font=fnt, fill=(0, 0, 0))
        d.rectangle(((10, baseY+2), (40, baseY+18)), fill=rgb)


    fname = saveDir + "images/key.png"
    utils.check_and_create_path(fname)
    im.save(fname)

    return tokenMap, colorList



# compare grouping across multiple runs
def getTokenColorMapMultiRun(saveDir, topWords, topName):
    numTops = len(topWords)
    tokenMaps = []

    fnames = ["%scolorByIndex.json" % (saveDir)]

    for file in utils.listFiles("%sextra_runs/" % saveDir):
        fnames.append("%sextra_runs/%s" % (saveDir, file))

    for fname in fnames:
        colors = utils.getContent(fname, True)
        tokenMap = []
        for c in colors:
            tokenMap.append((c[0], c[1], c[2]))
        tokenMaps.append(tokenMap)

    text_end = 0
    rect_width = 12
    rect_margin_h = 5
    rect_height = 5
    rect_top = 1
    rect_bottom = 4

    width = text_end + len(tokenMaps)*(rect_margin_h + rect_width) + rect_margin_h

    height = rect_height*numTops + 5
    im = Image.new("RGB", (width, height), "#FFFFFF")
    # get drawing context
    d = ImageDraw.Draw(im)
    # get a font
    fnt = ImageFont.truetype('fonts/DejaVuSans.ttf', int(0.8*rect_height))

    includedColors = {}
    colorList = []

     # draw text labels
    for i in range(numTops):

        baseY = rect_height*i

        # text = topWords[i]
        # text_width, _ = d.textsize(text, font=fnt)
        #
        # d.text((text_end - text_width,baseY+rect_top), text, font=fnt, fill=(0, 0, 0))

        rect_right = text_end
        # draw groupings for this word
        for tm in tokenMaps:
            rgb = tm[i]
            rect_left = rect_right+rect_margin_h
            rect_right = rect_left + rect_width
            d.rectangle(((rect_left, baseY+rect_top), (rect_right, baseY+rect_bottom)), fill=rgb)




    fname = saveDir + "images/groupingCompare.png"
    utils.check_and_create_path(fname)
    im.save(fname)

# Create visualizations of author word groups and usage
def visualizeWordOrder(authors, books, baseSaveDir, topWords, topName):
    baseSaveDir += "textsOnlyTopWords/"


    for numGroups in getWordGroupsRange(len(topWords)):
        if (numGroups == -1):
            print("    part of speech groups...")
            saveDir = "%spos_group/" % (baseSaveDir)
        else:
            print("    %d groups..." % numGroups)
            saveDir = "%s%d_group/" % (baseSaveDir, numGroups)

        # generate color map
        tokenToColor, colorList = getTokenColorMap(saveDir, topWords, topName)

        maxHeight = 0
        bars = {}

        # Create visualizations of each individual word colored by its group.
        for author in authors:
            # get author tokens as a block
            fname = baseSaveDir + "lists/authors/" + author.getSaveName() + ".json"
            tokens = utils.getContent(fname, True)

            arr = []
            for t in tokens:
                arr.append(tokenToColor[t])

            counts = barsFromRGBArray(arr, author.totalTokenCount, colorList)
            bars[author.authorName] = counts
            mh = np.max(counts)
            if mh > maxHeight:
                maxHeight = mh

            # This is not used for the paper but is rather interesting, as it lets
            # you potentially *see* different books, and certainly lets you see
            # different word usage

            # fname = saveDir + "images/authors_in_order/" + author.getSaveName() + ".png"
            # imageFromRGBArray(arr, fname)
            #
            # # get author's tokens divided by book
            # bookTokensArr = []
            # for book in books:
            #     if book.author == author.authorName:
            #         fname = baseSaveDir + "lists/books/" + book.getSaveName() + ".json"
            #         tokens = utils.getContent(fname, True)
            #         bookArr = []
            #         for t in tokens:
            #             bookArr.append(tokenToColor[t])
            #         bookTokensArr.append(bookArr)
            #
            # fname = saveDir + "images/authors-divided/" + author.getSaveName() + ".png"
            # imageFromRGBArrays(bookTokensArr, fname)


        # Graph word use bar charts now that we know the maximum scale.
        yHeight = (np.ceil(maxHeight*100.0))/100.0
        groupLabels = utils.getContent(saveDir + "groupLabels.json", True)
        title = "Group Frequency"
        # for author in authors:
        #     fname = saveDir + "images/authors_bars/" + author.getSaveName()
        #     graphUtils.wordUseBarChart(bars[author.authorName], colorList, yHeight, groupLabels, title, fname)

        quadList = [
            ("demosthenesHomer", ["AeliusAristides", "Demosthenes", "ApolloniusRhodius", "Homer"]),
            ("clementThucydides", ["JohnOfDamascus", "ClementOfAlexandria", "Appian", "Thucydides"]),
        ]
        for saveName, quad in quadList:
            fname = saveDir + "images/" + saveName
            counts4 = []
            for authorName in quad:
                counts4.append(bars[authorName])
            graphUtils.wordUseBarChart4Up(counts4, colorList, yHeight, groupLabels, quad, fname)

        #octo = ["ApolloniusRhodius", "Homer", "AeliusAristides", "Demosthenes", "Appian", "Thucydides", "JohnOfDamascus", "ClementOfAlexandria"]
        octo = ["Homer", "ApolloniusRhodius", "Demosthenes", "AeliusAristides", "Thucydides", "Appian", "ClementOfAlexandria", "JohnOfDamascus"]

        fname = saveDir + "images/dhct"
        counts8 = []
        for authorName in octo:
            counts8.append(bars[authorName])
        graphUtils.wordUseBarChart8Up(counts8, colorList, yHeight, groupLabels, octo, fname)
        #utils.safeWrite(saveDir+ "textsOnlyTopWords/images/authors/" + author.getSaveName() + ".json", tokens, dumpJSON=True)


        # Group by author
        numGroups = len(colorList)
        groups = []
        for i in range(numGroups):
            groups.append([])
        for author in bars:
            for i in range(numGroups):
                groups[i].append([author, bars[author][i]])

        for i, group in enumerate(groups):
            groupName = groupLabels[i]
            g = sorted(group, key=lambda x: x[1], reverse=True)
            tickLabels = []
            data = []
            dataErr = []
            # for each author
            for a in g:
                tickLabels.append(a[0].replace("Anonymous", "Anon "))
                data.append(a[1])
                dataErr.append(0)

            fname = "byAuthor/%.2d_%s" % (i+1, groupName)
            graphUtils.authorWordUseHistogram(data, ["Freq"], tickLabels, "Word usage for group %s" % groupName, "Frequency", saveDir, fname, True, color=colorList[i])


    # for book in books:
    #     tokens = getContent(saveDir+ "books/" + book.getSaveName() + ".json", True)


# ===========================================================
# ======== Aggregate features and run sort/visualize ========
# ===========================================================

def createBasicGraphs(authors, books, saveDir):
    # ==== Calculate data info
    a_typeName = "Authors"
    b_typeName = "Books"

    # aggregate features for each author into one dataSet
    a_data = []
    a_target = []
    a_names = []
    for i in range(len(authors)):
        author = authors[i]
        a_data.append(author.featureData[:-1]) # final item is the count for all other words
        a_target.append(i)
        a_names.append(author.authorName)

    # set up map from author name to target index
    authorToIndex = {}

    for i in range(len(authors)):
        author = authors[i]
        if (author.authorName[-2:] != "_2"):
            authorToIndex[author.authorName] = i

    includeBooks = True#False#

    if (includeBooks):
        # aggregate features for each book
        b_data = []
        b_target = []
        b_names = []
        b_authornames = []
        count = 0
        for book in books:
            if (book.numTokens >= mp.MIN_TOKENS_NECESSARY):
                b_data.append(book.featureData[:-1]) # final item is the count for all other words
                b_target.append(authorToIndex[book.author])
                b_names.append(book.getShortName())
                #print("%d: %s" % (count, book.getShortName()))
                b_authornames.append(book.author)
                count += 1

    # ==== Print and visualize info

    print("Authors:")

    subDir = "%s%s/" % (saveDir, a_typeName)
    visualizeItemData(a_data, a_target, a_names, a_names, a_typeName, subDir)

    if (includeBooks):
        print("Books:")

        subDir = "%s%s/" % (saveDir, b_typeName)
        visualizeItemData(b_data, b_target, b_names, b_authornames, b_typeName, subDir)


# ===========================================================
# ===================== Run Everything ======================
# ===========================================================


# print out basic graphs based on frequency info, with data normalized
def normalizedGraphs(dataSplit, top, saveDirBase):
    topName, _, _ = top

    authors, books, topWords = loadWCData(saveDirBase, dataSplit, topName)
    normalizations = []
    # normalize nothing
    # normalizations.append({"name":"", "norm": []})
    # normalize everything
    normalizations.append({"name":"allNorm", "norm": range(len(topWords))})
    # normalize those in first 50 with non-overlapping error bars
    #normalizations.append({"name":"custNorm", "norm": [0, 2, 3, 4, 6, 7, 11, 13, 14, 15, 18, 27, 30, 32, 36, 38, 39]})
    for normIndex, norm in enumerate(normalizations):
        normalizeFeatures(authors, books, norm["norm"])

        # calculate save directory based on input parameters
        saveDir = saveDirBase

        if (norm["name"] != ""):
            saveDir += "%s_%s/" % (topName, norm["name"])
        else:
            saveDir += "%s/" % (topName)

        print("  Basic Graphs...")
        createBasicGraphs(authors, books, saveDir)


# print out basic graphs based on frequency info
def basicGraphs(dataSplit, top, saveDirBase):
    topName, _, _ = top

    authors, books, topWords = loadWCData(saveDirBase, dataSplit, topName)

    # calculate save directory based on input parameters
    saveDir = saveDirBase + "%s/" % (topName)

    storeFreqResults(authors, books, saveDir, topWords)

    print("  Histogram comparison...")
    histogramComparison(authors, books, saveDir, topWords)

    print("  Key author histograms...")
    keyAuthorComparison(authors, books, saveDir, topWords,)

    print("  Key author word importance...")
    keyAuthorComparisonWithImportance(authors, books, saveDir, dataSplit, topWords)

    print("  Basic Graphs...")
    createBasicGraphs(authors, books, saveDir)

    print("  Word Order Visualizer...")
    visualizeWordOrder(authors, books, saveDir, topWords, topName)

if __name__ == "__main__":
    for top in mp.tops:
        name, topWords, poetryWords, subsetSize, splitParameter, includeBooks, includeGraphs, _, wordToPOS = top
        newTop = (name, topWords, poetryWords)
        saveDir = mp.getSaveDir(mp.language, mp.languageInfo, splitParameter)

        basicGraphs(splitParameter, newTop, saveDir)
        print("======================")
