# -*- coding: utf-8 -*-
# Run similarity calculations for different similarity metrics.
import re
import copy
import random
import unicodedata
import math
import time

import numpy as np
import scipy.spatial.distance as dist
from scipy.stats import percentileofscore as percentile

import utils
import graphUtils
import mainParams as mp
import genre
from getWordCounts import loadWCData

# ==============================================================================
# ==============================================================================


# ============================================================
# ================== Similarity Calculation ==================
# ============================================================

# precompute distances for Jensen-Shannon
def precomputeJS(data):
    # calculate Jensen-Shannon similarity (Before the summation)
    divs = []
    # smoothing amount
    k = 1
    for p in range(len(data)):
        row = []
        smoothedCounts = data[p]+k
        pPieces = smoothedCounts/(np.sum(smoothedCounts))
        pLogPieces = np.log(smoothedCounts) - np.log(np.sum(smoothedCounts))
        for q in range(len(data)):
            smoothedCounts = data[q]+k
            qPieces = smoothedCounts/(np.sum(smoothedCounts))
            qLogPieces = np.log(smoothedCounts) - np.log(np.sum(smoothedCounts))

            mLogPieces = np.log(0.5*(pPieces+qPieces))
            leftPieces = pPieces*(pLogPieces-mLogPieces)
            rightPieces = qPieces*(qLogPieces-mLogPieces)
            pieces = 0.5*(leftPieces + rightPieces)
            row.append(pieces)
        divs.append(row)
    return np.array(divs)

# precompute for probability calculation
def precomputeProb(data):
    # calculate Probability of production
    glob = np.sum(data, axis=0) + 1 # add plus-one smoothing
    globSum = np.sum(glob)
    globalPieces = np.log(glob) - np.log(globSum)

    globalLogProbs = []
    for j in range(len(data)):
        glp = data[j]*globalPieces
        globalLogProbs.append(glp)

    probs = []
    for i in range(len(data)):
        row = []
        smoothedCounts = data[i]+1
        iPieces = np.log(smoothedCounts) - np.log(np.sum(smoothedCounts))
        for j in range(len(data)):
            # probability that i generates j
            prob = data[j]*iPieces
            row.append(prob)
        probs.append(row)

    return np.array(probs), np.array(globalLogProbs)

# default precomputation does nothing
def precomputeDefault(data):
    # Convert counts to frequencies
    d = np.array(data)
    d = np.swapaxes(d, 0, 1)/np.sum(d, axis=1)
    d = np.swapaxes(d, 0, 1)
    return d

# default precomputation does +1 smoothing
def precomputePlusOne(data):
    # Convert counts to frequencies
    d = np.array(data) + 1
    d = np.swapaxes(d, 0, 1)/np.sum(d, axis=1)
    d = np.swapaxes(d, 0, 1)
    return d


# remove a given index from each list in a set of data
def removeIndex(data, i):
    res = list(map(lambda x: [v for k, v in enumerate(x) if not(i == k)], data))
    return res

# compute cosine similarity
def compSimsCosine(data, ignoreIndex=-1):
    if not(ignoreIndex == -1):
        data = removeIndex(data, ignoreIndex)
    dists = dist.squareform(dist.pdist(data, 'cosine'))
    return 1 - dists

# compute canberra similarity
def compSimsCanberra(data, ignoreIndex=-1):
    if not(ignoreIndex == -1):
        data = removeIndex(data, ignoreIndex)
    norm = 1.0/len(data[0])
    dists = norm*dist.squareform(dist.pdist(data, 'canberra'))
    return 1 -dists

# compute cityblock similarity
def compSimsCityblock(data, ignoreIndex=-1):
    if not(ignoreIndex == -1):
        data = removeIndex(data, ignoreIndex)
    # In theory we should normalize by number of words but the distances here
    # are very small so we don't have to; since all values sum to 1, the
    # maximum distance can be 2 so to put things in the 0-1 range we
    # normalize by 0.5.
    norm = 0.5#(1.0/len(data[0]))
    dists = norm*dist.squareform(dist.pdist(data, 'cityblock'))
    return 1 - dists

# compute burrows delta
def compSimsBurrowsDelta(data, ignoreIndex=-1):
    if not(ignoreIndex == -1):
        data = removeIndex(data, ignoreIndex)

    # normalize data
    normed_data = np.array(data)
    std = np.std(normed_data, axis=0)

    # if any of these values are equal to 0, that means all
    # associated values are 0, so instead of dividing by 0, divide by 1
    # (std == 0) has 1s where the value is 0
    std = std + (std == 0)
    normed_data = (normed_data - np.mean(normed_data, axis=0))/std

    # do cityblock distance on normalized data
    norm = 1.0/len(data[0])

    # Look at manhattan distance for z-normalized data
    dists = norm*dist.squareform(dist.pdist(normed_data, 'cityblock'))
    return 1 - dists

# compute minmax similairty
def compSimsMinMax(data, ignoreIndex=-1):
    if not(ignoreIndex == -1):
        data = removeIndex(data, ignoreIndex)

    data = np.array(data)
    data_len = len(data)
    sims = np.zeros([data_len, data_len])

    for i in range(0, data_len):
        for j in range(i, data_len):
            if (i == j):
                sims[i, j] = 1
                continue

            max = np.sum(np.maximum(data[i], data[j]))
            min = np.sum(np.minimum(data[i], data[j]))
            if (max == 0):
                minmax = 0
            else:
                minmax = min/max

            sims[i, j] = minmax
            sims[j, i] = minmax
    return sims

# Compute Jensen-Shannon Similarity
def compSimsJS(precomp, ignoreIndex=-1):
    N = len(precomp)

    if ignoreIndex == -1:
        dists = np.sum(precomp, axis=2)
    else:
        inds = [i for i in range(precomp.shape[2]) if not(ignoreIndex == i)]
        dists = np.sum(precomp[:,:,inds], axis=2)

    return 1 - dists

