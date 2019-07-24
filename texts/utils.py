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

# an object for storing a text still in XML format
class XMLText:
    # takes the filename of a json object created by TextSpec
    def __init__(self, fname):
        t = getContent(fname, True)
        self.textName = t["name"]
        self.author = t["author"]
        self.numBooks = t["numBooks"]
        self.booksRaw = t["booksRaw"]

    def convertFromXML(self):
        convertedBooks = []
        i = 0
        for b in self.booksRaw:
            i += 1
            debugString = "%s %s %d" % (self.author, self.textName, i)
            newText = removePunct(parse_TEI_full_book(b["bookText"]), debugString)
            # remove if you want to keep grave/acute difference
            newText = removeGraves(newText)

            b["bookText"] = newText
            convertedBooks.append(b)

        textObj = {
            "name": self.textName,
            "author": self.author,
            "numBooks": self.numBooks,
            "booksRaw": convertedBooks
        }
        return textObj

# Basic things shared by most text objects
class BaseText(object):
    # takes the filename of a text file
    def __init__(self, aname, wname, fname):
        t = getContent(fname, False)
        self.textName = wname
        self.author = aname

        split = t.split("===---===~~~")
        self.numBooks = len(split)
        self.booksRaw = []
        for i, book in enumerate(split): # For a larger project, there should be a better accouting of books.
            self.booksRaw.append({"bookNumber": i+1, "bookText": book})

    # Function for removing various artifacts. Should be overwritten by child.
    def removePunct(self, t, debugString):
        return t

    def convert(self):
        convertedBooks = []
        i = 0
        for b in self.booksRaw:
            i += 1
            debugString = "%s %s %d" % (self.author, self.textName, i)
            newText = self.removePunct(b["bookText"], debugString)

            b["bookText"] = newText
            convertedBooks.append(b)

        textObj = {
            "name": self.textName,
            "author": self.author,
            "numBooks": self.numBooks,
            "booksRaw": convertedBooks
        }
        return textObj


# an object for storing a text from the Gutenberg corpus
class GutenbergText(BaseText):
    # takes the filename of a text file
    def __init__(self, aname, wname, books):
        self.textName = wname
        self.author = aname
        self.numBooks = len(books)
        self.booksRaw = []
        for fname, bookNum in books:
            t = getContent(fname, False)
            self.booksRaw.append({"bookNumber": bookNum, "bookText": t})

    def removePunct(self, t, debugString):
        return removePunctGutenberg(t, debugString)


# an object for storing a text from the Shakespeare corpus
class ShakespeareText(BaseText):
    # takes the filename of a text file
    def __init__(self, aname, wname, fname):
        inFile = open(fname, 'rb')
        contents = inFile.read()
        t = contents.decode('utf-16')
        inFile.close()
        self.textName = wname
        self.author = aname
        self.numBooks = 1
        self.booksRaw = [{"bookNumber": 1, "bookText": t}]

    def removePunct(self, t, debugString):
        return removePunctShakespeare(t, debugString)

# an object for storing a Middle English text I gathered
class METext(BaseText):
    def removePunct(self, t, debugString):
        return removePunctME(t, debugString)


# an object for storing an Old English text I gathered
class OEText(BaseText):
    def removePunct(self, t, debugString):
        return removePunctOE(t, debugString)

# an object for storing an Icelandic Icepahc text
class IcepahcText(BaseText):
    def removePunct(self, t, debugString):
        return removePunctIcepahc(t, debugString)


# an object for storing an Icelandic Sagas text
class SagasText(BaseText):
    def removePunct(self, t, debugString):
        return removePunctSagas(t, debugString)



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

# ==============================================================================
# ==============================================================================
# ==============================================================================
# unicode helper functions

# compatability characters
def isCompatiblityChar(c):
    # from wikipedia
    return c in ["<initial>", "<medial>", "<final>", "<isolated>", "<wide>", "<narrow>", "<small>", "<square>", "<vertical>", "<circle>", "<noBreak>", "<fraction>", "<sub>", "<super>", "<compat>"]

