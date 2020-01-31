# -*- coding: utf-8 -*-
# Use some light machine learning to predict various categories for authors and segments
import re
import copy

import numpy as np

import utils
import mainParams as mp
import genre
from getWordCounts import loadWCData
from makeBasicGraphs import normalizeFeatures


from sklearn.model_selection import KFold, GroupKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB

# ==============================================================================
# ==============================================================================

# Random state for KFold, to maintain state. First written at 9:02 pm.
KFOLD_RANDOM = 902


# calculate accuracy given predictions and ground truth
def calculateAccuracy(preds, truth):
    return np.mean(preds==truth)


# Pick the majority class label from the train data and guess that label.
def majorityClass(X, y, splits, saveDir):
    accs = []
    for train_index, test_index in splits:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # Calculate mode
        # Source: https://stackoverflow.com/questions/6252280/find-the-most-frequent-number-in-a-numpy-vector
        maj_label = np.argmax(np.bincount(y_train))

        predictions = np.full((X_test.shape[0]), maj_label)

        acc = calculateAccuracy(predictions, y_test)

        accs.append(acc)

    return "  %f - Majority Class" % np.mean(accs)


# Choose labels using a KNN algorithm
def knn(X, y, splits, saveDir):
    accs = []
    bestKs = []
    for train_index, test_index in splits:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        best_k = -1
        best_acc = 0
        # find best k by splitting the train set into train and dev
        for k in [1, 2, 3, 5, 10, 20]:
            kf = KFold(n_splits=5, shuffle=True, random_state=KFOLD_RANDOM)
            dev_splits = list(kf.split(X_train))

            trains, devs = dev_splits[0]

            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(X_train[trains], y_train[trains])
            predictions = knn.predict(X_train[devs])
            dev_acc = calculateAccuracy(predictions, y_train[devs])
            if dev_acc > best_acc:
                best_k = k
                best_acc = dev_acc

        # Fit a KNN to the whole train set using best k value
        knn = KNeighborsClassifier(n_neighbors=best_k)
        knn.fit(X_train, y_train)
        predictions = knn.predict(X_test)

        acc = calculateAccuracy(predictions, y_test)

        bestKs.append("%d" % best_k)
        accs.append(acc)


    return "  %f - KNN (k = %s)" % (np.mean(accs), ", ".join(bestKs))


# Choose labels using the naive bayes algorithm.
def naiveBayes(X, y, splits, saveDir):
    accs = []
    for train_index, test_index in splits:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # No smoothing
        nb = MultinomialNB()
        nb.fit(X_train, y_train)
        predictions = nb.predict(X_test)

        acc = calculateAccuracy(predictions, y_test)

        accs.append(acc)

    return "  %f - Naive Bayes" % np.mean(accs)


# given data, target, and names, run all ML algorithms
def runMLAlgorithms(X, tokens, y, groups, type_name, category_name, saveDir):
    X = np.array(X)
    y = np.array(y)

    # get word counts for naive bayes
    counts = []
    for i in range(len(X)):
        counts.append(X[i]*tokens[i])
    counts = np.array(counts)

    # 9 splits yields ~10 test authors per fold
    kf = GroupKFold(n_splits=9)

    # Ensure no work has books (segments) in both the training and test set.
    splits = list(kf.split(X, None, groups))

    output = []
    output.append("Average results for %s (%s) across %d folds:" % (category_name, type_name, len(splits)))

    # Run Majority Class
    output.append(majorityClass(X, y, splits, saveDir))

    # Run KNN
    output.append(knn(X, y, splits, saveDir))

    # Run Naive Bayes
    try:
        output.append(naiveBayes(counts, y, splits, saveDir))
    except ValueError:
        output.append("  Failed    - Naive Bayes")



    fname = saveDir + "res_%s_%s.txt" % (category_name, type_name)
    utils.safeWrite(fname, "\n".join(output))


