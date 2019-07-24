# -*- coding: utf-8 -*-
# Code for creating many graphs

import numpy as np
import json
import copy
from scipy.stats import beta, linregress
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_pdf import PdfPages

from sklearn import decomposition

# For Regression
import statsmodels.api as sm


import utils
import tsne
import umap

# Object for storing a dataset
class Dataset:
    def __init__(self, data, target):
        self.data = data
        self.target = target

# Initialize a standard chart and return the figure
def initStandardChart(saveOutput):
    # set figure size
    plt.clf()
    if saveOutput:
        fig = plt.figure()
        fig.set_size_inches((11.), (8.5))
    else:
        fig = plt.figure(1, figsize=(8, 6))
    return fig

# Initialize a chart with two subplots and return the figure and axes
def init2SubplotChart(saveOutput):
    # set figure size
    plt.clf()
    if saveOutput:
        fig, axes = plt.subplots(2)
        fig.set_size_inches((8.5), (11))
    else:
        fig, axes = plt.subplots(2)
    return fig, axes


# If saveOutput, save the chart at filename; else, display it.
def finishChart(saveOutput, filename):
    if saveOutput:
        utils.check_and_create_path(filename)
        pp = PdfPages(filename)
        pp.savefig()
        pp.close()
    else:
        plt.show()

    plt.close()


# Fit using statsmodel
def runRegression(regrX, regrY):
    regrX = sm.add_constant(regrX)
    regrModel = sm.OLS(regrY,regrX)
    regr = regrModel.fit()

    slope = regr.params[1]
    intercept = regr.params[0]
    r2 = regr.rsquared
    # F Value
    fval = regr.fvalue
    # Degrees of freedom
    df = regr.df_resid
    pval = regr.pvalues[1]

    return (slope, intercept, r2, fval, df, pval)


# given a list of colors with r/g/b specified in the 0-255 range, convert them to the 0-1 range
def getPercentColors(predefinedColors):
    return list(map(lambda c: list(map(lambda v: v/255.0, c)), predefinedColors))


# darken/lighten an r, g, b tuple expressed in the 0-1 range
def adjustColor(color, adjust):
    r, g, b = color
    r = max(0, min(r*adjust, 1))
    g = max(0, min(g*adjust, 1))
    b = max(0, min(b*adjust, 1))
    return (r, g, b)

# ==============================================================================
# ==============================================================================
# ==============================================================================



# do PCA down to 3 components, then visualize
# Portions of this adapted from code written by Gaël Varoquaux
# dataSet is the list of data to train on, with names as an array of names for those feature vectors
# includeNames is true if we want to print the names in the figure
# saveOutput is true if we want to save the feature to a file rather than view it
def pca3Viz(dataSet, names, includeNames, saveOutput, saveDir):
    np.random.seed(5)

    X = dataSet.data

    # train PCA
    pca = decomposition.PCA(n_components=3)
    pca.fit(X)

    # transform the training and test data
    X = pca.transform(X)

    baseSaveDir = saveDir
    for t in dataSet.target:
        fig = initStandardChart(saveOutput)

        saveDir = baseSaveDir + t["name"]
        y = t["target"]

        # set 3d axes
        ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

        # if we include names, print them
        if (includeNames):
            for i in range(len(X)):
                name = names[i]
                ax.text3D(X[i, 0], X[i, 1], (X[i, 2] + 0.01),
                          name, horizontalalignment='center', size=8)


        # plot the data.
        ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y, cmap=plt.get_cmap("Set1"))

        ax.w_xaxis.set_ticklabels([])
        ax.w_yaxis.set_ticklabels([])
        ax.w_zaxis.set_ticklabels([])


        # save or show the data
        if includeNames:
            labelText = "_labels"
        else:
            labelText = "_no_labels"
        filename = saveDir + "pca3D" + labelText + ".pdf"
        finishChart(saveOutput, filename)

# do PCA down to 2 components, then visualize
# Portions of this adapted from code written by Gaël Varoquaux
# dataSet is the list of data to train on, with names as an array of names for those feature vectors
# includeNames is true if we want to print the names in the figure
# saveOutput is true if we want to save the feature to a file rather than view it
# oneThree is true if we are examining axes 1 and 3 rather than 1 and 2
def pca2Viz(dataSet, names, includeNames, saveOutput, saveDir, oneThree):
    np.random.seed(5)

    X = dataSet.data

    # get the proper axes to examine
    if (oneThree):
        ax0 = 0
        ax1 = 2
        numComponents = 3
    else:
        ax0 = 0
        ax1 = 1
        numComponents = 2

    # train PCA and transform data
    pca = decomposition.PCA(n_components=numComponents)
    pca.fit(X)
    X = pca.transform(X)

    baseSaveDir = saveDir
    for t in dataSet.target:
        fig = initStandardChart(saveOutput)

        saveDir = baseSaveDir + t["name"]
        y = t["target"]

        # plot the data.
        plt.scatter(X[:, ax0], X[:, ax1], s=49, c=y, cmap=plt.get_cmap("Set1"))

        ymin, ymax = plt.ylim()
        yscale = ymax - ymin


        # if we include names, print them
        if (includeNames):
            for i in range(len(X)):
                name = names[i]
                plt.text(X[i, ax0], (X[i, ax1] + 0.015*yscale),
                          name, horizontalalignment='center', size=8)

        # save or show the data
        if includeNames:
            labelText = "_labels"
        else:
            labelText = "_no_labels"
        if (oneThree):
            oneThreeText = "_1_3"
        else:
            oneThreeText = ""
        filename = saveDir + "pca2D" + oneThreeText + labelText + ".pdf"
        finishChart(saveOutput, filename)

# do PCA down to 4 components, then visualize
# Portions of this adapted from code written by Gaël Varoquaux
# dataSet is the list of data to train on, with names as an array of names for those feature vectors
# includeNames is true if we want to print the names in the figure
# saveOutput is true if we want to save the feature to a file rather than view it
def pca4Viz(dataSet, names, includeNames, saveOutput, saveDir):
    np.random.seed(5)

    X = dataSet.data

    # train and apply PCA
    pca = decomposition.PCA(n_components=4)
    pca.fit(X)
    X = pca.transform(X)

    baseSaveDir = saveDir
    for t in dataSet.target:
        fig, axes = init2SubplotChart(saveOutput)

        saveDir = baseSaveDir + t["name"]
        y = t["target"]

        # make the two plots, with names if we are including names
        for k in range(len(axes)):
            ax = axes[k]
            offset = k*2
            secondStartIndex = 1

            ax.scatter(X[:, 0+offset], X[:, secondStartIndex+offset], s=49, c=y, cmap=plt.get_cmap("Set1"))

            if (includeNames):
                ymin, ymax = ax.axes.get_ylim()
                yscale = ymax - ymin

                for i in range(len(X)):
                    name = names[i]
                    ax.text(X[i, 0+offset], (X[i, secondStartIndex+offset] + 0.015*yscale),
                              name, horizontalalignment='center', size=8)



        # save or show the data
        if includeNames:
            labelText = "_labels"
        else:
            labelText = "_no_labels"
        filename = saveDir + "pca4D" + labelText + ".pdf"

        finishChart(saveOutput, filename)