# decompose a unicode character into its combining pieces
def fullyDecomposeUnicodeChar(uChar):
    arr = unicodedata.decomposition(uChar).split(" ")
    # ignore compatibility stuff
    if (len(arr) >= 1 and isCompatiblityChar(arr[0])):
        arr = arr[1:]
    if (len(arr) == 1 and arr[0] == ''):
        arr = [uChar]
    else:
        for j in range(len(arr)):
            c = chr(int(arr[j], base=16))
            if (j == 0):
                arr[j] = fullyDecomposeUnicodeChar(c)
            else:
                arr[j] = c
    # for char in arr:
    #     print(i, unicodedata.name(char))
    return "".join(arr)

# decompose combining pieces in each character of a string
def fullyDecomposeUnicodeString(uStr):
    result = ""
    for i, c in enumerate(uStr):
        result += fullyDecomposeUnicodeChar(c)
    return result

# print a variety of information about a unicode character
def printUnicodeChar(c):
    print(("\'%s\'" % c), '\\u%04x' % ord(c), unicodedata.category(c), end=" ")
    try:
        print(unicodedata.name(c))
    except Exception as inst:
        print("NO NAME")


# ==============================================================================
# ==============================================================================
# ==============================================================================
# Functions for cleaning up texts


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

# remove punctuation for Greek texts
def removePunct(text, debugString):
    # remove specific error in Cassius Dio Book 59
    text = re.sub(r'῾π. 22, 24-23, 5 δ.᾿, Jοανν. αντιοξη. φρ. 84 μ. ῾ϝ. 7-11᾿.', ' ', text)
    # remove specific errors in Valerius Harpocration Lexion in decem oratores Atticos
    text = re.sub(r'\u1ffe\u0323\u0323\u1fbd\?\u0314\u0323\u0323\u1fbd', ' ', text)
    text = re.sub(r'\u0323\u0323\u1fbd\?\u0314\u0323\u0323\u1fbd', ' ', text)
    # remove specific error in Plutarch Antony
    text = re.sub(r'γυ˙[\s]+ναῖκες', 'γυναῖκες', text)


    text = re.sub(r'\[p\. [\d]+\]', ' ', text) # no page nums
    text = re.sub(r'\%5,', ',', text) # %5,
    text = re.sub(r'\#\d*', ' ', text) # remove # signs
    text = re.sub(r'(\%(5|2|14))|[\*\u005e_]', ' ', text) # replace with spaces
    text = re.sub(r'(\&lt;|[\u00ab])', '<', text) # remove &lt;
    text = re.sub(r'(\&gt;|[\u00bb])', '>', text) # remove &gt;
    text = re.sub(r'(\&amp;)', '&', text) # remove &amp;
    text = re.sub(r'[@&\$\%\?\ufffd\u00b4\u00a8\u0060\u00bd]', '', text) # replace "replacement character", floating acute, diaresis, ½ with nothing
    text = re.sub(r'[\u2026]', '...', text) # replace ellipses
    text = re.sub(r'\u00e6', 'αε', text) # replace ae
    text = re.sub(r'\u0323\u0323\u0313\s', '.\'', text) # fix end quote issue
    text = re.sub(r'\u0323\u0323\u0313', '\u0313', text) # remove double under dot issues
    text = re.sub(r'\u0375\s', ', ', text) # fix end quote issue
    text = re.sub(r'[\u201c\u201d]', '"', text) # normalize quotes
    text = re.sub(r'（', ' (', text) # fix start paren issue
    text = re.sub(r'）', ') ', text) # fix end paren issue
    text = re.sub(r'[\u3008\u2329]', ' <', text) # left bracket
    text = re.sub(r'[\u3009\u232a]', '> ', text) # right bracket
    text = re.sub(r'[—\u2010]', '> ', text) # normalize dashes
    text = re.sub(r'\u1fe4(᾽)?([,:])\s', 'ρ\u1fbd\1 ', text) # remove final rho problems
    text = re.sub(r'\u1fe4(᾽)?\s', 'ρ\u1fbd ', text) # remove final rho problems
    text = re.sub(r'([ΒΓΔΖΘΚΛΜΝΞΠΡΣΤΦΧΨβγδζθκλμνξπρσςτφχψ])[\u0313\u0314\u1fbf]', '\1\u1fbd', text) # fix reverse comma issue
    text = re.sub(r'[\u00a7]+ \d+', ' ', text) # fix rho breathing issue
    text = re.sub(r'([\d\.\,;:\"\s])\u1fbf([\d\.\,;:\"\s])', '\1\'\2', text) # fix end quote as breathing
    text = re.sub(r'\u1fbe', ',', text) # fix comma as iota subscript
    text = re.sub(r'{', '(', text) # curly to paren
    text = re.sub(r'}', ')', text) # curly to paren
    text = re.sub(r'ā', 'α', text) # replace macron a
    text = re.sub(r'ü', 'υ', text) # replace umlaut u
    text = re.sub(r'\[?[¯˘×]+[\s¯˘×!]*\]?', ' ', text) # remove length notation

    text = re.sub(r'ς\d+(^\s)', 'σ\1', text) # remove digits with sigma
    text = re.sub(r'\d+-\d+', ' ', text) # remove digits in range
    text = re.sub(r'\d+', ' ', text) # remove digits

    text = re.sub(r'\s[῾‘\u2018\u2019]', ' \'', text) # fix start quote issue
    text = re.sub(r'\s(\':)?[\'<]‘', ' \"', text) # fix different start quote issue
    text = re.sub(r'‘[᾽>][,>]?\s', '\" ', text) # fix different end quote issue
    text = re.sub(r'\u0374', '\'', text) # fix different end quote issue

    text = re.sub(r'\u0375', ',', text) # fix misrecognized comma

    # remove nonbreaking zero-width space and empty chars
    text = re.sub(r'(\ufeff|\u0001|\u0002)', '', text)

    # remove combining accents that shouldn't combine
    text = re.sub(r'(\u0300|\u1fef)', '', text)
    text = re.sub(r'([᾽λβγθμνπρτ])\u0301', r'\1', text)
    text = re.sub(r'([ν\s])\u0302', r'\1', text)
    text = re.sub(r'([αη\s])\u0308', r'\1', text)
    text = re.sub(r'([῾᾽\'\s])\u0313', r'\1', text)
    text = re.sub(r'([῾᾽\'\s])\u0314', r'\1', text)
    text = re.sub(r'\u0323', r'', text)
    text = re.sub(r'\u0345\u0345', r'', text)
    text = re.sub(r'([῾᾽\'\sειμνξρ])\u0345', r'\1', text)
    text = re.sub(r'([\.῾᾽\'\sσ])\u1fc0', r'\1', text)

    # replace some characters
    text = re.sub(r'ῡ', 'υ', text)


    # combine accents that are orphaned
    text = re.sub(r'\u1fcdΩ', 'Ὤ', text)
    #---
    text = re.sub(r'\u1fceΑ', 'Ἄ', text)
    text = re.sub(r'\u1fceΕ', 'Ἔ', text)
    text = re.sub(r'Ε\u1fce', 'Ἔ', text)
    text = re.sub(r'\u1fceΗ', 'Ἤ', text)
    text = re.sub(r'\u1fceΙ', 'Ἴ', text)
    text = re.sub(r'\u1fceΟ', 'Ὄ', text)
    text = re.sub(r'\u1fceΩ', 'Ὤ', text)
    text = re.sub(r'\u1fceα', 'ἄ', text)
    text = re.sub(r'\u1fceε', 'ἔ', text)
    text = re.sub(r'\u1fceη', 'ἤ', text)
    text = re.sub(r'\u1fceι', 'ἴ', text)
    # this one has to be last
    text = re.sub(r'\u1fce', 'ἔ', text)
    #---
    text = re.sub(r'\u1fcfη', 'ἦ', text)
    text = re.sub(r'\u1fcfΙ', 'Ἶ', text)
    #---
    text = re.sub(r'\u1fddε', 'ἓ', text)
    text = re.sub(r'\u1fddΩ', 'Ὣ', text)
    text = re.sub(r' \u1fdd ', ' ', text)
    #---
    text = re.sub(r'\u1fdeΑ', 'Ἅ', text)
    text = re.sub(r'\u1fdeΕ', 'Ἕ', text)
    text = re.sub(r'\u1fdeΗ', 'Ἥ', text)
    text = re.sub(r'Η\u1fde', 'Ἥ', text)
    text = re.sub(r'\u1fdeΟ', 'Ὅ', text)
    text = re.sub(r'\u1fdeΥ', 'Ὕ', text)
    text = re.sub(r'\u1fdeα', 'ἅ', text)
    text = re.sub(r'\u1fdeε', 'ἕ', text)
    text = re.sub(r'\u1fdeη', 'ἥ', text)
    text = re.sub(r'\u1fdeι', 'ἵ', text)
    text = re.sub(r'\u1fdeο', 'ὅ', text)
    text = re.sub(r'\u1fdeυ', 'ὕ', text)
    #---
    text = re.sub(r'\u1fdfῳ', 'ᾧ', text)
    text = re.sub(r'\u1fdfσ', '', text)
    text = re.sub(r'Ω\u1fdf', 'Ὧ', text)
    text = re.sub(r'\u1fdfω', 'ὧ', text)
    #---
    text = re.sub(r'\u1ffdα', 'ά', text)
    text = re.sub(r'\u1ffdι', 'ί', text)
    text = re.sub(r'\u1ffd', '', text)
    #---
    text = re.sub(r'Ρ\u1ffe', 'Ῥ', text)
    text = re.sub(r'Ι\u1ffe', 'Ἱ', text)
    text = re.sub(r'\u1ffe', '', text)
    text = re.sub(r'\u2019', '\'', text)
    #---

    # Used for determining where characters appear
    # \u1fbd is used for δ᾽, etc
    # \u1fbf - all sorts of different things, would have to fix issues in the text
    # matches = re.finditer(r'([\s\S]{3})(ῡ)([\s\S]{3})', text)
    # firstMatch = True
    # for m in matches:
    #     if (firstMatch):
    #         firstMatch = False
    #         print(debugString)
    #     print("<{%s~~%s~~%s}>" % (m.group(1), m.group(2), m.group(3)))
    #     #print("<{%s}>" % (m.group(0)))

    # specific for our concerns

    text = re.sub(r'-[\s]*\n', '', text) # no words split over lines
    text = re.sub(r'-', ' ', text) # replace dashes with spaces
    text = re.sub(r'[,\.\[\]\(\)†<>:;¯⟦⟧\"\'!]', '', text) # no punct
    text = re.sub(r'[\s]+', ' ', text) # unify spaces
    return text

