# -*- coding: utf-8 -*-
# Extract word counts from all of the texts.
import re
import copy
import random
import unicodedata
import math

from sklearn import decomposition
import numpy as np

import utils
import mainParams as mp

from genre import toGenre

# ==============================================================================
# ==============================================================================

# fix some unicode mess stuff
def preprocessToken(token):
    if token == "":
        return token

    if (token == "ὧς"):
        token = "ὥς"


    if (token == "δἰ" or token == "δἱ"):
        token = "δι" + "\u1fbd"

    # if (token == "ἐς"):
    #     token = "εἰς"

    # ------------------------

    return token

# ===================================================
# ============== Load all of the texts ==============
# ===================================================

# Given tokens, select the first subsetSize or a random subsetSize of them.
# This allows us to see whether our comparisons hold for small values
def selectSubset(tokens, subsetSize):
    if (subsetSize == -1):
        resTokens = tokens
    else:
        # randomly select a subset of tokens
        if (len(tokens) > subsetSize):
            # initial
            resTokens = tokens[:subsetSize]
            # random
            #resTokens = np.random.choice(tokens, size=(subsetSize), replace=False)
        else:
            resTokens = tokens

    #print("%d, %d" % (len(resTokens), subsetSize))
    return resTokens

# Load all of the texts. if splitParameter is not -1, divide each author's
# work in 2, putting the first half of each 2*splitParameter words in one
# "author" and the second half in another "author"
def loadTexts(splitParameter, subsetSize, textLocation, language, saveDir):
    useSplitParam = splitParameter != -1

    available = utils.getContent(textLocation + "available.json", True)
    authors = []
    allWorks = []
    books = []
    print(len(available), end=" - ", flush=True)

    # For each available text
    for i, o in enumerate(available):
        if (i % 20 == 0):
            print(i, end=" ", flush=True)

        authorName = o["author"]
        # split into two authors if necessary
        if useSplitParam:
            a1 = utils.Author(authorName)
            a2 = utils.Author(authorName + "_2")
        else:
            a = utils.Author(authorName)

        workLocs = o["works"]
        works = []
        authorTokens1 = []
        authorTokens2 = []

        # Process each work
        for w in workLocs:
            allWorks.append(w)
            # if authorName == "Arrian" and w["name"] != "Anabasis":
            #     continue
            t = utils.Text(w["location"])

            if useSplitParam:
                a1.addWork(t)
                a2.addWork(t)
            else:
                a.addWork(t)

            # For each book, process all of its tokens, count them,
            # add them to this author.
            for b in t.books:
                rawTokens = re.sub(r'\.,;:᾽῾\'', "", b.bookText).split(" ")
                tokens = []
                for token in rawTokens:
                    if language == "Greek":
                        token = preprocessToken(token)

                        token = utils.transformElided(token)


                    if (token == ""):
                        continue


                    tokens.append(token)

                b.tokens = tokens
                books.append(b)

                if useSplitParam:
                    # add in the tokens from this book as well
                    if (splitParameter == -2):
                        authorTokens1.extend(tokens)
                        authorTokens2.extend(tokens)
                    else:
                        modul = splitParameter*2
                        t1 = [tokens[i] for i in range(len(tokens)) if ((i % modul) < splitParameter)]
                        t2 = [tokens[i] for i in range(len(tokens)) if ((i % modul) >= splitParameter)]
                        authorTokens1.extend(t1)
                        authorTokens2.extend(t2)
                        a1.bookSplits[len(authorTokens1)] = True
                        a2.bookSplits[len(authorTokens2)] = True
                else:
                    # add in the tokens from this book as well
                    authorTokens1.extend(tokens)
                    a.bookSplits[len(authorTokens1)] = True;


        if useSplitParam:
            if splitParameter == -2:
                half = int(len(authorTokens1)/2)
                a1.allTokens = authorTokens1[:half]
                a2.allTokens = authorTokens2[half:]
            else:
                a1.allTokens = selectSubset(authorTokens1, subsetSize)
                a2.allTokens = selectSubset(authorTokens2, subsetSize)

            authors.append(a1)
            authors.append(a2)
        else:
            a.allTokens = selectSubset(authorTokens1, subsetSize)

            authors.append(a)

    numProseA = 0
    numPoetryA = 0
    for a in authors:
        if (toGenre(a.authorName) == 0):
            numProseA += 1
        else:
            numPoetryA += 1

    numProseB = 0
    numPoetryB = 0
    for b in books:
        if (toGenre(b.author) == 0):
            numProseB += 1
        else:
            numPoetryB += 1

    print("")
    countInfo = []
    countInfo.append("Number of authors: %d" % len(authors))
    countInfo.append("  prose: %d" % numProseA)
    countInfo.append("  poetry: %d" % numPoetryA)
    countInfo.append("Number of works: %d" % len(allWorks))
    countInfo.append("Number of books: %d" % len(books))
    countInfo.append("  prose: %d" % numProseB)
    countInfo.append("  poetry: %d" % numPoetryB)
    countInfoStr = "\n".join(countInfo)
    print(countInfoStr)

    if (saveDir != ""):
        utils.safeWrite(saveDir+"numberOfAuthors_Books.txt", countInfoStr)

    # If true, print all of the loaded texts.
    printLoaded = False

    if printLoaded:
        tab = "  "
        print("Authors:")
        s = []
        for author in authors:
            s.append(tab + str(author))
        print("\n".join(s))
        print("----")

        print("Books:")
        s = []
        for book in books:
            s.append(tab + str(book))
        print("\n".join(s))
        print("----")

    return authors, books