# data histogram with no beta distribution shown
def dataHistogram(data, saveOutput, saveDir, name):
    dataHistogramWithBeta(data, 0, 0, saveOutput, saveDir, name, useBeta=False)

# data histogram with a beta distribution specified by a (alpha) and b (beta)
def dataHistogramWithBeta(data, a, b, saveOutput, saveDir, name, useBeta=True):
    fig = initStandardChart(saveOutput)

    n, bins, patches = plt.hist(data, bins='auto', density=True, stacked=True)

    if useBeta:
        x = np.linspace(beta.ppf(0.001, a, b), beta.ppf(0.999, a, b), 1000)
        plt.plot(x, beta.pdf(x, a, b), 'r-', lw=2, alpha=0.8, label='beta pdf')

        plt.xlim(0, 1)

    filename = saveDir + name + ".pdf"

    finishChart(saveOutput, filename)


# Calculate x and y coordinates to display beta distributions
def compBetaData(beta_1, beta_2):
    a1, b1 = beta_1
    a2, b2 = beta_2

    x1 = np.linspace(beta.ppf(0.001, a1, b1), beta.ppf(0.999, a1, b1), 1000)
    y1 = beta.pdf(x1, a1, b1)

    x2 = np.linspace(beta.ppf(0.001, a2, b2), beta.ppf(0.999, a2, b2), 1000)
    y2 = beta.pdf(x2, a2, b2)

    return x1, y1, x2, y2

# graph two beta distributions compared to a past distribution
def twoBetasComp(data, sims, saveOutput, saveDir, name, oldDist=None, oldSims=None, xlim=[0, 1]):
    fig = initStandardChart(saveOutput)

    if (not(oldDist == None)):
        x1, y1, x2, y2 = oldDist
        plt.plot(x1, y1, 'r-.', lw=2, alpha=0.4)

        plt.plot(x2, y2, 'b-.', lw=2, alpha=0.4)

    if (not(oldSims == None)):
        colorMap = plt.get_cmap("Set2")
        colors = colorMap(range(len(oldSims)))
        for i, s in enumerate(oldSims):
            sim, simName = s
            plt.axvline(x=sim, linestyle=":", color=colors[i], alpha=0.5)


    x1, y1, x2, y2 = data
    plt.plot(x1, y1, 'r-', lw=2, alpha=0.5, label='Different Author')
    plt.plot(x2, y2, 'b-', lw=2, alpha=0.5, label='Same Author')


    colorMap = plt.get_cmap("Set2")
    colors = colorMap(range(len(sims)))
    for i, s in enumerate(sims):
        sim, simName = s
        plt.axvline(x=sim, linestyle="-", label=simName, color=colors[i])


    plt.xlim(xlim[0], xlim[1])

    plt.legend()

    filename = saveDir + name + ".pdf"

    finishChart(saveOutput, filename)


# graph two beta distributions on a zoomed scale
def twoBetasZoom(data, sims, saveOutput, saveDir, name, oldDist=None, oldSims=None):
    twoBetasComp(data, sims, saveOutput, saveDir, name, oldDist=oldDist, oldSims=oldSims, xlim=[0.8, 1])

# graph two beta distributions on a log scale
def twoBetasLog(data, sims, saveOutput, saveDir, name, oldDist=None, oldSims=None):
    fig = initStandardChart(saveOutput)

    if (not(oldDist == None)):
        x1, y1, x2, y2 = oldDist
        plt.semilogx(1-x1, y1, 'r-.', lw=2, alpha=0.4)

        plt.semilogx(1-x2, y2, 'b-.', lw=2, alpha=0.4)

    if (not(oldSims == None)):
        colorMap = plt.get_cmap("Set2")
        colors = colorMap(range(len(oldSims)))
        for i, s in enumerate(oldSims):
            sim, simName = s
            plt.axvline(x=1-sim, linestyle=":", color=colors[i], alpha=0.5)


    x1, y1, x2, y2 = data
    plt.semilogx(1-x1, y1, 'r-', lw=2, alpha=0.5, label='Different Author')

    plt.semilogx(1-x2, y2, 'b-', lw=2, alpha=0.5, label='Same Author')


    colorMap = plt.get_cmap("Set2")
    colors = colorMap(range(len(sims)))
    for i, s in enumerate(sims):
        sim, simName = s
        plt.axvline(x=1-sim, linestyle="-", label=simName, color=colors[i])

    xEnd = 0.001
    plt.xlim(1, xEnd)

    xTicks = [xEnd, 0.01, 0.1, 1]
    xLabels = list(map(lambda x: str(1-x), xTicks))
    plt.xticks(xTicks, xLabels)

    plt.legend()

    filename = saveDir + name + "_log.pdf"

    finishChart(saveOutput, filename)

    plt.close()

# graph centuries between on the x axis, similarity on the y axis
# Consider all texts, don't divide by genre
def centuryComparisonOverall(data, y, names, saveOutput, saveDir):
    # remove same/different genre distinction
    newY = []
    conversion = {
        0: 2,
        1: 2,
        2: 0,
        3: 1,
    }
    for label in y:
        newY.append(conversion[label])

    predefinedColors = [(112, 44, 140), (219, 105, 23), (170, 170, 170)]
    legendLabels = ["Euclid", "Hymn to Dionysus", "Other Texts"]
    legendOrder = [0, 1, 2]
    centuryComparison(data, newY, names, saveOutput, True, False, False, predefinedColors, legendLabels, legendOrder, saveDir, "century_sims_overall", None)

# graph centuries between on the x axis, similarity on the y axis
# Consider all texts, divide by genre
def centuryComparisonByGenre(data, y, names, saveOutput, saveDir):
    newData = []
    newY = []
    indices = []
    for i in range(len(y)):
        if (y[i] <= 1):
            indices.append(i)
            # newData.append(data[i])
            # newY.append(y[i])

    # newData = np.array(newData)
    newData = data[indices]
    newY = y[indices]
    newNames = names[indices]

    predefinedColors = [(150, 205, 230), (186, 28, 48), (0, 0, 0)]
    legendLabels = ["Same Genre", "Different Genres", "All Pairs"]
    legendOrder = [2, 0, 1]
    centuryComparison(newData, newY, newNames, saveOutput, False, True, True, predefinedColors, legendLabels, legendOrder, saveDir, "century_sims_genre", [0.87, 1.0])

    # Cut off the tail after a cutoff
    TAIL_CUTOFF = 9
    maxPoint = 0
    for i, point in enumerate(newData):
        pointVal = int(round(point[0]))
        if pointVal > maxPoint:
            maxPoint = pointVal

    if maxPoint > TAIL_CUTOFF:
        cutoffIndices = []
        for i in range(len(newData)):
            if (int(round(newData[i][0])) <= TAIL_CUTOFF):
                cutoffIndices.append(i)

        cutoffData = newData[cutoffIndices]
        cutoffY = newY[cutoffIndices]
        cutoffNames = newNames[cutoffIndices]
        centuryComparison(cutoffData, cutoffY, cutoffNames, saveOutput, False, True, True, predefinedColors, legendLabels, legendOrder, saveDir, "century_sims_genre_under_%d" % TAIL_CUTOFF, [0.87, 1.0])