# remove grave accents
def removeGraves(text):
    text = re.sub(r'ὰ', 'ά', text)
    text = re.sub(r'ὲ', 'έ', text)
    text = re.sub(r'ὴ', 'ή', text)
    text = re.sub(r'ὶ', 'ί', text)
    text = re.sub(r'ὸ', 'ό', text)
    text = re.sub(r'ὺ', 'ύ', text)
    text = re.sub(r'ὼ', 'ώ', text)
    text = re.sub(r'Ὰ', 'Ά', text)
    text = re.sub(r'Ὲ', 'Έ', text)
    text = re.sub(r'Ὴ', 'Ή', text)
    text = re.sub(r'Ὶ', 'Ί', text)
    text = re.sub(r'Ὸ', 'Ό', text)
    text = re.sub(r'Ὺ', 'Ύ', text)
    text = re.sub(r'Ὼ', 'Ώ', text)
    text = re.sub(r'ἂ', 'ἄ', text)
    text = re.sub(r'ἒ', 'ἔ', text)
    text = re.sub(r'ἢ', 'ἤ', text)
    text = re.sub(r'ἲ', 'ἴ', text)
    text = re.sub(r'ὂ', 'ὄ', text)
    text = re.sub(r'ὒ', 'ὔ', text)
    text = re.sub(r'ὢ', 'ὤ', text)
    text = re.sub(r'Ἂ', 'Ἄ', text)
    text = re.sub(r'Ἒ', 'Ἔ', text)
    text = re.sub(r'Ἢ', 'Ἤ', text)
    text = re.sub(r'Ἲ', 'Ἴ', text)
    text = re.sub(r'Ὂ', 'Ὄ', text)
    text = re.sub(r'Ὢ', 'Ὤ', text)
    text = re.sub(r'ἃ', 'ἅ', text)
    text = re.sub(r'ἓ', 'ἕ', text)
    text = re.sub(r'ἣ', 'ἥ', text)
    text = re.sub(r'ἳ', 'ἵ', text)
    text = re.sub(r'ὃ', 'ὅ', text)
    text = re.sub(r'ὓ', 'ὕ', text)
    text = re.sub(r'ὣ', 'ὥ', text)
    text = re.sub(r'Ἃ', 'Ἅ', text)
    text = re.sub(r'Ἓ', 'Ἕ', text)
    text = re.sub(r'Ἣ', 'Ἥ', text)
    text = re.sub(r'Ἳ', 'Ἵ', text)
    text = re.sub(r'Ὃ', 'Ὅ', text)
    text = re.sub(r'Ὓ', 'Ὕ', text)
    text = re.sub(r'Ὣ', 'Ὥ', text)
    text = re.sub(r'ᾲ', 'ᾴ', text)
    text = re.sub(r'ῂ', 'ῄ', text)
    text = re.sub(r'ῲ', 'ῴ', text)
    text = re.sub(r'ᾂ', 'ᾄ', text)
    text = re.sub(r'ᾒ', 'ᾔ', text)
    text = re.sub(r'ᾢ', 'ᾤ', text)
    text = re.sub(r'ᾃ', 'ᾅ', text)
    text = re.sub(r'ᾓ', 'ᾕ', text)
    text = re.sub(r'ᾣ', 'ᾥ', text)
    text = re.sub(r'ῒ', 'ΐ', text)
    text = re.sub(r'ῢ', 'ΰ', text)
    return text