# Compute probability of one author's distribution producing the other.
def compSimsProb(precomp, ignoreIndex=-1):
    probData, globalLogProbs = precomp


    inds = [i for i in range(probData.shape[2]) if not(ignoreIndex == i)]

    # Only identical up to 6 decimal places, which seems pretty decent
    glp = np.sum(globalLogProbs[:,inds], axis=1)
    mlp = np.sum(probData[:,:,inds], axis=2)
    sims = mlp - glp

    return sims


# ============================================================
# ===================== Data Calculation =====================
# ============================================================

# given a century integer, get a string representation
def centToString(cent):
    end = " CE"
    if (cent < 0):
        end = " BCE"
    cent = abs(cent)
    if (cent == 1):
        s = "1st"
    elif (cent == 2):
        s = "2nd"
    elif (cent == 3):
        s = "3rd"
    else:
        s = "%dth" % cent
    return s + " Century" + end

# get the difference between two century integers
def centDiff(cent1, cent2):
    diff = abs(cent1 - cent2)
    # difference between 1st and 1st bc is 1, not 2
    if (cent1*cent2 < 0):
        diff -= 1
    return diff

# get the string representation of a similarity
def getSimString(sim):
    c1 = genre.toCent(sim["1author"])
    c2 = genre.toCent(sim["2author"])
    cdiff = centDiff(c1, c2)
    return "%.6f - %s, %s (%d centuries apart)" % (sim["score"], sim["1"], sim["2"], cdiff)

# given a sim, extract a "century difference, similarity" pair
def extractCentDatapoint(s):
    c1 = genre.toCent(s["1author"])
    c2 = genre.toCent(s["2author"])
    sameGenre = genre.toGenre(s["1author"]) == genre.toGenre(s["2author"])
    cdiff = centDiff(c1, c2)
    if (sameGenre):
        cdiff -= 0.15
    else:
        cdiff += 0.15
    sim = s["score"]
    return [cdiff, sim]

# determine whether the text was written by Euclid or is the hymn to Dionysus,
# then return an appropriate indicator value (these sets of texts are a little
# unusual, so we want to visualize them).
def extractEuclidDionysus(s):
    isEuclid = s["1author"] == "Euclid" or s["2author"] == "Euclid"
    isHymnsDionysus = s["1author"] == "Anonymous(Hymns_Dionysus)" or s["2author"] == "Anonymous(Hymns_Dionysus)"
    if (isEuclid):
        return 2
    elif (isHymnsDionysus):
        return 3
    elif (genre.toGenre(s["1author"]) != genre.toGenre(s["2author"])):
        return 1 # different genres
    else:
        return 0

# sims: similarity info for books
# names: names for each book
# authornames: names for each author
# typeName: Books or Authors
# useBeta: true if we are looking at beta distribution info
def getSimilarityInfo(simMatrix, names, authornames, typeName, useBeta):
    #================ Gather info
    sims = []

    itemVsItemSims = []

    # get the comparison of each author to each other author
    for i in range(len(names)):
        # for each author/book, print their similarity to others
        itemSims = []
        for j in range(len(names)):
            uniq = (j > i)
            obj = {
                "score": simMatrix[i][j],
                "1": names[i],
                "2": names[j],
                "1author": authornames[i],
                "2author": authornames[j],
                "sameAuthor": (authornames[i] == authornames[j]),
                "sameItem": (i == j),
                "uniq": uniq
            }
            itemSims.append(obj)
            # add each pair to the list of sims only once
            if uniq:
                sims.append(obj)

        itemSims = sorted(itemSims, key=lambda x: x["score"], reverse=True)

        itemVsItemSims.append(itemSims)

    if useBeta:
        # get data for scatter of similarities by century difference and beta distribution fits
        raw_sims = np.array(list(map(lambda x: x["score"], sims)))
        raw_sims_da = np.array(list(map(lambda x: x["score"], filter(lambda x: not(x["sameAuthor"]), sims))))
        raw_sims_sa = np.array(list(map(lambda x: x["score"], filter(lambda x: x["sameAuthor"], sims))))

        # calculate beta distribution fits for the data
        a, b = utils.estimateBeta(raw_sims)

        # authors can only be the same if we are examining the book level
        if (typeName == "Books"):
            a_da, b_da = utils.estimateBeta(raw_sims_da)
            a_sa, b_sa = utils.estimateBeta(raw_sims_sa)
        else:
            a_da, b_da = -1, -1
            a_sa, b_sa = -1, -1

        # save information about the beta distributions fit to the data.
        betaParams = [
            [a, b],
            [a_da, b_da],
            [a_sa, b_sa]
        ]
    else:
        betaParams = []

    return itemVsItemSims, betaParams


# given a similarity matrix and a filter for books by the same author,
# get the parameters for the beta distributions fit to the data.
def getBooksBeta(simMatrix, sameAuthorFilter):
    #================ Gather info
    daFilter = 1 - sameAuthorFilter

    # remove comparisons between the same books
    saFilter = sameAuthorFilter - np.identity(sameAuthorFilter.shape[0])

    daSims = (simMatrix*daFilter).flatten()
    saSims = (simMatrix*saFilter).flatten()

    a_da, b_da = utils.estimateBeta(daSims)
    a_sa, b_sa = utils.estimateBeta(saSims)

    betaParams = [
        [0, 0],
        [a_da, b_da],
        [a_sa, b_sa]
    ]

    return betaParams

