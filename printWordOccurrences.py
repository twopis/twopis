# -*- coding: utf-8 -*-
# Given an author and target words, save all occurrences of that word with
# Some context.
import re
import copy
import random
import math
import time

import numpy as np

import utils
import graphUtils
import genre
from getWordCounts import selectSubset
from mainParams import language

# ==============================================================================

# ===================================================
# ============== Load all of the texts ==============
# ===================================================


# Load all of the texts. if splitParameter is not -1, divide each author's
# work in 2, putting the first half of each 2*splitParameter words in one
# "author" and the second half in another "author"
# important to note this has differences from the getWordCounts loadTexts
def loadTexts(splitParameter, subsetSize, targets, language):
    useSplitParam = splitParameter != -1

    available = utils.getContent("texts/" + language.lower() + "/available.json", True)
    authors = []
    books = []
    for o in available:
        authorName = o["author"]
        if authorName in targets:
            if useSplitParam:
                a1 = utils.Author(authorName)
                a2 = utils.Author(authorName + "_2")
            else:
                a = utils.Author(authorName)

            workLocs = o["works"]
            works = []
            authorTokens1 = []
            authorTokens2 = []
            for w in workLocs:
                t = utils.Text(w["location"])

                if useSplitParam:
                    a1.addWork(t)
                    a2.addWork(t)
                else:
                    a.addWork(t)

                for b in t.books:
                    books.append(b)

                    if useSplitParam:
                        # add in the tokens from this book as well
                        tokens = re.sub(r'\.,;:᾽῾\'', "", b.bookText).split(" ")
                        modul = splitParameter*2
                        t1 = [tokens[i] for i in range(len(tokens)) if ((i % modul) < splitParameter)]
                        t2 = [tokens[i] for i in range(len(tokens)) if ((i % modul) >= splitParameter)]
                        authorTokens1.extend(t1)
                        authorTokens2.extend(t2)
                    else:
                        # add in the tokens from this book as well
                        tokens = re.sub(r'\.,;:᾽῾\'', "", b.bookText).split(" ")
                        authorTokens1.extend(tokens)


            if useSplitParam:
                a1.allTokens = selectSubset(authorTokens1, subsetSize)
                a2.allTokens = selectSubset(authorTokens2, subsetSize)

                authors.append(a1)
                authors.append(a2)
            else:
                a.allTokens = selectSubset(authorTokens1, subsetSize)

                authors.append(a)

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

# preprocess the tokens from a text
def processAllTokens(authors):
    for author in authors:
        for i, token in enumerate(author.allTokens):
            author.allTokens[i] = token

# get a window of tokens around a given token
def getTokenContext(index, tokenList):
    windowSize = 10
    start = max(0, index - windowSize)
    end = min(len(tokenList), index + windowSize + 1)

    before = []
    tok = []
    after = []
    for i in range(start, end):
        # mark the target token with squiggles
        if (i - start) == windowSize:
            tok.append(tokenList[i])
        elif (i - start) < windowSize:
            before.append(tokenList[i])
        else:
            after.append(tokenList[i])

    return [" ".join(before), tok[0], " ".join(after), " ".join(before[::-1])]

# given the authors, a list of target tokens by author, and location to save
# print each occurrence of a target word in a given author with context
# on either side
def printAuthorWords(authors, targets, saveDir):
    for author in authors:
        aname = author.authorName
        for targetTokenName in targets[aname]:
            targetToken = targetTokenName.split("_")[-1]
            matches = []
            for i, token in enumerate(author.allTokens):
                if token == targetToken:
                    matches.append(getTokenContext(i, author.allTokens))

            orders = [
                ("", None),
                ("_after", lambda x: x[2]), # after context
                ("_before", lambda x: x[3]), # reverse of before context
            ]
            for order in orders:
                oname, keyFunc = order
                if keyFunc == None:
                    myMatches = matches
                else:
                    myMatches = sorted(matches, key=keyFunc)
                output = []
                for match in myMatches:
                    output.append(" ~~ ".join(match[:3]))
                fname = saveDir + ("wordOccurrences%s/%s_%s.txt" % (oname, targetTokenName, aname))
                utils.safeWrite(fname, "\n".join(output))

# ===========================================================
# ===================== Run Everything ======================
# ===========================================================

def printWordOccurrences(saveDirBase, targets, language):
    authors, books = loadTexts(-1, -1, targets, language)

    processAllTokens(authors)

    printAuthorWords(authors, targets, saveDirBase)

if __name__ == "__main__":
    # default: output
    saveDir = "output/"

    targets = {
        #"ApolloniusRhodius": ["τε"],
        "AeliusAristides": ["ἄνδρες"],
        "Demosthenes": ["ἄνδρες"],
        #"DioChrysostom": ["ὑμεῖς", "ὑμῖν"]
    }

    printWordOccurrences(saveDir, targets, language)