# graph centuries between on the x axis, similarity on the y axis
# color texts based on whether they represent sets of the same/different genres
def centuryComparison(data, y, names, saveOutput, showAverage, showLinReg, separateGenres, predefinedColors, legendLabelsBase, legendOrder, saveDir, fname="century_sims", ylim=None):
    legendLabels = copy.deepcopy(legendLabelsBase)

    averageStorage = {}
    averageStorageSameGenre = {}
    averageStorageDiffGenre = {}
    maxPoint = 0

    # store x and y values for points, as well as for points separated by same/different genre
    allX = []
    allY = []
    sgX = []
    sgY = []
    dgX = []
    dgY = []

    for i, point in enumerate(data):
        pointVal = int(round(point[0]))
        if pointVal > maxPoint:
            maxPoint = pointVal

        if pointVal in averageStorage:
            averageStorage[pointVal]["sum"] += point[1]
            averageStorage[pointVal]["num"] += 1
        else:
            averageStorage[pointVal] = {"sum": point[1], "num": 1}

        allX.append(pointVal)
        allY.append(point[1])

        if y[i] == 0:
            sgX.append(pointVal)
            sgY.append(point[1])
            if pointVal in averageStorageSameGenre:
                averageStorageSameGenre[pointVal]["sum"] += point[1]
                averageStorageSameGenre[pointVal]["num"] += 1
            else:
                averageStorageSameGenre[pointVal] = {"sum": point[1], "num": 1}
        elif y[i] == 1:
            dgX.append(pointVal)
            dgY.append(point[1])
            if pointVal in averageStorageDiffGenre:
                averageStorageDiffGenre[pointVal]["sum"] += point[1]
                averageStorageDiffGenre[pointVal]["num"] += 1
            else:
                averageStorageDiffGenre[pointVal] = {"sum": point[1], "num": 1}


    # Calculate average for each century difference
    avgData = {}
    avgData["normal"] = {}
    avgData["normal"]["x"] = []
    avgData["normal"]["y"] = []
    # averageLineData2X = []
    # averageLineData2Y = []
    avgData["sg"] = {}
    avgData["sg"]["x"] = []
    avgData["sg"]["y"] = []
    avgData["dg"] = {}
    avgData["dg"]["x"] = []
    avgData["dg"]["y"] = []
    for i in range(maxPoint+1):
        if (i in averageStorage):
            avg = averageStorage[i]["sum"]/averageStorage[i]["num"]
            avgData["normal"]["x"].append(i)
            avgData["normal"]["y"].append(avg)

        # if (i in averageStorage2):
        #     avg = averageStorage2[i]["sum"]/averageStorage2[i]["num"]
        #     averageLineData2X.append(i)
        #     averageLineData2Y.append(avg)

        if (i in averageStorageSameGenre):
            avgSG = averageStorageSameGenre[i]["sum"]/averageStorageSameGenre[i]["num"]
            avgData["sg"]["x"].append(i)
            avgData["sg"]["y"].append(avgSG)

        if (i in averageStorageDiffGenre):
            avgDG = averageStorageDiffGenre[i]["sum"]/averageStorageDiffGenre[i]["num"]
            avgData["dg"]["x"].append(i)
            avgData["dg"]["y"].append(avgDG)

    # Calculate linear regression for points
    # slope, intercept, r_value, p_value, std_err

    slopePlusPData = []

    linRegData = {}
    for t in [("normal", allX, allY), ("sg", sgX, sgY), ("dg", dgX, dgY)]:
        name, datX, datY = t
        if (len(datX) > 0):


            # Fit using statsmodel
            ret = runRegression(datX, datY)
            slope, intercept, r2, fval, df, pval = ret


            #slope, intercept, _, pval, _ = linregress(datX, datY)
            linRegData[name] = {}
            linRegData[name]["x"] = [0, maxPoint]
            linRegData[name]["y"] = [intercept, intercept + slope*maxPoint]
            linRegData[name]["info"] = "Slope: %.6f" % slope

            slopePlusPData.append("  %s:" % (name))

            slopePlusPData.append("    slope: %.6f, intercept: %.6f" % (slope, intercept))
            slopePlusPData.append("    (R2=%.3e, F(%d)=%.3f, p=%.3e)" % (r2, df, fval, pval))


    # Run Regression on Genre only
    if (np.max(y) != np.min(y)):
        slope, intercept, r2, fval, df, pval = runRegression(y, allY)
        slopePlusPData.append("  Genre as independent var:")
        slopePlusPData.append("    slope: %.6f, intercept: %.6f" % (slope, intercept))
        slopePlusPData.append("    (R2=%.3e, F(%d)=%.3f, p=%.3e)" % (r2, df, fval, pval))

    utils.safeWrite(saveDir + fname + "_pslope.txt", "\n".join(slopePlusPData))

    #colorMap = plt.get_cmap("Set1")
    pctColors = getPercentColors(predefinedColors)
    colorMap = LinearSegmentedColormap.from_list("custom", pctColors, N=len(pctColors))

    # add some scatter to the x axis
    scatter = np.stack((0.3*(np.random.rand(data.shape[0]) - 0.5), np.zeros(data.shape[0])), axis=-1)
    Xfinal = data + scatter
    yFinal = y
    namesFinal = names

    lineList = [("normal", (0, 0, 0))]
    if separateGenres:
        lineList.append(("sg", pctColors[0]))
        lineList.append(("dg", pctColors[1]))

    if (showLinReg): # add linear regression info to labels
        legendLabels[0] = "%s (%s)" % (legendLabels[0], linRegData["sg"]["info"])
        if ("dg" in linRegData):
            legendLabels[1] = "%s (%s)" % (legendLabels[1], linRegData["dg"]["info"])
        legendLabels[2] = "%s (%s)" % (legendLabels[2], linRegData["normal"]["info"])


    for includeNames in [True, False]:
        fig = initStandardChart(saveOutput)
        fig.set_size_inches((11.), (6.8))

        colors = colorMap(yFinal)
        plt.scatter(Xfinal[:, 0], Xfinal[:, 1], s=9, c=colors, cmap=colorMap, alpha=0.6, linewidths=0)

        if (showAverage):
            # Averages
            for key, color in lineList:
                if key in avgData:
                    dat = avgData[key]
                    plt.plot(dat["x"], dat["y"], "-o", color=adjustColor(color, 0.8))

            # plt.plot(avgData["normal"]["x"], avgData["normal"]["y"], "k-o")
            # # plt.plot(averageLineData2X, averageLineData2Y, "-o", color="#888888")
            # plt.plot(avgData["sg"]["x"], avgData["sg"]["y"], "-o", color=adjustColor(pctColors[0], 0.8))
            # plt.plot(avgData["dg"]["x"], avgData["dg"]["y"], "-o", color=adjustColor(pctColors[1], 0.8))

        plt.xlabel('Centuries Between Authors')
        plt.ylabel('Similarity')

        xmin, xmax = plt.xlim()
        xscale = xmax - xmin

        if (ylim == None):
            ymin, ymax = plt.ylim()
        else:
            ymin = ylim[0]
            ymax = ylim[1]
            plt.ylim(ymin, ymax)

        yscale = ymax - ymin

        # if we include names, print them
        textSize = 1
        if (not(saveOutput)):
            textSize = 12
        if (includeNames):
            for i in range(len(Xfinal)):
                name = namesFinal[i]
                plt.text(Xfinal[i, 0], (Xfinal[i, 1] + 0.002*yscale),
                          name,
                          horizontalalignment='center', size=textSize)

        if (showLinReg):
            # Linear Regression
            for key, color in lineList:
                if key in linRegData:
                    dat = linRegData[key]
                    plt.plot(dat["x"], dat["y"], "-", color=adjustColor(color, 0.8))
                    #plt.text(dat["x"][-1] + 0.005*xscale, dat["y"][-1], dat["info"], horizontalalignment='left', size=textSize)

        patches = []
        colors = colorMap(range(len(legendLabels)))
        for i in legendOrder:
            patches.append(mpatches.Patch(color=colors[i], label=legendLabels[i]))
        plt.legend(handles=patches, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)


        margin = 0.05
        plt.subplots_adjust(left=0.1, right=0.99, top=0.92, bottom=0.1)

        # save or show the data
        if includeNames:
            labelText = "_labels"
        else:
            labelText = "_no_labels"
        filename = saveDir + fname + labelText + ".pdf"

        finishChart(saveOutput, filename)