# given item vs item similarities and parameters for the beta distributions
# fitting books by same and different authors, add information about
# the probability that each sim is one of these types
def calculateTypeProbs(itemVsItemSims, betaParams):
    _, beta_diff, beta_same = betaParams
    a_da, b_da = beta_diff
    a_sa, b_sa = beta_same

    # if there are dummy params, just return dummy values
    if (a_da == -1):
        for i, itemGroup in enumerate(itemVsItemSims):
            for j, item in enumerate(itemGroup):
                item["same_prob"] = math.nan
                item["diff_prob"] = math.nan
                item["sd_ratio"] = "---"
                item["sd_logratio"] = "---"
                item["ratiotext"] = "---"
        return itemVsItemSims


    # do some minor score adjustment
    N = len(itemVsItemSims)
    sims = np.zeros((N, N))
    for i, itemGroup in enumerate(itemVsItemSims):
        for j, item in enumerate(itemGroup):
            score = item["score"]
            if (score == 1):
                score = 0.99
            sims[i][j] = score

    same_probs = utils.getBetaProb(sims, a_sa, b_sa)
    diff_probs = utils.getBetaProb(sims, a_da, b_da)

    for i, itemGroup in enumerate(itemVsItemSims):
        for j, item in enumerate(itemGroup):
            score = item["score"]
            if score == 1:
                same_prob = math.nan
                diff_prob = math.nan
                ratioStr = "---"
                logRatioStr = "---"
                ratioText = "---"
            else:
                same_prob = same_probs[i][j] # utils.getBetaProb(score, a_sa, b_sa)
                diff_prob = diff_probs[i][j] # utils.getBetaProb(score, a_da, b_da)
                ratio = same_prob/diff_prob
                ratioStr = "%.4f" % ratio
                logRatioStr = "%.4f" % np.log(ratio)
                ratioText = "%.2f/%.2f" % (same_prob, diff_prob)
            item["same_prob"] = same_prob
            item["diff_prob"] = diff_prob
            item["sd_ratio"] = ratioStr
            item["sd_logratio"] = logRatioStr
            item["ratiotext"] = ratioText

    return itemVsItemSims

# flatten item v item similarities into a single list
# If symmetric is false, include all that don't compare the same item
# If symmetric is true, include each pair only once.
def flattenIVI(ivi, symmetric=True):
    newSims = []
    for itemGroup in ivi:
        newSims.extend(itemGroup)
    if symmetric:
        sims = list(filter(lambda x: x["uniq"], newSims))
    else:
        sims =  list(filter(lambda x: not(x["sameItem"]), newSims))
    return sims