# remove punctuation from gutenberg texts
def removePunctGutenberg(text, debugString):
    text = re.sub(r'\[(page|\d|Illustration:[^\]]+)\]', ' ', text)
    text = re.sub(r'Æ', 'Ae', text)
    text = re.sub(r'æ', 'ae', text)
    text = re.sub(r'œ', 'oe', text)
    text = re.sub(r'Œ', 'Oe', text)
    text = re.sub(r'[—–‐]', '-', text)

    text = re.sub(r'--+', ' ', text)

    text = re.sub(r'[äàáâãāă]', 'a', text)
    text = re.sub(r'[ÂÀÁÄÃ]', 'A', text)
    text = re.sub(r'[ëèéêĕ]', 'e', text)
    text = re.sub(r'[ÈÉËÊĒ]', 'E', text)
    text = re.sub(r'[ïîìíĭ]', 'i', text)
    text = re.sub(r'[ÎÏ]', 'I', text)
    text = re.sub(r'[öôòóōŏ]', 'o', text)
    text = re.sub(r'[ÔÖÒ]', 'O', text)
    text = re.sub(r'[üûùúŭ]', 'u', text)
    text = re.sub(r'[ÛÜ]', 'U', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[Ç]', 'C', text)
    text = re.sub(r'[ñ]', 'n', text)
    text = re.sub(r'[Ñ]', 'N', text)
    # text = re.sub(r'[½]', ' 1/2 ', text)
    # text = re.sub(r'[¼]', ' 1/4 ', text)
    # text = re.sub(r'[¾]', ' 3/4 ', text)
    # text = re.sub(r'[⅛]', ' 1/8 ', text)
    # text = re.sub(r'…', ' ... ', text)

    # [], others?
    # matches = re.finditer(r'([\s\S]{30})([^A-Za-z0-9\s\-\(\)\.,;:?!`´′‘’“”″\"\'%$¢£—–‐\&\|~_^\\\/=@+#*×±¦°º¤·¶§«»©\[\]\{\}<>])([\s\S]{30})', text)
    # firstMatch = True
    # for m in matches:
    #     if (firstMatch):
    #         firstMatch = False
    #         print(debugString)
    #     print("<{%s~~%s~~%s}>" % (m.group(1), m.group(2), m.group(3)))
    #     #print("<{%s}>" % (m.group(0)))

    text = re.sub(r'[^A-Za-z\-\&\s]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    return text

# remove punctuation from shakespeare texts
def removePunctShakespeare(text, debugString):
    text = re.sub(r'<[^>]+>', ' ', text)
    text = text.replace("—", "-")
    text = text.replace("Æ", "Ae")
    text = text.replace("æ", "ae")
    text = text.replace("œ", "oe")
    text = text.replace("ç", "c")
    text = re.sub(r'[äàáâ]', 'a', text)
    text = re.sub(r'[ëèéê]', 'e', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[Ç]', 'C', text)

    # matches = re.finditer(r'([\s\S]{30})([^A-Za-z0-9\s!\"\',_.;:?\(\)\-])([\s\S]{30})', text)
    # firstMatch = True
    # for m in matches:
    #     if (firstMatch):
    #         firstMatch = False
    #         print(debugString)
    #     print("<{%s~~%s~~%s}>" % (m.group(1), m.group(2), m.group(3)))
    #     #print("<{%s}>" % (m.group(0)))

    text = re.sub(r'[^A-Za-z\-\&\s]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    return text

# remove punctuation from middle english texts
def removePunctME(text, debugString):
    text = re.sub(r'[ā]', 'a', text)
    text = re.sub(r'[ëèéē]', 'e', text)
    text = re.sub(r'[ïîìíĭ]', 'i', text)
    text = re.sub(r'[öóō]', 'o', text)
    text = re.sub(r'[úū]', 'u', text)
    text = re.sub(r'[ÿ]', 'y', text)



    # matches = re.finditer(r'([\s\S]{30})(ℏ)([\s\S]{30})', text)
    # firstMatch = True
    # for m in matches:
    #     if (firstMatch):
    #         firstMatch = False
    #         print(debugString)
    #     print("<{%s~~%s~~%s}>" % (m.group(1), m.group(2), m.group(3)))
    #     #print("<{%s}>" % (m.group(0)))

    text = re.sub(r'[^A-Za-z\-\s]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    return text

# remove punctuation from Old English texts
def removePunctOE(text, debugString):

    # matches = re.finditer(r'([\s\S]{30})(ℏ)([\s\S]{30})', text)
    # firstMatch = True
    # for m in matches:
    #     if (firstMatch):
    #         firstMatch = False
    #         print(debugString)
    #     print("<{%s~~%s~~%s}>" % (m.group(1), m.group(2), m.group(3)))
    #     #print("<{%s}>" % (m.group(0)))

    #ðþæ

    text.replace("ð", "th")
    text.replace("þ", "th")
    text.replace("æ", "ae") # looks like this always becomes "a" in modern english, but it's a different sound... TODO

    #text = re.sub(r'[^A-Za-z\-\s]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    return text

# remove punctuation from Icelandic icepahc texts
def removePunctIcepahc(text, debugString):

    # matches = re.finditer(r'([\s\S]{30})(ד)([\s\S]{30})', text)
    # firstMatch = True
    # for m in matches:
    #     if (firstMatch):
    #         firstMatch = False
    #         print(debugString)
    #     print("<{%s~~%s~~%s}>" % (m.group(1), m.group(2), m.group(3)))
    #     #print("<{%s}>" % (m.group(0)))

    text = re.sub(r'[-–—]', '-', text)

    text = text.lower()
    text = re.sub(r'[^A-Za-z\-\sáæéíðóöúüýþøǿẏȧėȯęıǫɛʜοωד]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


# remove punctuation from Icelandic icepahc texts
def removePunctSagas(text, debugString):

    # matches = re.finditer(r'([\s\S]{30})([])([\s\S]{30})', text)
    # firstMatch = True
    # for m in matches:
    #     if (firstMatch):
    #         firstMatch = False
    #         print(debugString)
    #     print("<{%s~~%s~~%s}>" % (m.group(1), m.group(2), m.group(3)))
    #     #print("<{%s}>" % (m.group(0)))

    text = re.sub(r'<teiHeader>[\s\S]*</teiHeader>', '', text)
    text = re.sub(r'<c type="punctuation">[^<]+</c>', '', text)
    text = re.sub(r'<[^>]+>', '', text)

    text = text.replace(".", "")
    text = text.replace("$", "")
    text = text.lower()
    text = re.sub(r'[^A-Za-z\-\sáàâäåæçéèêëíìîïðñóôõöœúüûýþøǿẏȧėȯęıǫɛʜοωדßšƒ]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


# ==============================================================================
# ==============================================================================
# ==============================================================================

# parse the TEI data for a full book
def parse_TEI_full_book(xml):
    # remove notes, bibliography, heads, and foreign languages
    noNotes = re.sub(r'<note[\S\s]*?/note>', " ", xml)
    noBibl = re.sub(r'<bibl[\S\s]*?/bibl>', " ", noNotes)
    noHead = re.sub(r'<head[\S\s]*?/head>', " ", noBibl)
    noForeign = re.sub(r'<foreign lang="(la|en)"[\S\s]*?/foreign>', " ", noHead)
    noForeign = re.sub(r'<p lang="(la|en)"[\S\s]*?/p>', " ", noForeign)
    # remove all the xml tags since we just need the whole text
    noTags = re.sub(r'<[^>][\S\s]*?>', " ", noForeign)
    return noTags