# ============================================================
# ========== Calculate overall most frequent words ===========
# ============================================================

# Given the authors (with their associated tokens), get the counts of each
# token across all texts.
# poetryOnly is true if we only look at poetry
def getAllTokenCounts(authors, saveDir):
    allTokenCounts = {}
    poetryTokenCounts = {}
    totalTokens = 0

    # for each author, keep track of counts; also keep track of prose/poetry
    for i in range(len(authors)):
        author = authors[i]
        totalTokens += len(author.allTokens)
        # print("%s: %d" %(author.authorName, len(author.allTokens)))
        allTokens = author.allTokens

        totalTokenCount = 0
        tokenCounts = {}
        for token in allTokens:

            totalTokenCount += 1
            if (token in tokenCounts):
                tokenCounts[token] = tokenCounts[token] + 1
            else:
                tokenCounts[token] = 1

            if (token in allTokenCounts):
                allTokenCounts[token] = allTokenCounts[token] + 1
            else:
                allTokenCounts[token] = 1

            if (toGenre(author.authorName) == 1):
                if (token in poetryTokenCounts):
                    poetryTokenCounts[token] = poetryTokenCounts[token] + 1
                else:
                    poetryTokenCounts[token] = 1

        author.tokenCounts = tokenCounts

        author.totalTokenCount = totalTokenCount

        # print("Results for %s:" % author.authorName)
        # print(len(allTokens))
        # print("---")
    typeTokenInfo = []
    typeTokenInfo.append("Total tokens: %d" % totalTokens)
    typeTokenInfo.append("Total types: %d" % len(allTokenCounts))

    typeTokenInfoStr = "\n".join(typeTokenInfo)
    print(typeTokenInfoStr)

    utils.safeWrite(saveDir+"numberOfTypes_Tokens.txt", typeTokenInfoStr)

    return allTokenCounts, poetryTokenCounts

# calculate the top N words given a map of word to counts
def getTopWords(N, allTokenCounts):
    tokenCountsList = []
    for token in allTokenCounts:
        if (allTokenCounts[token] > 2): # timesaving to skip unit/double words
            tokenCountsList.append([token, allTokenCounts[token]])

    sortedTokenCounts = sorted(tokenCountsList, key=lambda x: x[1], reverse=True)

    tops = sortedTokenCounts[0:N]

    topWords = list(map(lambda x: x[0], tops))

    return topWords

# ============================================================
# ================== Calculate word counts  ==================
# ============================================================

# get the word count filename
def getWCFilename(saveDir, topStr):
    res = saveDir + "%s/wordCountData/wcd_%s.json" % (topStr, topStr)
    return res