# calculate the change in similarities for author comparisons with each
# word left out.
# a_precomp and b_precomp include the data for authors and books, respectively
#    (With some precomputation already done)
# a_names is the names of the authors,
# a_ivi is the item vs item similarities for authors
# b_beta is the beta parameters for the book data
# b_authornames is the names of the authors associated with each book
# topWords is the list of top words
# saveDir is the location to save items.
# simInfo contains information about the similarity metric:
#    the distance calculation function
#    whether to fit the data to beta distributions
#    whether the metric is symmetric or not
def calculateKeyAuthorSimWords(a_precomp, a_names, a_ivi, b_beta, b_precomp, b_authornames, topWords, saveDir, simInfo):
    compSims = simInfo["compute"]
    useBeta = simInfo["useBeta"]
    symmetric = simInfo["symmetric"]
    useRemainder = simInfo["useRemainder"]
    addToJSON = simInfo["addToJSON"]

    sims = flattenIVI(a_ivi, symmetric)
    sims = sorted(sims, key=lambda x: x["1"]+x["2"])

    print("    Calculating importance of each word to similarity score...")

    b_names = []
    for i in range(len(b_precomp)):
        b_names.append("")

    namesToIndex = {}
    for i in range(len(a_names)):
        namesToIndex[a_names[i]] = i

    # get a filter that is 1 when a similarity has the same author
    numBooks = len(b_authornames)
    sameAuthorFilter = np.zeros((numBooks, numBooks))
    for i, a1 in enumerate(b_authornames):
        for j, a2 in enumerate(b_authornames):
            if (a1 == a2):
                sameAuthorFilter[i][j] = 1

    if useBeta:
        # Get pairs of target authors
        targetSimAuthors = [
            ["ApolloniusRhodius", "Homer", False],
            ["Arrian", "Thucydides", False]
        ]

        graphSaveDir = saveDir + "removeWordBetaCharts/"

        # print initial graph
        graphSims = []
        for k in range(len(a_ivi)):
            for j in range(len(a_ivi)):
                for ts in targetSimAuthors:
                    if((a_ivi[k][j]["1author"] == ts[0] and a_ivi[k][j]["2author"] == ts[1]) or
                       (a_ivi[k][j]["1author"] == ts[1] and a_ivi[k][j]["2author"] == ts[0])):
                       if not(ts[2]):
                           graphSims.append((a_ivi[k][j]["score"], ts[0] + "-" + ts[1]))
                           ts[2] = True


        oldDist = graphUtils.compBetaData(b_beta[1], b_beta[2])
        graphUtils.twoBetasComp(oldDist, graphSims, True, graphSaveDir, "original")
        oldGraphSims = graphSims
        graphUtils.twoBetasLog(oldDist, graphSims, True, graphSaveDir, "original")
        graphUtils.twoBetasZoom(oldDist, graphSims, True, graphSaveDir, "original")

    # calculate information with each word held out
    holdOneOutSims = []
    for i, tw in enumerate(topWords):
        # print(i, end=" ", flush=True)
        a_sims = compSims(a_precomp, ignoreIndex=i)

        a_res, _ = getSimilarityInfo(a_sims, a_names, a_names, "Authors", useBeta)

        if useBeta:
            # add info on the type probabilities for each dataset
            a_res = calculateTypeProbs(a_res, b_beta)
            # get book similarity data with the specific word held out
            b_simMatrix = compSims(b_precomp, ignoreIndex=i)

            b2_beta = getBooksBeta(b_simMatrix, sameAuthorFilter)

            # reset whether target authors have been found
            for ts in targetSimAuthors:
                ts[2] = False

            # get info on the target authors
            graphSims = []
            for k in range(len(a_res)):
                for j in range(len(a_res)):
                    for ts in targetSimAuthors:
                        if((a_res[k][j]["1author"] == ts[0] and a_res[k][j]["2author"] == ts[1]) or
                           (a_res[k][j]["1author"] == ts[1] and a_res[k][j]["2author"] == ts[0])):
                           if not(ts[2]):
                               graphSims.append((a_res[k][j]["score"], ts[0] + "-" + ts[1]))
                               ts[2] = True

            # create and save three kinds of graphs showing the beta distributions
            # and location of our target author pairs
            graphName = "remove_%d_%s" % (i, topWords[i])
            betaDist = graphUtils.compBetaData(b2_beta[1], b2_beta[2])
            graphUtils.twoBetasComp(betaDist, graphSims, True, graphSaveDir, graphName, oldDist=oldDist, oldSims=oldGraphSims)
            graphUtils.twoBetasLog(betaDist, graphSims, True, graphSaveDir, graphName, oldDist=oldDist, oldSims=oldGraphSims)
            graphUtils.twoBetasZoom(betaDist, graphSims, True, graphSaveDir, graphName, oldDist=oldDist, oldSims=oldGraphSims)

        i_sims = flattenIVI(a_res, symmetric)
        # sort so it is in same order as sims
        i_sims = sorted(i_sims, key=lambda x: x["1"]+x["2"])

        # check on these being out of sorted order
        for j, s in enumerate(sims):
            if s["1author"] != i_sims[j]["1author"]:
                print("%d Different first author: %s, %s" % (i, s["1author"], i_sims[j]["1author"]))
            if s["2author"] != i_sims[j]["2author"]:
                print("%d Different second author: %s, %s" % (i, s["2author"], i_sims[j]["2author"]))
        holdOneOutSims.append(i_sims)
    print("")


    # Calculate all of the differences so we can get a percentile score
    allDiffs = []
    for k, sim in enumerate(sims):
        if useBeta:
            scoreStr = "sd_logratio"
        else:
            scoreStr = "score"
        simLogRat = float(sim[scoreStr])

        # get word importance info
        for i, i_sims in enumerate(holdOneOutSims):
            noILogRat = float(i_sims[k][scoreStr])
            diff =  simLogRat - noILogRat
            allDiffs.append(diff)
    allDiffs = np.array(allDiffs)
    allDiffs.sort()
    diffPercentiles = {}
    # calculate "strong" percentile, gives the percent it is strictly
    # greater than.
    for i in reversed(range(len(allDiffs))):
        d = allDiffs[i]
        diffPercentiles[d] = (i)*100.0/len(allDiffs)

    # save the full list of differences.
    save = {
        "name": simInfo["name"].capitalize(),
        "allDiffs": allDiffs.tolist()
    }
    fname = "%sdists/diffLists.json" % (simInfo["baseDir"])
    if (addToJSON):
        utils.addToJSONList(fname, save)

    # save information from the calculations
    baseSaveDir = saveDir
    saveDir = saveDir + "authorSymReports/"
    allDiffs = []
    allDiffsNames = []
    allCumulDiffs = []
    allCumulDiffsNames = []
    allPercentiles = []
    allPercentilesNames = []
    for k, sim in enumerate(sims):
        output = []
        if useBeta:
            scoreStr = "sd_logratio"
        else:
            scoreStr = "score"

        simLogRat = float(sim[scoreStr])

        # get word importance info
        oList = []
        rawDiffs = []
        for i, i_sims in enumerate(holdOneOutSims):
            noILogRat = float(i_sims[k][scoreStr])
            diff =  simLogRat - noILogRat
            outString = "%+f %s (original %+f vs %+f)" % (diff, topWords[i], simLogRat, noILogRat)
            output.append(outString)
            oList.append([diff, outString])
            rawDiffs.append(diff)

        # save unsorted word importance in a file
        fname = "%s%s_%s.txt" % (saveDir, sim["1"], sim["2"])
        utils.safeWrite(fname, "\n".join(output))


        if (useRemainder):
            # Calculate difference contribution from each word
            firstIndex = namesToIndex[sim["1"]]
            secondIndex = namesToIndex[sim["2"]]
            perWord = -1*a_precomp[firstIndex][secondIndex]
        else:
            perWord = rawDiffs

        # save word importance into a json file
        # have to get the distance type and remove it from path
        vals = []
        simPercentiles = []
        # include both the regular values and the percentile
        for pw in perWord:
            #percentileVal = percentile(allDiffs, rd, kind="strict") #(rd-minDiff)/(maxDiff-minDiff)
            # Percentiles needs to be updated to use current system, but since
            # it isn't used for the paper we leave it as 0 for now.
            percentileVal = 0#diffPercentiles[pw]
            vals.append([pw, percentileVal])
            simPercentiles.append(percentileVal)

        sortedDiffs = sorted(perWord, reverse=True)

        pairName = "%s_%s" % (sim["1"], sim["2"])
        ad = sortedDiffs
        allDiffs.append(ad)
        allDiffsNames.append((pairName, ad))
        acd = np.cumsum(sortedDiffs).tolist()
        allCumulDiffs.append(acd)
        allCumulDiffsNames.append((pairName, acd))
        ap = sorted(simPercentiles, reverse=True)
        allPercentiles.append(ap)
        allPercentilesNames.append((pairName, ap))


        diffData = {"name": simInfo["name"].capitalize(), "vals": vals}
        fname = "%sdists/%s_%s.json" % (simInfo["baseDir"], sim["1"], sim["2"])
        if (addToJSON):
            utils.addToJSONList(fname, diffData)

        sortedOList = sorted(oList, key=lambda x: x[0])

        # save sorted word importance in a file
        output = []
        for item in sortedOList:
            output.append(item[1])

        fname = "%s%s_%s_sorted.txt" % (saveDir, sim["1"], sim["2"])
        utils.safeWrite(fname, "\n".join(output))


    # store median data for each author
    graphTypes = [
        ("all-diffs", allDiffs, allDiffsNames),
        ("all-diffs-cumul", allCumulDiffs, allCumulDiffsNames),
        ("all-pcts", allPercentiles, allPercentilesNames)
    ]
    for graphType, allPoints, allPointsNames in graphTypes:
        medianPoints = np.median(np.array(allPoints), axis=0)

        save = {
            "name": simInfo["name"].capitalize(),
            "line": medianPoints.tolist(),
            "all": allPointsNames
        }
        fname = "%sdists/median-%s.json" % (simInfo["baseDir"], graphType)
        if (addToJSON):
            utils.addToJSONList(fname, save)