# Make predictions for all categories with all machine learning algorithms
def makeAllPredictions(authors, books, topWords, saveDir):
    saveDir += "dataPreds/"
    # Gather data
    # ==== Calculate data info
    a_typeName = "Authors"
    b_typeName = "Books"

    # aggregate features for each author into one dataSet
    a_data = []
    a_tokens = []
    a_groups = []
    for i in range(len(authors)):
        author = authors[i]
        a_data.append(author.featureData[:-1]) # final item is the count for all other words
        a_tokens.append(author.totalTokenCount)
        a_groups.append(author.authorName)

    # aggregate features for each book
    b_data = []
    b_target = []
    b_tokens = []
    b_groups = []
    b_groups_2 = []
    for i, book in enumerate(books):
        if (book.numTokens >= mp.MIN_TOKENS_NECESSARY):
            b_data.append(book.featureData[:-1]) # final item is the count for all other words
            b_tokens.append(book.numTokens)
            b_groups.append(book.textName)
            b_groups_2.append(i)

    namesToIndex = {}
    for i, author in enumerate(authors):
        namesToIndex[author.authorName] = i

    workToIndex = {}
    index = 0
    for i, book in enumerate(books):
        if not(book.textName in workToIndex):
            workToIndex[book.textName] = index
            index += 1

    # we predict genre, timeframe, and dialect
    predictionTypes = [
        ("genre", genre.namesToGenre),
        ("timeframe", genre.namesToTimeframe),
        ("dialect", genre.namesToDialect),
    ]

    for p in predictionTypes:
        name, convert = p

        a_target = []
        for author in authors:
            a_target.append(convert[author.authorName])
        runMLAlgorithms(a_data, a_tokens, a_target, a_groups, a_typeName, name, saveDir)



    # for books, add author prediction.
    predictionTypes.append(("author", namesToIndex))

    # Predictions without segments from a work in both training and test.
    for p in predictionTypes:
        name, convert = p

        b_target = []
        for book in books:
            if (book.numTokens < mp.MIN_TOKENS_NECESSARY):
                continue
            b_target.append(convert[book.author])

        runMLAlgorithms(b_data, b_tokens, b_target, b_groups, b_typeName, name, saveDir)

    # Predictions with segments from a work in both training and test.
    for p in predictionTypes:
        name, convert = p

        b_target = []
        for book in books:
            if (book.numTokens < mp.MIN_TOKENS_NECESSARY):
                continue
            b_target.append(convert[book.author])

        runMLAlgorithms(b_data, b_tokens, b_target, b_groups_2, b_typeName + "_2", name, saveDir)

    # Predict works as well
    for p in predictionTypes:
        b_target = []
        for book in books:
            if (book.numTokens < mp.MIN_TOKENS_NECESSARY):
                continue
            b_target.append(workToIndex[book.textName])

        runMLAlgorithms(b_data, b_tokens, b_target, b_groups_2, b_typeName + "_2", "work", saveDir)


# ===========================================================
# ===================== Run Everything ======================
# ===========================================================

# print out basic graphs based on frequency info
def predictCategories(dataSplit, top, saveDirBase):
    topName, _, _ = top
    authors, books, topWords = loadWCData(saveDirBase, dataSplit, topName)

    normalizations = []
    # normalize nothing
    normalizations.append({"name":"", "norm": []})
    for normIndex, norm in enumerate(normalizations):
        normalizeFeatures(authors, books, norm["norm"])

        # calculate save directory based on input parameters
        saveDir = saveDirBase

        if (norm["name"] != ""):
            saveDir += "%s_%s/" % (topName, norm["name"])
        else:
            saveDir += "%s/" % (topName)

        makeAllPredictions(authors, books, topWords, saveDir)

if __name__ == "__main__":
    for top in mp.tops:
        name, topWords, poetryWords, subsetSize, splitParameter, _, _, _, _ = top
        newTop = (name, topWords, poetryWords)
        saveDir = mp.getSaveDir(mp.language, mp.languageInfo, splitParameter)

        predictCategories(splitParameter, newTop, saveDir)
        print("======================")