# given the list of words, remove a certain subset of them
# to prevent powerful words from overwhelming the display.
def wordPCAFitTransform(arr):
    # skipFirst = 4
    # return arr[skipFirst:]
    # 0, 1, 2, 3, 19
    v2 = []
    for i, row in enumerate(arr):
        if not(i in [0, 1, 2, 3, 18]): # de kai gar te es
            v2.append(row)
    return np.array(v2)



# Given authors, books, the top words, the location to save info,
# calculate the count of the top words for the authors and books
# and save them.
def calculateWordCounts(authors, books, topWords, topName, saveDir):
    wcData = {}

    wcData["topWords"] = topWords
    wcData["authors"] = {}
    wcData["books"] = {}

    totalWords = ["Words, Author"]
    fullCount = np.zeros((len(authors), len(topWords)))
    # get the top token frequency features for each author
    for i in range(len(authors)):
        if (i%10 == 0):
            print(i, end=" ", flush=True)
        author = authors[i]
        tC = author.tokenCounts

        counts = []
        for j, word in enumerate(topWords):
            if (word in tC):
                wordCount = tC[word]
            else:
                wordCount = 0
            fullCount[i, j] = wordCount
            counts.append(wordCount)

        # add in frequency of remaining tokens

        last = int(author.totalTokenCount - np.sum(counts))
        counts.append(last)
        totalWords.append("%d, %s" % (author.totalTokenCount, author.authorName))

        aInfo = {}
        aInfo["counts"] = counts
        aInfo["name"] = author.authorName
        wcData["authors"][author.getSaveName()] = aInfo

    print("")
    # print number of words in each author
    utils.safeWrite(saveDir+"wordCountData/authorTotalWords.txt", "\n".join(totalWords))

    # print info about each word
    w_sum = np.sum(fullCount, axis=0)
    w_means = np.mean(fullCount, axis=0)
    w_median = np.median(fullCount, axis=0)
    out = ["word: sum, mean, median"]
    for i, word in enumerate(topWords):
        out.append("%s: %d, %.2f, %.1f" % (word, w_sum[i], w_means[i], w_median[i]))
    fname = "%s%s/wordInfo_%s.txt" % (saveDir, topName, topName)
    utils.safeWrite(fname, "\n".join(out))

    fname = "%s%s/wordCountData/wordCountByText_%s.json" % (saveDir, topName, topName)
    utils.safeWrite(fname, fullCount.T.tolist(), True)

    # run pca on the words to give related words similar info.
    pca = decomposition.PCA(n_components=6)

    pca.fit(wordPCAFitTransform(fullCount.T))
    components = pca.transform(fullCount.T)
    #print("PCA on words:")
    # print(pca.explained_variance_ratio_)
    fname = "%s%s/wordCountData/wordPrincipalComponents_%s.json" % (saveDir, topName, topName)
    utils.safeWrite(fname, components.tolist(), True)


    # get the top token frequency features for each book
    for book in books:
        tokens = book.tokens

        book.numTokens = len(tokens)

        totalTokenCount = 0
        tokenCounts = {}
        for token in tokens:

            totalTokenCount += 1
            if (token in tokenCounts):
                tokenCounts[token] = tokenCounts[token] + 1
            else:
                tokenCounts[token] = 1

        counts = []
        for word in topWords:
            if (word in tokenCounts):
                counts.append(tokenCounts[word])
            else:
                counts.append(0)

        # add in frequency of remaining tokens
        last = int(totalTokenCount - np.sum(counts))
        counts.append(last)


        bInfo = {}
        bInfo["counts"] = counts
        bInfo["name"] = book.textName
        bInfo["author"] = book.author
        bInfo["number"] = book.bookNumber
        wcData["books"][book.getSaveName()] = bInfo

    fname = getWCFilename(saveDir, topName)
    utils.safeWrite(fname, wcData, True)

