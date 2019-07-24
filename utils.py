# -*- coding: utf-8 -*-
# utility functions and text parsing classes/helper functions

import urllib3
import xml.etree.ElementTree as ET
from scipy.stats import beta
import os
import re
import json
import errno
import unicodedata



# empty class for creating constants
class Constant:
    pass

# ==============================================================================
# ==============================================================================
# ==============================================================================
# Useful utility functions

# check if the given file path exists, and if not create it.
# based on Krumelur's answer to
# http://stackoverflow.com/questions/12517451/python-automatically-creating-directories-with-file-output
def check_and_create_path(filename):
    if (not os.path.exists(os.path.dirname(filename))):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

# true if the file exists
def fileExists(filename):
    return os.path.isfile(filename)


# write content to the file at filename. Make the directory path to the given
# file if it does not exist.
def safeWrite(filename, content, dumpJSON=False):
    check_and_create_path(filename)
    out_file = open(filename, "w")
    if dumpJSON:
        content = json.dumps(content)
    out_file.write(content)
    out_file.close()

# get the content from a given file by reading it
# parseJSON is true if we should parse the contents as JSON first
def getContent(inFileName, parseJSON):
    inFile = open(inFileName, 'r')
    inContents = inFile.read()
    inFile.close()
    if parseJSON:
        return json.loads(inContents)
    else:
        return inContents

# if the json file exists, add the new item to the list, otherwise create it
def addToJSONList(filename, data):
    if fileExists(filename):
        saveData = getContent(filename, True)
        saveData.append(data)
    else:
        saveData = [data]
    safeWrite(filename, saveData, dumpJSON=True)


# list the files in a directory
def listFiles(dir):
    return os.listdir(dir)

# ==============================================================================
# ==============================================================================
# ==============================================================================
# Functions for beta distribution handling

# adjust data so it falls within (0, 1)
def smoothZeroOne(x):
    if (x == 0):
        x = 0.0001
    if (x == 1):
        x = 0.9999
    return x

# prep data for a beta distribution
def prepDataForBeta(data):
    # remove zeroes since they seem to be an error artifact
    return list(map(smoothZeroOne, list(filter(lambda x: not(x == 0), data))))

# given data, estimate the beta distribution
def estimateBeta(data):
    preppedDat = prepDataForBeta(data)
    a, b, _, _ = beta.fit(preppedDat, floc=0, fscale=1)
    a = round(a, 4)
    b = round(b, 4)
    return a, b

# get probability of a given value based on beta distribution
def getBetaProb(x, a, b):
    return beta.pdf(x, a, b, loc=0, scale=1)


# generate n samples from beta distribution defined by a and b
def getBetaSamples(a, b, n):
    return beta.rvs(a, b, size=n)



# ==============================================================================
# ==============================================================================
# ==============================================================================
# Objects for storing authors and texts


# store an author
class Author:
    def __init__(self, name):
        self.authorName = name
        self.works = []

        # list of this author's tokens
        self.allTokens = []

        # indices of book split tokens
        self.bookSplits = {}

        # raw frequency of tokens
        self.tokenFreqs = None
        # total number of tokens for this author
        self.totalTokenCount = None

        # feature data associated with this author
        self.featureData = None
        self.unNormalizedFeatureData = None

    # get the name for saving this author
    def getSaveName(self):
        return self.authorName

    # add a work to this author's list of works
    def addWork(self, work):
        self.works.append(work)

    # download and save all of this author's works
    def downloadAndSaveWorks(self, path, downloadedWorks, oldAuthorWorksList, verbose):
        # ignore already downloaded works
        worksToDownload = []
        for work in self.works:
            if not(work.textName in downloadedWorks):
                worksToDownload.append(work)

        # count the number of texts
        numTexts = len(worksToDownload)


        res = oldAuthorWorksList
        for i in range(len(worksToDownload)):
            work = worksToDownload[i]
            print("    %s. %.2f%% (%d/%d)" % (work.textName, (100*(i+1)/numTexts), (i+1), numTexts))
            try:
                res.append(work.downloadAndSaveText(path, self.authorName, verbose))
            except:
                print("    Work failed to download.")

        print("%s Done." % self.authorName)
        return {
            "author": self.authorName,
            "works": res
        }

    def __str__(self):
        return ("%s (%d works)." %(self.authorName, len(self.works)))