# Given the item vs item similarities, calculate the internal consistency of the metric.
def evaluateMetricConsistency(itemVsItemSims, typeName, saveDir):
    # figure out which authors have one work and which works have one book
    if (typeName == "Books"):
        closest_same_work = 0
        closest_same_author = 0
        closest_same_author_unit = 0
        closest_different_author = 0
        closest_different_author_unit = 0
        num_unit_books = 0

        closest_same_work_list = []
        closest_same_author_list = []
        closest_same_author_unit_list = []
        closest_different_author_list = []
        closest_different_author_unit_list = []


        workBooks = {}
        authorWorks = {}
        for itemSims in itemVsItemSims:
            aName = itemSims[0]["1author"] #authornames[i]
            name = itemSims[0]["1"] #names[i]
            if aName in authorWorks:
                authorWorks[aName] += 1
            else:
                authorWorks[aName] = 1

            wName = aName + "." + name.split(".")[1]
            if wName in workBooks:
                workBooks[wName] += 1
            else:
                workBooks[wName] = 1




        # +0 when closest_different_author && !unitAuthor
        # +1 when !closest_different_author && !unitAuthor
        closestAuthorScores = []

        # +1 when closest_same_work and nonUnitBooks
        # +0 when !closest_same_work and nonUnitBooks
        closestWorkScores = []


        # Calculate information about whether each book's closest neighbor is
        # same author same work
        # same author different work
        # different author
        # with additional accounting for whether the work/author actually has
        # other books that could be closest.
        for itemSims in itemVsItemSims:
            me = itemSims[0]
            first = itemSims[1]
            aName = me["1author"] # authornames[i]
            myWork = me["1"].split(".")[1] # names[i].split(".")[1]
            otherWork = first["2"].split(".")[1]
            workName = aName + "." + myWork

            sameAuthor = first["2author"] == aName
            sameWork = sameAuthor and (myWork == otherWork)
            unitWork = workBooks[workName] == 1
            if unitWork:
                num_unit_books += 1

            unitAuthor = authorWorks[aName] == 1

            # find first books with same author and work
            numItems = len(itemSims)
            firstSameAuthor = numItems
            for i in range(1, numItems):
                if (itemSims[i]["2author"] == aName):
                    firstSameAuthor = i
                    break

            firstSameWork = numItems
            for i in range(1, numItems):
                if (itemSims[i]["2"].split(".")[1] == myWork):
                    firstSameWork = i
                    break

            signature = (aName, ".".join(me["1"].split(".")[1:]), first["2author"], ".".join(first["2"].split(".")[1:]), firstSameAuthor, firstSameWork)


            # Track scores for closest author, closest work
            if (not(unitAuthor)):
                if (sameAuthor):
                    closestAuthorScores.append(1)
                else:
                    closestAuthorScores.append(0)
            if (not(unitWork)):
                if (sameWork):
                    closestWorkScores.append(1)
                else:
                    closestWorkScores.append(0)

            if (sameWork and sameAuthor):
                closest_same_work += 1
                closest_same_work_list.append(signature)
            elif (sameAuthor and unitWork):
                closest_same_author_unit += 1
                closest_same_author_unit_list.append(signature)
            elif (sameAuthor):
                closest_same_author += 1
                closest_same_author_list.append(signature)
            elif (unitAuthor):
                closest_different_author_unit += 1
                closest_different_author_unit_list.append(signature)
            else:
                closest_different_author += 1
                closest_different_author_list.append(signature)

        totalWorks = len(itemVsItemSims)
        bookComparisonOutput = []
        bookComparisonOutput.append("%.2f%%, %d/%d, Same work" % ((100.0*closest_same_work/totalWorks), closest_same_work, totalWorks))
        bookComparisonOutput.append("%.2f%%, %d/%d, Same author (no same work)" % ((100.0*closest_same_author_unit/totalWorks), closest_same_author_unit, totalWorks))
        bookComparisonOutput.append("%.2f%%, %d/%d, Same author" % ((100.0*closest_same_author/totalWorks), closest_same_author, totalWorks))
        bookComparisonOutput.append("%.2f%%, %d/%d, Different author (no same author)" % ((100.0*closest_different_author_unit/totalWorks), closest_different_author_unit, totalWorks))
        bookComparisonOutput.append("%.2f%%, %d/%d, Different author" % ((100.0*closest_different_author/totalWorks), closest_different_author, totalWorks))

        #print("\n".join(bookComparisonOutput))

        bookComparisonOutput.append("====================")
        bookComparisonOutput.append("====================")

        pssblSameAuth = totalWorks - closest_different_author_unit
        similarSameAuth = pssblSameAuth - closest_different_author
        bookComparisonOutput.append("%.2f%%, %d/%d, Book most similar to same author (where possible)" % ((100.0*similarSameAuth/pssblSameAuth), similarSameAuth, pssblSameAuth))
        #bookComparisonOutput.append("Of the %d books by an author who wrote at least 2 books, %d (%.2f%%) were judged most similar to a book by the same author" % (pssblSameAuth, similarSameAuth, (100.0*similarSameAuth/pssblSameAuth)))

        nonUnitBooks = totalWorks - num_unit_books
        bookComparisonOutput.append("%.2f%%, %d/%d, Books most similar to same work (where possible)" % ((100.0*closest_same_work/nonUnitBooks), closest_same_work, nonUnitBooks))
        #bookComparisonOutput.append("of the %d books with another book in the same work, %d (%.2f%%) were most similar to another book from the same work" % (nonUnitBooks, closest_same_work, (100.0*closest_same_work/nonUnitBooks)))

        bookComparisonOutput.append("%.2f%%, %d/%d, Books most similar to another work by same author" % ((100.0*closest_same_author/nonUnitBooks), closest_same_author, nonUnitBooks))
        #bookComparisonOutput.append("With another %d (%.2f%%) closest to another work by the same author" % (closest_same_author, (100.0*closest_same_author/nonUnitBooks)))

        sameAuthorRanks = []
        for sig in closest_different_author_list:
            _, _, _, _, saRank, _ = sig
            sameAuthorRanks.append(saRank)

        medianSARank = np.median(sameAuthorRanks)
        bookComparisonOutput.append("%d, Books closest to a different author (when not required): " % (closest_different_author))
        bookComparisonOutput.append("%d, Median first occurrence of a book by the same author in list of most similar texts (when author is different)." % (medianSARank))

        #bookComparisonOutput.append("Of the %d books judged to be closest to a different author (when another work by the same author exists), the median first occurrence of a book by the same author was the %d most similar text." % (closest_different_author, medianSARank))

        bookComparisonOutput.append("====================")
        bookComparisonOutput.append("====================")
        bookComparisonOutput.append("Same work: %.2f%% (%d/%d)" % ((100.0*closest_same_work/totalWorks), closest_same_work, totalWorks))
        for sig in closest_same_work_list:
            bookComparisonOutput.append("  %s.%s: closest is %s.%s. Highest with same author: %d. Highest from same work: %d." % sig)

        bookComparisonOutput.append("=========")
        bookComparisonOutput.append("Same author (no same work): %.2f%% (%d/%d)" % ((100.0*closest_same_author_unit/totalWorks), closest_same_author_unit, totalWorks))
        for sig in closest_same_author_unit_list:
            bookComparisonOutput.append("  %s.%s: closest is %s.%s. Highest with same author: %d. Highest from same work: %d." % sig)

        bookComparisonOutput.append("=========")
        bookComparisonOutput.append("Same author: %.2f%% (%d/%d)" % ((100.0*closest_same_author/totalWorks), closest_same_author, totalWorks))
        for sig in closest_same_author_list:
            bookComparisonOutput.append("  %s.%s: closest is %s.%s. Highest with same author: %d. Highest from same work: %d." % sig)

        bookComparisonOutput.append("=========")
        bookComparisonOutput.append("Different author (no same author): %.2f%% (%d/%d)" % ((100.0*closest_different_author_unit/totalWorks), closest_different_author_unit, totalWorks))
        for sig in closest_different_author_unit_list:
            bookComparisonOutput.append("  %s.%s: closest is %s.%s. Highest with same author: %d. Highest from same work: %d." % sig)

        bookComparisonOutput.append("=========")
        bookComparisonOutput.append("Different author: %.2f%% (%d/%d)" % ((100.0*closest_different_author/totalWorks), closest_different_author, totalWorks))
        for sig in closest_different_author_list:
            bookComparisonOutput.append("  %s.%s: closest is %s.%s. Highest with same author: %d. Highest from same work: %d." % sig)

        bookComparisonOutput.append("=========")
        utils.safeWrite(saveDir+"comparisonInfo.txt", "\n".join(bookComparisonOutput))


        scores = {}
        scores["author"] = closestAuthorScores
        scores["work"] = closestWorkScores
        utils.safeWrite(saveDir+"scores.json", scores, True)