# ==============================================================================
# ==============================================================================

# Run a 2D tSNE on the data
def tSNE_2D(dataSet, names, perplexity, saveOutput, saveDir, runtSNE, predefinedColors=[], verbose=True, useUMAP=False):
    X = dataSet.data
    y = dataSet.target[0]["target"]

    baseSaveDir = saveDir
    algorithmName = "tSNE"
    if (useUMAP):
        algorithmName = "umap"

    # if runtSNE is true, we compute the tSNE data from the start and save it.
    if (runtSNE):
        if (useUMAP):
            tsneX = umap.UMAP().fit_transform(X)
        else:
            tsneX = tsne.tsne(X, 2, X.shape[1], perplexity, verbose=verbose)
        filename = baseSaveDir + ("%s_2D_data.txt" % algorithmName)
        writeDat = {
            "x": tsneX.tolist(),
            "y": y.tolist(),
            "names": names
        }
        utils.safeWrite(filename, writeDat, True)
    else:
        tsneX = X

    # for each type of labeling, create a new version of the graph.
    for t in dataSet.target:
        saveDir = baseSaveDir + t["name"]
        yFinal = t["target"]
        for includeNames in [True, False]:
            fig = initStandardChart(saveOutput)

            Xfinal = tsneX
            namesFinal = names
            if (len(predefinedColors) > 0 and len(predefinedColors) == len(t["labels"])):
                pctColors = list(map(lambda c: list(map(lambda v: v/255.0, c)), predefinedColors))
                colorMap = LinearSegmentedColormap.from_list("custom", pctColors, N=len(predefinedColors))
                colors = colorMap(yFinal)
            elif len(t["labels"]) == 0:
                colorMap = plt.get_cmap("tab20")
                colors = yFinal
            elif len(t["labels"]) > 9:
                colorMap = plt.get_cmap("Paired")
                colors = colorMap(yFinal)
            else:
                colorMap = plt.get_cmap("Set1")
                colors = colorMap(yFinal)
            plt.scatter(Xfinal[:, 0], Xfinal[:, 1], s=49, c=colors, cmap=colorMap)

            ymin, ymax = plt.ylim()
            yscale = ymax - ymin

            # if we include names, print them
            if (includeNames):
                for i in range(len(Xfinal)):
                    name = namesFinal[i]
                    plt.text(Xfinal[i, 0], (Xfinal[i, 1] + 0.015*yscale),
                              name,
                              horizontalalignment='center', size=8)


            # add in legend
            if len(t["labels"]) > 0:
                patches = []
                legendLabels = t["labels"]
                colors = colorMap(range(len(legendLabels)))
                for i, c in enumerate(colors):
                    patches.append(mpatches.Patch(color=c, label=legendLabels[i]))
                plt.legend(handles=patches, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)

            # save or show the data
            if includeNames:
                labelText = "_labels"
            else:
                labelText = "_no_labels"
            filename = saveDir + algorithmName + "_2D" + labelText + ".pdf"

            finishChart(saveOutput, filename)

# Run a tsne with two different labels, one for dot fill and one for dot stroke.
def tSNE_2D_2color(dataSet, names, perplexity, saveOutput, saveDir, runtSNE, useUMAP=False):
    X = dataSet.data
    y = dataSet.target[0]["target"]

    baseSaveDir = saveDir
    algorithmName = "tSNE"
    if (useUMAP):
        algorithmName = "umap"

    # if tsne was not provided, save the information.
    if (runtSNE):
        if (useUMAP):
            tsneX = umap.UMAP().fit_transform(X)
        else:
            tsneX = tsne.tsne(X, 2, X.shape[1], perplexity)
        filename = baseSaveDir + ("%s_2D_data.txt" % algorithmName)

        writeDat = {
            "x": tsneX.tolist(),
            "y": y.tolist(),
            "names": names
        }
        utils.safeWrite(filename, writeDat, True)
    else:
        tsneX = X

    t = dataSet.target[2] #2 dataSet.target[2]["target"]
    t2 = dataSet.target[4]
    saveDir = baseSaveDir + "narrowgen_x_timeframe_"
    yFinal = t["target"]
    for includeNames in [True, False]:
        fig = initStandardChart(saveOutput)

        Xfinal = tsneX
        namesFinal = names
        if len(t["labels"]) == 0:
            colorMap = plt.get_cmap("tab20")
            colors = yFinal
        elif len(t["labels"]) > 9:
            colorMap = plt.get_cmap("Paired")
            colors = colorMap(yFinal)
            colorMap2 = plt.get_cmap("Set1")
            edgeColors = colorMap2(t2["target"])
        else:
            colorMap = plt.get_cmap("Set1")
            colors = colorMap(yFinal)
            colorMap2 = plt.get_cmap("tab20")
            edgeColors = colorMap2(t2["target"])
        plt.scatter(Xfinal[:, 0], Xfinal[:, 1], s=49, c=colors, cmap=colorMap, edgecolors=edgeColors)

        ymin, ymax = plt.ylim()
        yscale = ymax - ymin

        # if we include names, print them
        if (includeNames):
            for i in range(len(Xfinal)):
                name = namesFinal[i]
                plt.text(Xfinal[i, 0], (Xfinal[i, 1] + 0.015*yscale),
                          name,
                          horizontalalignment='center', size=8)


        # add in legend
        patches = []
        if len(t["labels"]) > 0:
            legendLabels = t["labels"]
            colors = colorMap(range(len(legendLabels)))
            for i, c in enumerate(colors):
                patches.append(mpatches.Patch(color=c, label=legendLabels[i]))
        if len(t2["labels"]) > 0:
            legendLabels2 = t2["labels"]
            colors2 = colorMap2(range(len(legendLabels2)))
            for i, c in enumerate(colors2):
                patches.append(mpatches.Patch(color=c, label=legendLabels2[i]))

        plt.legend(handles=patches, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)

        # save or show the data
        if includeNames:
            labelText = "_labels"
        else:
            labelText = "_no_labels"
        filename = saveDir + algorithmName + "_2D_2color" + labelText + ".pdf"

        finishChart(saveOutput, filename)