# Given authors, books, the top words, and the location to save info,
# save each author's usage of top words (and top words only)
def extractTopWordsOnly(authors, books, topWords, topWordsName, saveDir):
    saveDir += "%s/textsOnlyTopWords/" % topWordsName
    topWordDict = {}
    for i, w in enumerate(topWords):
        topWordDict[w] = i

    for author in authors:
        tokens = author.allTokens
        onlyTopTokens = []
        for token in tokens:
            if token in topWordDict:
                onlyTopTokens.append(topWordDict[token])

        utils.safeWrite(saveDir+ "lists/authors/" + author.getSaveName() + ".json", onlyTopTokens, dumpJSON=True)


    # get the top token frequency features for each book
    for book in books:
        tokens = book.tokens
        onlyTopTokens = []
        for token in tokens:
            if token in topWordDict:
                onlyTopTokens.append(topWordDict[token])

        utils.safeWrite(saveDir+ "lists/books/" + book.getSaveName() + ".json", onlyTopTokens, dumpJSON=True)


# ============================================================
# ==== Calculate frequency features for authors and books ====
# ============================================================

def calculateFrequencies(authors, books, topWords):
    # get the top token frequency features for each author
    for author in authors:
        freqs = []
        for j, word in enumerate(topWords):
            wc = author.counts[j]
            freqs.append(wc/author.totalTokenCount)

        npf = np.array(freqs)
        author.featureData = npf
        author.unNormalizedFeatureData = npf

    # get the top token frequency features for each book
    for book in books:
        freqs = []
        for j, word in enumerate(topWords):
            wc = book.counts[j]
            if book.numTokens != 0:
                freqs.append(wc/book.numTokens)
            else:
                freqs.append(0)

        npf = np.array(freqs)
        book.featureData = npf
        book.unNormalizedFeatureData = npf

# Loads wordcount data for the texts
def loadWCData(saveDir, dataSplit, topName):
    wcData = utils.getContent(getWCFilename(saveDir, topName), True)

    # load author data
    authors = []
    for key in wcData["authors"]:
        a = wcData["authors"][key]
        authorName = a["name"]
        auth = utils.Author(authorName)
        auth.counts = a["counts"]
        auth.totalTokenCount = np.sum(a["counts"])

        authors.append(auth)

    # load book data
    books = []
    for key in wcData["books"]:
        b = wcData["books"][key]
        raw = {
            "bookText": "",
            "bookNumber": b["number"]
        }
        book = utils.Book(raw, b["name"], b["author"])
        book.counts = b["counts"]
        book.numTokens = np.sum(b["counts"])

        books.append(book)

    topWords = wcData["topWords"]

    calculateFrequencies(authors, books, topWords)

    return authors, books, topWords

# ===========================================================
# ===================== Run Everything ======================
# ===========================================================

# load texts and save the word count info
def getWordCounts(dataSplit, top, subsetSize, textLocation, language, addPoetry, saveDir):
    authors, books = loadTexts(dataSplit, subsetSize, textLocation, language, saveDir)

    print("Getting token counts for all texts...")
    allTokenCounts, poetryTokenCounts = getAllTokenCounts(authors, saveDir)

    name, tops, poetryTops = top
    print("%s:" % name)
    # if we are using words from poetry, add those
    # that don't appear in the top for all texts to the list
    print("  Getting top words...")
    if (poetryTops != -1):
        topWords = getTopWords(tops, allTokenCounts)
        topWordsPoetry = getTopWords(poetryTops, poetryTokenCounts)
        for w in topWordsPoetry:
            if not(w in topWords):
                topWords.append(w)
    else:
        topWords = getTopWords(tops, allTokenCounts)

    print("  Calculating word counts per author...")
    calculateWordCounts(authors, books, topWords, name, saveDir)
    if (language == "Greek"):
        print("  Extracting top words...")
        extractTopWordsOnly(authors, books, topWords, name, saveDir)

if __name__ == "__main__":
    textLocation = mp.languageInfo[mp.language]["textLocation"]
    tops = mp.languageInfo[mp.language]["tops"]
    for top in tops:
        name, topWords, poetryWords, subsetSize, splitParameter, includeBooks, includeGraphs, _, wordToPOS = top
        newTop = (name, topWords, poetryWords)
        saveDir = mp.getSaveDir(mp.language, mp.languageInfo, splitParameter)
        getWordCounts(splitParameter, newTop, subsetSize, mp.textLocation, mp.language, mp.addPoetry, saveDir)