# Only Print information about the data similarities
#   itemVsItemSims: similarities gathered by item
#   saveDir: place to save data
def printSimData(itemVsItemSims, saveDir):
    #================ Extract data from sims and betaParams
    sims = flattenIVI(itemVsItemSims)

    # sort similarities for printing
    sortedSims = sorted(sims, key=lambda x: x["score"], reverse=True)

    simOutput = []
    for s in sortedSims:
        simOutput.append(getSimString(s))
    utils.safeWrite(saveDir+"sims.txt", "\n".join(simOutput))

# Print and visualize information about the data similarities
#   itemVsItemSims: similarities gathered by item
#   useBeta: True if we should be printing/displaying beta distribution info
#   betaParams: parameters for beta distributions
#   typeName: Books or Authors
#   saveDir: place to save data
def printAndVizSimData(itemVsItemSims, useBeta, betaParams, typeName, saveDir):
    #================ Extract data from sims and betaParams
    sims = flattenIVI(itemVsItemSims)

    simsDifferentAuthors = list(filter(lambda x: not(x["sameAuthor"]), sims))
    simsSameAuthor = list(filter(lambda x: x["sameAuthor"], sims))

    # get data for scatter of similarities by century difference and beta distribution fits
    raw_sims = np.array(list(map(lambda x: x["score"], sims)))
    raw_sims_da = np.array(list(map(lambda x: x["score"], simsDifferentAuthors)))
    raw_sims_sa = np.array(list(map(lambda x: x["score"], simsSameAuthor)))
    sim_cen = np.array(list(map(extractCentDatapoint, sims)))
    sim_cen_y = np.array(list(map(extractEuclidDionysus, sims)))
    sim_cen_names = np.array(list(map(lambda x: x["1"] + ", " + x["2"], sims)))

    # sort similarities for printing
    sortedSims = sorted(sims, key=lambda x: x["score"], reverse=True)
    sortedSimsDA = sorted(simsDifferentAuthors, key=lambda x: x["score"], reverse=True)
    sortedSimsSA = sorted(simsSameAuthor, key=lambda x: x["score"], reverse=True)

    if useBeta:
        beta_all, beta_diff, beta_same = betaParams
        a, b = beta_all
        a_da, b_da = beta_diff
        a_sa, b_sa = beta_same

    #================ Print info

    # Write information about similarity comparisons
    for itemSims in itemVsItemSims:
        me = itemSims[0]

        itemOutput = []
        for s in itemSims:
            #itemOutput.append("%.6f (%s) - %s (%s)" % (s["score"], s["sd_ratio"], s["2"], centToString(genre.toCents["2author"])))
            itemOutput.append("%.6f - %s (%s)" % (s["score"], s["2"], centToString(genre.toCent(s["2author"]))))
        itemSaveDir = "%ssims/%s.txt" % (saveDir, me["1"])
        utils.safeWrite(itemSaveDir, "\n".join(itemOutput))

    # print top similarities and save all similarities to a file
    numSimsToPrint = 5

    # print("Top Similarities:")
    # for s in sortedSims[:numSimsToPrint]:
    #     print(getSimString(s))
    # print("----")

    simOutput = []
    for s in sortedSims:
        simOutput.append(getSimString(s))
    utils.safeWrite(saveDir+"sims.txt", "\n".join(simOutput))

    if (typeName == "Books"):
        # print("Top Similarities (Different Authors):")
        # for s in sortedSimsDA[:numSimsToPrint]:
        #     print(getSimString(s))
        # print("----")

        simDAOutput = []
        for s in sortedSimsDA:
            simDAOutput.append(getSimString(s))
        utils.safeWrite(saveDir+"simsDifferentAuthors.txt", "\n".join(simDAOutput))

        simSAOutput = []
        for s in sortedSimsSA:
            simSAOutput.append(getSimString(s))
        utils.safeWrite(saveDir+"simsSameAuthors.txt", "\n".join(simSAOutput))

    if useBeta:
        print("all authors beta params: %.4f, %.4f" % (a, b))
        if (typeName == "Books"):
            print("different author beta params: %.4f, %.4f" % (a_da, b_da))
            print("same author beta params: %.4f, %.4f" % (a_sa, b_sa))
        print("------")

    saveOutput = True

    if (typeName == "Authors"):
        # display similarities by century
        sim_cen_no_genre_diff = np.copy(sim_cen)
        for pair in sim_cen_no_genre_diff:
            pair[0] = np.around(pair[0])
        print("    Starting comparison overall... ", end="", flush=True)
        graphUtils.centuryComparisonOverall(sim_cen_no_genre_diff, sim_cen_y, sim_cen_names, saveOutput, saveDir)
        print("done")
        print("    Starting comparison by genre... ", end="", flush=True)
        graphUtils.centuryComparisonByGenre(sim_cen, sim_cen_y, sim_cen_names, saveOutput, saveDir)
        print("done")
        print("    Starting rainclouds... ", end="", flush=True)
        try:
            graphUtils.centuryComparisonByGenre(sim_cen, sim_cen_y, sim_cen_names, saveOutput, saveDir, violin=True)
        except:
            print("error making violin...", end="", flush=True)
        try:
            graphUtils.centuryComparisonByGenre(sim_cen, sim_cen_y, sim_cen_names, saveOutput, saveDir, raincloud=True)
        except:
            print("error making raincloud...", end="", flush=True)
        print("done")

        # Save the range of similarities for the graphs
        minSim = 1
        minName = ""
        maxSim = 0
        maxName = ""
        for i in range(len(sim_cen)):
            if (sim_cen_y[i] <= 1): # Ignore Hymn to Dionysus and Euclid
                i_sim = sim_cen[i][1]
                if i_sim < minSim:
                    minSim = i_sim
                    minName = sim_cen_names[i]
                if i_sim > maxSim:
                    maxSim = i_sim
                    maxName = sim_cen_names[i]
        simRangeOutput = []
        simRangeOutput.append("Range: %.6f" % (maxSim-minSim))
        simRangeOutput.append("Max: %s (%.6f)" % (maxName, maxSim))
        simRangeOutput.append("Min: %s (%.6f)" % (minName, minSim))
        utils.safeWrite(saveDir+"simRange.txt", "\n".join(simRangeOutput))