# create a tSNE with clickable icons
def clickable_tSNE_2D(dataSet, names, perplexity, saveDir, runtSNE, useUMAP=False):
    X = dataSet.data
    y = dataSet.target[0]["target"]

    baseSaveDir = saveDir
    algorithmName = "tSNE"
    if (useUMAP):
        algorithmName = "umap"

    # if tsne was not provided, save the information.
    if (runtSNE):
        if (useUMAP):
            tsneX = umap.UMAP().fit_transform(X)
        else:
            tsneX = tsne.tsne(X, 2, X.shape[1], perplexity)
        filename = baseSaveDir + ("%s_2D_data.txt" % algorithmName)

        writeDat = {
            "x": tsneX.tolist(),
            "y": y.tolist(),
            "names": names
        }
        utils.safeWrite(filename, writeDat, True)
    else:
        tsneX = X

    for t in dataSet.target:
        # set figure size

        fig, ax = plt.subplots()

        yFinal = t["target"]
        Xfinal = tsneX
        namesFinal = names
        if len(t["labels"]) == 0:
            colorMap = plt.get_cmap("tab20")
            colors = yFinal
        elif len(t["labels"]) > 9:
            colorMap = plt.get_cmap("Paired")
            colors = colorMap(yFinal)
        else:
            colorMap = plt.get_cmap("Set1")
            colors = colorMap(yFinal)

        scat = plt.scatter(Xfinal[:, 0], Xfinal[:, 1], s=49, c=colors, cmap=colorMap, edgecolor='black', linewidth=0.7, picker=True)

        # add in legend
        if len(t["labels"]) > 0:
            patches = []
            legendLabels = t["labels"]
            legendColors = colorMap(range(len(legendLabels)))
            for i, c in enumerate(legendColors):
                patches.append(mpatches.Patch(color=c, label=legendLabels[i]))
            plt.legend(handles=patches, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)


        # annot adapted from https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib
        annot = ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        # get labels for each point
        pointCategories = []
        for y in yFinal:
            cats = []
            for cat in dataSet.target:
                if(len(cat["labels"]) > 0):
                    cats.append(cat["labels"][y])
            pointCategories.append(", ".join(cats))
        pointLabels = list(map(lambda x: "%s: %s" % x, list(zip(namesFinal, pointCategories))))
        def update_annot(ind):
            # get central position of points
            pos = [0, 0]
            for i in ind:
                posI = scat.get_offsets()[i]
                pos[0] += posI[0]
                pos[1] += posI[1]
            pos[0] = pos[0]/len(ind)
            pos[1] = pos[1]/len(ind)
            annot.xy = pos
            textParts = [pointLabels[i] for i in ind]
            text = "\n".join(textParts)
            annot.set_text(text)
            annot.get_bbox_patch().set_alpha(0.9)

        pickX = Xfinal[:, 0]
        pickY = Xfinal[:, 1]
        annotationOn = np.zeros(pickY.shape)
        def on_pick(event):
            #artist = event.artist
            #xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
            update_annot(event.ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()

        fig.canvas.callbacks.connect('pick_event', on_pick)


        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

        plt.show()
        plt.close()

# create four tSNEs
# highlightAuthor is true if we want to highlight a single author.
def tSNE_2D_4Up(dataSet, names, highlightAuthor, saveOutput, saveDir, fname, runtSNE, useUMAP=False):
    X = dataSet.data
    y = dataSet.target[0]["target"]

    baseSaveDir = saveDir
    algorithmName = "tSNE"
    if (useUMAP):
        algorithmName = "umap"

    # if tsne was not provided, save the information.
    if (runtSNE):
        if (useUMAP):
            tsneX = umap.UMAP().fit_transform(X)
        else:
            tsneX = tsne.tsne(X, 2, X.shape[1], perplexity,)
        filename = baseSaveDir + ("%s_2D_data.txt" % algorithmName)
        writeDat = {
            "x": tsneX.tolist(),
            "y": y.tolist(),
            "names": names
        }
        utils.safeWrite(filename, writeDat, True)
    else:
        tsneX = X


    #for t in dataSet.target:
    fig, axarr = plt.subplots(2, 2)

    # set figure size
    if saveOutput:
        if (highlightAuthor):
            fig.set_size_inches((6), (8))
        else:
            fig.set_size_inches((7), (9))

    for i, ax in enumerate([axarr[0, 0], axarr[0, 1], axarr[1, 0], axarr[1, 1]]):
        t = dataSet.target[i]

        yFinal = t["target"]
        Xfinal = tsneX
        namesFinal = names
        if (highlightAuthor):
            colorMap = plt.get_cmap("Set1")
        else:
            colorMaps = [plt.get_cmap("Set1"), plt.get_cmap("Paired"), plt.get_cmap("Set2"), plt.get_cmap("tab10")]
            colorMap = colorMaps[i]
        colors = yFinal

        # add targets to sort
        if (highlightAuthor):
            targ = yFinal.reshape((yFinal.shape[0], 1))
            Xfinal = np.append(Xfinal, targ, axis=1)
            Xfinal = Xfinal[np.argsort(targ+0, axis=0).reshape((targ.shape[0]))]

            Xfinal = np.flipud(Xfinal)
            colors = np.flipud(np.sort(colors))

            colorsFinal = colorMap(colors*7+1)
        else:
            colorsFinal = colorMap(colors)

        scat = ax.scatter(Xfinal[:, 0], Xfinal[:, 1], s=16, c=colorsFinal, picker=True)

        # add in legend
        # skip broad genre (i == 1)
        if len(t["labels"]) > 0 and (highlightAuthor or i != 1):
            patches = []
            legendLabels = t["labels"]
            if (highlightAuthor):
                legendColors = colorMap([1, 8])
            else:
                legendColors = colorMap(range(len(legendLabels)))
            for i, c in enumerate(legendColors):
                patches.append(mpatches.Patch(color=c, label=legendLabels[i]))
            ax.legend(handles=patches, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)

        # no need for axes
        ax.set_xticks([])
        ax.set_yticks([])


    if (highlightAuthor):
        plt.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01, wspace=0.02, hspace=0.15)
    else:
        plt.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01, wspace=0.02, hspace=0.25)

    if (useUMAP):
        filename = saveDir + fname + "_umap.pdf"
    else:
        filename = saveDir + fname + ".pdf"

    finishChart(saveOutput, filename)