# an object for storing a book;
class Book:
    def __init__(self, raw, name, author):
        self.textName = name
        self.author = author
        self.bookNumber = raw["bookNumber"]
        self.bookText = raw["bookText"]
        self.numTokens = None
        self.tokens = []

        self.feature_data = None
        self.unNormalizedFeatureData = None

    def getSaveName(self):
        s = "%s_%s_%s" % (self.author, self.textName.replace(" ", "-"), self.bookNumber)
        return s

    def getLongName(self):
        s = "%s.%s.%s" % (self.author, self.textName.replace(" ", "-"), self.bookNumber)
        return s

    def getShortName(self):
        cutoff = 5
        tName = self.textName.lower().replace("the ", "").replace("de ", "").replace("on ", "").replace("against ", "")
        return "%s.%s.%s" % (self.author[0:cutoff], tName[0:cutoff], str(self.bookNumber))

    def __str__(self):
        return ("%s: %s book %s." %(self.author, self.textName, self.bookNumber))

# an object for storing a text
class Text:
    # takes the filename of a json object created by TextSpec
    def __init__(self, fname):
        t = getContent(fname, True)
        self.textName = t["name"]
        self.author = t["author"]
        self.numBooks = t["numBooks"]
        self.books = []

        booksRaw = t["booksRaw"]
        for b in booksRaw:
            self.books.append(Book(b, self.textName, self.author))


# conversions for elision
ELIDED_TRANSFORM = {
    'δ᾽': 'δέ',
    'ἀλλ᾽': 'ἀλλά',
    'παρ᾽': 'παρά',
    'οὐδ᾽': 'οὐδέ',
    'ἐπ᾽': 'ἐπί',
    'δι᾽': 'διά', # but here there are actually a decent number (~3k) of διὸ
    'καθ᾽': 'κατά',
    'κατ᾽': 'κατά',
    'θ᾽': 'τ᾽',
    # no τ᾽; too many possibilities: "τό", "τε", "τά", "τι", etc
    'ἐφ᾽': 'ἐπί',
    'ὑπ᾽': 'ὑπό',
    'γ᾽': 'γε',
    'μετ᾽': 'μετά',
    'μεθ᾽': 'μετά',
    'ἀπ᾽': 'ἀπό',
    'οὔτ᾽': 'οὔτε',
    'οὔθ᾽': 'οὔτε',
    'ταῦτ᾽': 'ταῦτα',
    'ταῦθ᾽': 'ταῦτα',
    'τοῦτ᾽': 'τοῦτο',
    'τοῦθ᾽': 'τοῦτο',
    'μηδ᾽': 'μηδέ',
    'ὑφ᾽': 'ὑπό',
    'ἀφ᾽': 'ἀπό',
    'ῥ᾽': 'ἄρα',
    #
    "περ᾽": "περί",
    "ὅτ᾽": "ὅτι",
    # "οὔτ᾽": "οὔτε",
    # "οὔθ᾽": "οὔτε",
    "ἔτ᾽": "ἔτι", # maybe eths, but seems unlikely
    "πάντ᾽": "πάντα",
    "πάνθ᾽": "πάντα",
    "ὥστ᾽": "ὥστε",
    "ὥσθ᾽": "ὥστε",
    "ἐστ᾽": "ἐστι",
    "ἐσθ᾽": "ἐστι",
    "ἔστ᾽": "ἔστι",
    "ἔσθ᾽": "ἔστι",
    "μάλιστ᾽": "μάλιστα",
    "μάλισθ᾽": "μάλιστα",
    "ἄρ᾽": "ἄρα",
    "τότ᾽": "τότε",
    "τόθ᾽": "τότε",
    "πολλ᾽": "πολλά",
    # "μηδ᾽": "μηδέ",
    "ἅμ᾽": "ἅμα",
    # "ἐστ᾽": "ἐστί",
    "ἵν᾽": "ἵνα",
    "δύ᾽": "δύο", # other possibilities, but pretty unlikely
    # "αὐτ᾽": "αὐτό",
    # #"τιν᾽": "τινα", could be tini also
    # "πολ᾽": "πολύ",
    "μήτ᾽": "μήτε",
    "μήθ᾽": "μήτε",
    "μ᾽": "με",
    #"ὅθ᾽": , too many possibilities
    #"ἔθ᾽": , too many positiblities
    #"τιν᾽": "τινα", could be tini also
    # these don't appear
    # "οὔτ᾽": 0,
    # "οὔθ᾽": 0,
    # "μηδ᾽": 0,
    # "αὐτ᾽": 0,
    # "αὐθ᾽": 0,
    # "πολ᾽": 0,
}
# convert from ellided form to most likely un-elided form
# for those with a count over 2000
def transformElided(token):
    if (token in ELIDED_TRANSFORM):
        token = ELIDED_TRANSFORM[token]
    return token