# ===========================================================
# ======== Aggregate features and run sort/visualize ========
# ===========================================================

def runAnalysis(authors, books, saveDir, topWords, simInfo, includeBooks):
    useBeta = simInfo["useBeta"]
    compSims = simInfo["compute"]
    useRemainder = simInfo["useRemainder"]
    evaluateMetric = simInfo["evaluateMetric"]
    makeGraphs = simInfo["makeGraphs"]

    if (simInfo["useSmoothing"]):
        precompSims = simInfo["precomputeSmooth"]
    else:
        precompSims = simInfo["precompute"] # lambda x: x for most

    # If we aren't making graphs, we are at most evaluating the metric, which
    # only happens when examining the books, so we can just skip
    if (not(makeGraphs) and not(includeBooks)):
        return

    # ==== Calculate data info
    a_typeName = "Authors"
    b_typeName = "Books"

    # aggregate features for each author into one data set
    a_data = []
    a_target = []
    a_names = []
    for i in range(len(authors)):
        author = authors[i]
        if useRemainder:
            base = np.zeros(len(author.counts))
            base[:-1] = author.counts[:-1]
            base[-1] = np.sum(author.counts[-1])
        else:
            base = author.counts[:-1]
        a_data.append(base)
        a_target.append(i)
        a_names.append(author.authorName)

    # Precompute similarity data
    a_precomp = precompSims(a_data)
    # Compute similarity data
    a_sims = compSims(a_precomp)
    # Get comparison data for each item vs each other item
    a_ivi, a_beta = getSimilarityInfo(a_sims, a_names, a_names, a_typeName, useBeta)

    # set up map from author name to target index
    authorToIndex = {}

    for i in range(len(authors)):
        author = authors[i]
        if (author.authorName[-2:] != "_2"):
            authorToIndex[author.authorName] = i

    if (includeBooks):
        # aggregate features for each book
        b_data = []
        b_target = []
        b_names = []
        b_authornames = []
        count = 0
        for book in books:
            if (book.numTokens >= mp.MIN_TOKENS_NECESSARY):
                if useRemainder:
                    base = np.zeros(len(book.counts))
                    base[:-1] = book.counts[:-1]
                    base[-1] = np.sum(book.counts[-1])
                else:
                    base = book.featureData[:-1]
                b_data.append(base)
                b_target.append(authorToIndex[book.author])
                b_names.append(book.getLongName())
                #print("%d: %s" % (count, book.getShortName()))
                b_authornames.append(book.author)
                count += 1

        b_precomp = precompSims(b_data)
        b_sims = compSims(b_precomp)
        b_ivi, b_beta = getSimilarityInfo(b_sims, b_names, b_authornames, b_typeName, useBeta)
    else:
        b_beta = [[-1, -1], [-1, -1], [-1, -1]]

    if useBeta:
        # add info on the type probabilities for each dataset
        a_ivi = calculateTypeProbs(a_ivi, b_beta)
        if (includeBooks):
            b_ivi = calculateTypeProbs(b_ivi, b_beta)

    a_subDir = "%s%s/" % (saveDir, a_typeName)
    b_subDir = "%s%s/" % (saveDir, b_typeName)

    # Evaluate how the metric does at comparing books of the same authors.
    if (evaluateMetric and includeBooks):
        print("    Evaluating Metric...")

        evaluateMetricConsistency(b_ivi, b_typeName, b_subDir)

    if (makeGraphs):
        # calculate which words are important for author similarity
        if (includeBooks):
            calculateKeyAuthorSimWords(a_precomp, a_names, a_ivi, b_beta, b_precomp, b_authornames, topWords, saveDir, simInfo)

        # ==== Print and visualize info
        print("Authors:")

        printAndVizSimData(a_ivi, useBeta, a_beta, a_typeName, a_subDir)

        if (includeBooks):
            print("Books:")

            printAndVizSimData(b_ivi, useBeta, b_beta, b_typeName, b_subDir)
    else:
        printSimData(a_ivi, a_subDir)