# ==============================================================================
# ==============================================================================

# Create a comparison histogram between two categories
def comparisonHistogram(data, dataErr, dataLabels, tickLabels, title, axLabel, saveDir, saveName, saveOutput, color=None):
    N = len(data[0])
    numBars = len(data)

    numWordsScale = len(tickLabels)/50
    numCatsScale = len(dataLabels)/2

    ind = np.arange(N)  # the x locations for the groups
    width = .7/numBars  # the width of the bars

    fig, ax = plt.subplots()

    if saveOutput:
        fig.set_size_inches((8.5), (11*numWordsScale*numCatsScale))

    # add some text for labels, title and axes ticks
    ax.set_xlabel(axLabel)
    ax.set_title(title)
    ax.set_yticks(ind + width / 2)
    ax.set_yticklabels(tickLabels)

    legendRects = []
    colors = plt.get_cmap("Set1")
    startXPos = ind - width*(numBars/2 - 1)
    for i in range(len(data)):
        d = data[i]
        xPos = startXPos + width*(i)
        if (color == None):
            c = colors(i)
        else:
            c = getPercentColors([color])[0]
        rects = ax.barh(xPos, data[i], width, color=c, xerr=dataErr[i])
        legendRects.append(rects)

    ax.legend(legendRects, dataLabels)

    filename = saveDir + saveName + ".pdf"

    finishChart(saveOutput, filename)


# Graph each author by how often they use words from a certain word group
def authorWordUseHistogram(data, dataLabels, tickLabels, title, axLabel, saveDir, saveName, saveOutput, color=None):
    N = len(data)
    numBars = 1

    ind = np.arange(N)  # the x locations for the groups
    width = 0.9/numBars  # the width of the bars

    fig, ax = plt.subplots()

    if saveOutput:
        fig.set_size_inches((8.5), (11))

    # add some text for labels, title and axes ticks
    ax.set_xlabel(axLabel)
    ax.set_title(title)
    ax.set_yticks(ind + width / 2)
    ax.set_yticklabels(tickLabels, fontdict={'fontsize': 8})

    legendRects = []
    colors = plt.get_cmap("Set1")
    startXPos = ind - width*(numBars/2 - 1)

    xPos = startXPos
    if (color == None):
        c = colors(i)
    else:
        c = getPercentColors([color])[0]
    rects = ax.barh(xPos, data, width, color=c)
    legendRects.append(rects)

    ax.legend(legendRects, dataLabels)

    plt.subplots_adjust(left=0.19, right=0.99, bottom=0.05, top=0.95)

    filename = saveDir + saveName + ".pdf"

    finishChart(saveOutput, filename)




# freqData is a list of texts, where each text is a list of word frequencies for that text
# dataLabels contains the names of the texts
# wordLabels is the words being used
# dists contains [name, vals] pairs, where the name is the name of the distance metric
#       and val is the change from baseline with each word removed
# If saveOutput is true, save it at saveDir + saveName + ".pdf"
def wordImportanceComparison(freqData, dataLabels, wordLabels, dists, saveDir, saveName, saveOutput):
    N = len(freqData[0])
    numBars = len(freqData)

    numRows = 2
    numCols = N + 1

    widthScale = numCols/6

    ind = np.arange(1)  # the x locations for the groups
    width = .7/numBars  # the width of the bars

    #fig, axs = plt.subplots(2, 1+N, sharey=True)

    fig, _ = plt.subplots()

    colors = plt.get_cmap("Set1")

    firstPlot = True
    legendRects = []
    baseYTickLabels = None

    # set up leftmost, empty plot
    ax0 = plt.subplot(numRows, numCols, 1)
    ax0.set_xlim(0,width*numBars)
    ax0.axis('off')

    firstAx = None
    # set up chart for each word
    for i in range(N):
        if firstPlot:
            ax = plt.subplot(numRows, numCols, i+2)
            firstAx = ax
        else:
            ax = plt.subplot(numRows, numCols, i+2, sharey = firstAx)
        # add some text for labels, title and axes ticks
        ax.set_title(wordLabels[i])

        legendRects = []
        startXPos = width/2
        for j in range(numBars):
            xPos = startXPos + width*(j)
            rects = ax.bar(xPos, freqData[j][i], width, color=colors(j))
            if firstPlot:
                legendRects.append(rects)


        if firstPlot:
            # add the legend
            ax0.legend(legendRects, dataLabels, loc="center left", bbox_to_anchor=(0, 0.5), borderaxespad=0.)
            firstPlot = False
        else:
            # hide the ticks
            plt.setp(ax.get_yticklabels(), visible=False)

        ax.set_xticks([])


    # set up leftmost plot, with names of metrics
    ax0 = plt.subplot(numRows, numCols, numCols+1)#axs[1][0]
    ax0.set_xlim(0,2)
    ax0.set_ylim(-1, 0)

    labels = map(lambda x: x["name"], dists)
    rowLabels = "index\n\n" + "\n\n\n".join(labels)
    ax0.text(2, 0, rowLabels, fontsize=10, va="top", linespacing=1.8, ha="right", family="monospace")
    ax0.axis('off')

    # set up info for each word
    for i in range(N):
        ax = plt.subplot(numRows, numCols, numCols+i+2)
        ax.set_xlim(0,2)
        ax.set_ylim(-1,0)

        scores = list(map(lambda x: x["vals"][i], dists))
        labels = []
        # show index
        labels.append("%d\n" % (i + 1))
        for s in scores:
            labels.append("%0.6f" % s[0])
            labels.append("%0.6f\n" % s[1])
        ax.text(1, 0, "\n".join(labels), fontsize=10, va="top", linespacing=1.8, ha="center", family="monospace")

        ax.axis('off')

    margin = 0.05/widthScale
    plt.subplots_adjust(left=margin, right=(1-margin), hspace=0.05)

    if saveOutput:
        fig.set_size_inches((8.5*widthScale), (11))
    filename = saveDir + saveName + ".pdf"
    finishChart(saveOutput, filename)


