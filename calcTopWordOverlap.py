import numpy as np

import utils
from getWordCounts import loadWCData
import mainParams as mp
from genre import toCent

# Return a simple ascii table as a string
def asciiTable(colHeaders, rowHeaders, cells):
    rows = []
    separator = "------+-"
    formatter = "%-6s| "

    row = []
    rowDivider = []
    row.append(formatter % "")
    rowDivider.append(separator)
    for i, c in enumerate(colHeaders):
        row.append(formatter % c)
        rowDivider.append(separator)

    rows.append("".join(row))
    rows.append("".join(rowDivider))

    for i, r in enumerate(rowHeaders):
        row = []
        rowDivider = []
        row.append(formatter % r)
        rowDivider.append(separator)
        for j, c2 in enumerate(colHeaders):
            row.append(formatter % cells[i][j])
            rowDivider.append(separator)

        rows.append("".join(row))
        rows.append("".join(rowDivider))

    return "\n".join(rows)

def newEmptyWordCounts(topWords):
    wordCounts = {}
    for w in topWords:
        wordCounts[w] = 0
    return wordCounts

# ===========================================================================
NUM_TOP_WORDS = 100

def calcTopWordOverlapOverTime(language):
    saveDirBase = mp.languageInfo[language]["saveDir"]

    print("  Loading data...", end=" ", flush=True)
    authors, books, topWords = loadWCData(saveDirBase, -1, "commonWords", "")
    print("done")


    centWordCounts = {}
    for author in authors:
        cent = toCent(author.authorName)
        if not(cent in centWordCounts):
            centWordCounts[cent] = newEmptyWordCounts(topWords)

        for i, w in enumerate(topWords):
            count = author.counts[i]
            if (count > 0):
                centWordCounts[cent][w] += count

    centTopWords = {}
    for cent in centWordCounts:
        wc = centWordCounts[cent]
        wordList = []
        for w in wc:
            # word, count
            wordList.append([w, wc[w]])

        sortedWordList = sorted(wordList, key=lambda x: x[1], reverse=True)
        topWordList = list(map(lambda x: x[0], sortedWordList))
        centTopWords[cent] = set(topWordList[:NUM_TOP_WORDS])

    centuries = []
    for cent in centTopWords:
        centuries.append(cent)

    centuries = sorted(centuries)

    cells = []
    for i, c1 in enumerate(centuries):
        row = []
        for j, c2 in enumerate(centuries):
            overlap = 0
            wordSet1 = centTopWords[c1]
            wordSet2 = centTopWords[c2]
            for w in wordSet1:
                if (w in wordSet2):
                    overlap += 1
            row.append("%d" % overlap)
        cells.append(row)

    output = asciiTable(centuries, centuries, cells)

    utils.safeWrite(saveDirBase+"topWordOverlapOverTime.txt", output)


if __name__ == "__main__":
    language = "Greek"
    calcTopWordOverlapOverTime(language)