# ===========================================================
# ===================== Run Everything ======================
# ===========================================================

# list of distance/similarity types to check, with a name and function for each
SIMILARITY_METRICS = [
    # Probability of generation doesn't do nearly as good a job as jensen-shannon
    # {
    #     "name": "probability",
    #     "compute": compSimsProb,
    #     "useBeta": False,#True,#
    #     "symmetric": False,
    #     "useRemainder": True,
    #     "precompute": precomputeProb,
    #     "evaluateMetric": True,
    #     "makeGraphs": False,
    # },
    {
        "name": "jensen-shannon",
        "compute": compSimsJS,
        "useBeta": False,#True,#
        "symmetric": True,
        "useRemainder": True, # we're comparing probability distributions so we need non top words also
        "useSmoothing": True,
        "precompute": precomputeJS,
        "precomputeSmooth": precomputeJS,
        "evaluateMetric": True,
        "makeGraphs": True,
        "addToJSON": True,
    },
    {
        "name": "cosine",
        "compute": compSimsCosine,
        "useBeta": False,#True,#
        "symmetric": True,
        "useRemainder": False,
        "useSmoothing": False,
        "precompute": precomputeDefault,
        "precomputeSmooth": precomputePlusOne,
        "evaluateMetric": True,
        "makeGraphs": False,
        "addToJSON": True,
    },
    {
        "name": "canberra",
        "compute": compSimsCanberra,
        "useBeta": False,#True,#
        "symmetric": True,
        "useRemainder": False,
        "useSmoothing": False,
        "precompute": precomputeDefault,
        "precomputeSmooth": precomputePlusOne,
        "evaluateMetric": True,
        "makeGraphs": False,
        "addToJSON": True,
    },
    {
        "name": "cityblock",
        "compute": compSimsCityblock,
        "useBeta": False,#True,#
        "symmetric": True,
        "useRemainder": False,
        "useSmoothing": False,
        "precompute": precomputeDefault,
        "precomputeSmooth": precomputePlusOne,
        "evaluateMetric": True,
        "makeGraphs": False,
        "addToJSON": True,
    },
    {
        "name": "minmax",
        "compute": compSimsMinMax,
        "useBeta": False,#True,#
        "symmetric": True,
        "useRemainder": False,
        "useSmoothing": False,
        "precompute": precomputeDefault,
        "precomputeSmooth": precomputePlusOne,
        "evaluateMetric": True,
        "makeGraphs": False,
        "addToJSON": True,
    },
    {
        "name": "burrowsdelta",
        "compute": compSimsBurrowsDelta,
        "useBeta": False,#True,#
        "symmetric": True,
        "useRemainder": False,
        "useSmoothing": False,
        "precompute": precomputeDefault,
        "precomputeSmooth": precomputePlusOne,
        "evaluateMetric": True,
        "makeGraphs": False,
        "addToJSON": True,
    }
]

# Run various similarity calculations
def calculateSimilarity(dataSplit, top, subsetSize, simCompare, includeBooks, saveDirBase):
    topName, _, _ = top

    # Load authors and books
    authors, books, topWords = loadWCData(saveDirBase, dataSplit, topName)

    # calculate save directory based on input parameters
    baseSaveDir = saveDirBase + "%s/" % (topName)

    # Always just run every metric with its defaults set
    simConditions = [
        (True, False, False)
    ]

    # If we want to compare various metrics, add the different options
    if simCompare:
        simConditions.append((False, False, False))
        simConditions.append((False, True, False))
        simConditions.append((False, False, True))
        simConditions.append((False, True, True))


    # For each type of distance, run the analysis and save it in an
    # appropriate directory
    for default, useSmoothing, useRemainder in simConditions:
        if (default):
            print("Default...")
        else:
            print("Smoothing: %s, Remainder: %s..." % (useSmoothing, useRemainder))
        for simInfo in SIMILARITY_METRICS:
            if not(default) and (simInfo["name"] == "jensen-shannon"):
                continue
            simInfo = copy.deepcopy(simInfo)

            distName = simInfo["name"]
            simInfo["baseDir"] = baseSaveDir
            print("  Working on %s..." % distName)

            folderName = "metric"
            if (simInfo["useBeta"]):
                folderName += "-beta"

            # Set up appropriate folder name and parameters
            if not(default):
                simInfo["addToJSON"] = False
                if (useRemainder):
                    simInfo["useRemainder"] = True
                    folderName += "+remainder"
                else:
                    simInfo["useRemainder"] = False
                    folderName += "-remainder"

                if (useSmoothing):
                    simInfo["useSmoothing"] = True
                    folderName += "+smoothed"
                else:
                    simInfo["useSmoothing"] = False
                    folderName += "-smoothed"

            saveDir = "%s%s/%s/" % (baseSaveDir, distName, folderName)

            runAnalysis(authors, books, saveDir, topWords, simInfo, includeBooks)

if __name__ == "__main__":
    for top in mp.tops:
        name, topWords, poetryWords, subsetSize, splitParameter, includeBooks, includeGraphs, compSimOptions, wordToPOS = top
        newTop = (name, topWords, poetryWords)
        saveDir = mp.getSaveDir(mp.language, mp.languageInfo, splitParameter)

        calculateSimilarity(splitParameter, newTop, subsetSize, compSimOptions, includeBooks, saveDir)
        print("======================")