# Create a bar chart showing the frequency of an author's usage of various words or groups of words
def wordUseBarChart(counts, colors, yHeight, groupLabels, title, saveName):
    fig, ax = plt.subplots()
    x = np.arange(len(counts)) + 1

    fig.set_size_inches((3), (3))

    bars = plt.bar(x, counts)

    pctColors = getPercentColors(colors)

    for i, bar in enumerate(bars):
        bar.set_facecolor(pctColors[i])

    # add some text for labels, title and axes ticks
    ax.set_xlabel("Group")
    ax.set_ylabel("Frequency")
    ax.set_title(title)
    plt.xticks(x, groupLabels, rotation=45)

    ax.title.set_fontsize(10)
    for item in [ax.xaxis.label, ax.yaxis.label]:
        item.set_fontsize(10)

    for item in (ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(8)


    ax.set_ylim(0, yHeight)

    fig.tight_layout()
    filename = saveName + ".pdf"

    finishChart(True, filename)

# Put four word use bar charts on one plot
def wordUseBarChart4Up(counts4, colors, yHeight, groupLabels, title4, saveName):
    counts = counts4[0]
    title = title4[0]
    #fig, ax = plt.subplots()
    fig, axarr = plt.subplots(2, 2)

    fig.set_size_inches((7), (7))


    pctColors = getPercentColors(colors)

    for i, ax in enumerate([axarr[0, 0], axarr[0, 1], axarr[1, 0], axarr[1, 1]]):
        counts = counts4[i]
        title = title4[i]

        x = np.arange(len(counts)) + 1

        bars = ax.bar(x, counts)


        for j, bar in enumerate(bars):
            bar.set_facecolor(pctColors[j])

        # add some text for labels, title and axes ticks
        if (i >= 2):
            ax.set_xlabel("Group")
        if (i % 2 == 0):
            ax.set_ylabel("Frequency")
        ax.set_title(title)
        plt.sca(ax)
        plt.xticks(x, groupLabels, rotation=45)

        ax.title.set_fontsize(10)
        for item in [ax.xaxis.label, ax.yaxis.label]:
            item.set_fontsize(10)

        for item in (ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(8)


        ax.set_ylim(0, yHeight)

    fig.tight_layout()
    filename = saveName + ".pdf"

    finishChart(True, filename)

# Put eight word use bar charts on one plot
def wordUseBarChart8Up(counts8, colors, yHeight, groupLabels, title8, saveName):
    counts = counts8[0]
    title = title8[0]
    #fig, ax = plt.subplots()
    fig, axarr = plt.subplots(4, 2)

    fig.set_size_inches((6), (10))


    pctColors = getPercentColors(colors)

    for i, ax in enumerate([axarr[0, 0], axarr[0, 1], axarr[1, 0], axarr[1, 1], axarr[2, 0], axarr[2, 1], axarr[3, 0], axarr[3, 1]]):
        counts = counts8[i]
        title = title8[i]

        x = np.arange(len(counts)) + 1

        bars = ax.bar(x, counts)


        for j, bar in enumerate(bars):
            bar.set_facecolor(pctColors[j])

        # add some text for labels, title and axes ticks
        # if (i >= 6):
        #     ax.set_xlabel("Group")
        if (i % 2 == 0):
            ax.set_ylabel("Frequency")
        ax.set_title(title)
        plt.sca(ax)
        plt.xticks(x, groupLabels, rotation=45)

        ax.title.set_fontsize(10)
        for item in [ax.xaxis.label, ax.yaxis.label]:
            item.set_fontsize(10)

        for item in (ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(8)


        ax.set_ylim(0, yHeight)

    fig.tight_layout()
    filename = saveName + ".pdf"

    finishChart(True, filename)

# Create a line chart
def lineChart(x, y, saveOutput, saveDir, name, allLines=[], xLim=None, yLim=[0, 100], log=False, yAdjust=0):
    fig = initStandardChart(saveOutput)


    minAbsY = 100; # all values should be at most -1
    for line in allLines:
        pairName = line[0]
        ydat = line[1]
        if (ydat[0] + yAdjust != 0): # linthreshy cannot be 0
            minAbsY = min(minAbsY, abs(ydat[0] + yAdjust))
        if (ydat[-1] + yAdjust != 0):
            minAbsY = min(minAbsY, abs(ydat[-1] + yAdjust))
        plt.plot(x, np.array(ydat) + yAdjust, 'k-', lw=1, alpha=0.05)

    for label, ydat in y:
        if (ydat[0] + yAdjust != 0): # linthreshy cannot be 0
            minAbsY = min(minAbsY, abs(ydat[0] + yAdjust))
        if (ydat[-1] + yAdjust != 0):
            minAbsY = min(minAbsY, abs(ydat[-1] + yAdjust))
        plt.plot(x, np.array(ydat) + yAdjust, '-', lw=2, label=label)

    plt.xlim(x[0], x[-1])

    if (yLim != None):
        plt.ylim(yLim[0], yLim[1])

    logStr = ""
    if (log):
        print(abs(minAbsY))
        plt.yscale('symlog', linthreshy=abs(minAbsY))
        # ymin, ymax = plt.ylim()
        # t = np.arange(ymin, ymax, (ymax-ymin)/10.0)
        #
        # plt.semilogy(t, np.exp(-t/5.0))

        logStr = "-log"

    filename = saveDir + name + logStr + ".pdf"

    plt.legend()

    finishChart(saveOutput, filename)


# Create a 4up line chart
def lineChart4Up(x, y, saveOutput, saveDir, name, allLines=[], xLim=None, yLim=[0, 100], log=False, yAdjust=0):
    fig = initStandardChart(saveOutput)

    fig, axarr = plt.subplots(2, 2)

    if len(allLines) == 0:
        allLines = [[], [], [], []]

    # set figure size
    if saveOutput:
        fig.set_size_inches((7), (9))

    for i, ax in enumerate([axarr[0, 0], axarr[0, 1], axarr[1, 0], axarr[1, 1]]):
        minAbsY = 100; # all values should be at most -1
        for line in allLines[i]:
            pairName = line[0]
            ydat = line[1]
            if (ydat[0] + yAdjust != 0): # linthreshy cannot be 0
                minAbsY = min(minAbsY, abs(ydat[0] + yAdjust))
            if (ydat[-1] + yAdjust != 0):
                minAbsY = min(minAbsY, abs(ydat[-1] + yAdjust))
            ax.plot(x, np.array(ydat) + yAdjust, 'k-', lw=1, alpha=0.05)

        for label, ydat in y[i]:
            if (ydat[0] + yAdjust != 0): # linthreshy cannot be 0
                minAbsY = min(minAbsY, abs(ydat[0] + yAdjust))
            if (ydat[-1] + yAdjust != 0):
                minAbsY = min(minAbsY, abs(ydat[-1] + yAdjust))
            ax.plot(x, np.array(ydat) + yAdjust, '-', lw=2, label=label)

        ax.set_xlim(x[0], x[-1])

        if (yLim != None):
            ax.set_ylim(yLim[0], yLim[1])

        logStr = ""
        if (log):
            print(abs(minAbsY))
            ax.yscale('symlog', linthreshy=abs(minAbsY))
            # ymin, ymax = plt.ylim()
            # t = np.arange(ymin, ymax, (ymax-ymin)/10.0)
            #
            # plt.semilogy(t, np.exp(-t/5.0))

            logStr = "-log"




        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=1, mode="expand", borderaxespad=0.)


    plt.subplots_adjust(left=0.08, right=0.99, top=0.91, bottom=0.03, wspace=0.25, hspace=0.35)
    filename = saveDir + name + logStr + ".pdf"
    finishChart(saveOutput, filename)

# Special line chart for comparing word usage
def compareWordUsageChart(y, saveOutput, saveDir, name, allLines=[], xLim=None, yLim=None, log=False, yAdjust=0):
    fig = initStandardChart(saveOutput)
    fig.set_size_inches((8.), (6.))

    # calculate x axis points
    _, _, l = y[0]
    x = list(range(len(l)))

    minAbsY = 100; # all values should be at most -1
    for line in allLines:
        pairName = line[0]
        color = line[1]
        ydat = line[2]
        if (ydat[0] + yAdjust != 0): # linthreshy cannot be 0
            minAbsY = min(minAbsY, abs(ydat[0] + yAdjust))
        if (ydat[-1] + yAdjust != 0):
            minAbsY = min(minAbsY, abs(ydat[-1] + yAdjust))
        plt.plot(x, np.array(ydat) + yAdjust, color, lw=1, alpha=0.05)

    for label, color, ydat in y:
        if (ydat[0] + yAdjust != 0): # linthreshy cannot be 0
            minAbsY = min(minAbsY, abs(ydat[0] + yAdjust))
        if (ydat[-1] + yAdjust != 0):
            minAbsY = min(minAbsY, abs(ydat[-1] + yAdjust))
        plt.plot(x, np.array(ydat) + yAdjust, '-', lw=2, label=label)

    plt.xlim(x[0], x[-1])

    if (yLim != None):
        plt.ylim(yLim[0], yLim[1])

    plt.xlabel("Number of Top Words Ignored")
    plt.ylabel("Similarity")

    logStr = ""
    if (log):
        print(abs(minAbsY))
        plt.yscale('symlog', linthreshy=abs(minAbsY))
        # ymin, ymax = plt.ylim()
        # t = np.arange(ymin, ymax, (ymax-ymin)/10.0)
        #
        # plt.semilogy(t, np.exp(-t/5.0))

        logStr = "-log"

    filename = saveDir + name + logStr + ".pdf"

    plt.legend()

    finishChart(saveOutput, filename)


# Create a line chart showing a metric's performance
def metricIntuitionChart(y, saveOutput, saveDir, name, boundries=[], allLines=[], yLim=None):
    x = np.array(range(len(y[0][1])))*100/len(y[0][1])
    yAdjust = 0

    heights = [0]
    if (saveOutput):
        heights = [3., 5.]

    for height in heights:
        fig = initStandardChart(saveOutput)

        # Add extra lines
        for line in allLines:
            pairName = line[0]
            ydat = line[1]
            plt.plot(x, np.array(ydat), 'k-', lw=1, alpha=0.2)




        for label, ydat in y:
            plt.plot(x, np.array(ydat), '-', lw=2, label=label)
            plt.plot(x[0], ydat[0], 'k-', lw=1, alpha=0.2, label="Individual Runs")

        # Add boundries
        for line in boundries:
            pairName = line[0]
            yval = line[1]
            plt.plot([x[0], x[-1]], [yval, yval], '--', lw=1, label=pairName)


        plt.xlim(x[0], x[-1])

        if (yLim != None):
            plt.ylim(yLim[0], yLim[1])

        plt.xlabel("% Swapped")
        plt.ylabel("Similarity")

        plt.legend()

        fig.tight_layout()

        plt.subplots_adjust(left=0.11, bottom=0.1*(5./height), right=0.97, top=0.97)

        if (saveOutput):
            fig.set_size_inches((8.), (height))

        filename = "%s%s_%d.pdf" % (saveDir, name, height)
        finishChart(saveOutput, filename)



# create a basic regression
def basicRegression(data, names, xlabels, saveOutput, saveDir, fname="regression", ylim=None):
    ylab = "Overall Similarity"

    regLineColor = (0, 0, 0)

    legendLabels = []
    linRegDatas = []
    slopePlusPData = []

    namesFinal = names

    upperY = 0
    lowerY = 1
    for i, _ in enumerate(data):
        subData = data[i]
        legendLabel = "Best Fit"
        xlabel = xlabels[i]

        maxX = 0
        minX = 1

        maxY = 0
        minY = 1

        # store x and y values for points, as well as for points separated by same/different genre
        allX = []
        allY = []
        for i, point in enumerate(subData):
            xVal = point[0]
            if xVal > maxX:
                maxX = xVal
            if xVal < minX:
                minX = xVal

            yVal = point[1]
            if yVal > maxY:
                maxY = yVal
            if yVal < minY:
                minY = yVal

            allX.append(xVal)
            allY.append(yVal)

        if minY < lowerY:
            lowerY = minY
        if maxY > upperY:
            upperY = maxY

        # Calculate linear regression for points
        # slope, intercept, r_value, p_value, std_err
        linRegData = {}
        name, datX, datY = ("normal", allX, allY)
        if (len(datX) > 0):
            linRegData[name] = {}
            slope, intercept, _, pval, _ = linregress(datX, datY)
            linRegData[name]["x"] = [minX, maxX]
            linRegData[name]["y"] = [intercept + slope*minX, intercept + slope*maxX]
            linRegData[name]["info"] = "Slope: %.6f" % slope

            slopePlusPData.append("  %s:\n    slope: %.6f, p: %.6E" % (xlabel, slope, pval))

        linRegDatas.append(linRegData)

        legendLabel = "%s (%s)" % (legendLabel, linRegData["normal"]["info"])
        legendLabels.append(legendLabel)

    #utils.safeWrite(saveDir + fname + "_pslope.txt", "\n".join(slopePlusPData))

    for includeNames in [True, False]:
        # fig = initStandardChart(saveOutput)
        #fig, ax = plt.subplots()
        fig, axarr = plt.subplots(1, 2)

        fig.set_size_inches((8.), (4))

        plt.subplots_adjust(wspace=0.4)

        for i, ax in enumerate([axarr[0], axarr[1]]):
            Xfinal = np.array(data[i])
            namesFinal = names[i]
            xlab = xlabels[i]
            legendLabel = legendLabels[i]
            linRegData = linRegDatas[i]

            # colors = colorMap(yFinal) , c=colors
            ax.scatter(Xfinal[:, 0], Xfinal[:, 1], s=9, alpha=0.6, linewidths=0)

            ax.set_xlabel(ylab)
            ax.set_ylabel(xlab)

            xmin, xmax = ax.set_xlim()
            xscale = xmax - xmin

            if (ylim == None):
                # ymin = lowerY
                # ymax = upperY + .002
                # ax.set_ylim(ymin, ymax)
                ymin, ymax = ax.set_ylim()
            else:
                ymin = ylim[0]
                ymax = ylim[1]
                ax.set_ylim(ymin, ymax)

            yscale = ymax - ymin

            # if we include names, print them
            textSize = 3
            if (not(saveOutput)):
                textSize = 12
            if (includeNames):
                for i in range(len(Xfinal)):
                    name = namesFinal[i]
                    ax.text(Xfinal[i, 0], (Xfinal[i, 1] + 0.005*yscale),
                              name,
                              horizontalalignment='center', size=textSize)

            # Linear Regression
            dat = linRegData["normal"]
            ax.plot(dat["x"], dat["y"], "-", color=adjustColor(regLineColor, 0.8))

            patches = []
            patches.append(mpatches.Patch(color=regLineColor, label=legendLabel))
            ax.legend(handles=patches, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)


        # save or show the data
        if includeNames:
            labelText = "_labels"
        else:
            labelText = "_no_labels"
        filename = saveDir + fname + labelText + ".pdf"

        finishChart(saveOutput, filename)
