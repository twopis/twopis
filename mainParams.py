# store some key parameters used by multiple files
import wordToPOSDicts as wtp
import random
import numpy as np

SEED = 2018
random.seed(SEED)
np.random.seed(SEED)
# default: output

# True if we should run all analyses, even the ones that aren't used for the paper.
RUN_EVERYTHING = False


# Minimum number of tokens necessary to include a book
MIN_TOKENS_NECESSARY = 1000

# Language to focus on when running individual parts.
language = "Greek"
# language = "English"
# language = "Icelandic"



topNum = 145
comparableTopNum = 172;
poetryNum = 100
topStr = "top%d" % topNum
comparableTopStr = "top%d" % comparableTopNum
topPlusPStr = topStr + "+p"

# tops consist of:
# Name, All words, poetry words, subset size, split parameter, includeBooks,
#     includeGraphs, examine +1smoothing and remainder for metrics, word to part of speech dictionary
languageInfo = {
    "Greek": {
        "rawTextLocation": "rawTexts/greek/",
        "textLocation": "texts/greek/",
        "saveDir": "output/greek/",
        "tops": [
            # These four allow author-internal comparison below; since we
            # don't end up using this they are commented out for now.
            # (topStr, topNum, -1, -1, -2, True, False, False, wtp.greek),
            # (topStr, topNum, -1, -1, 5, True, False, False, wtp.greek),
            # (topPlusPStr, topNum, poetryNum, -1, -2, True, False, False, wtp.greek),
            # (topPlusPStr, topNum, poetryNum, -1, 5, True, False, False, wtp.greek),
            # Main analysis with top 145 and top 145 + poetry
            (topStr, topNum, -1, -1, -1, True, True, False, wtp.greek),
            (comparableTopStr, comparableTopNum, -1, -1, -1, True, False, False, wtp.greek),
            (topPlusPStr, topNum, poetryNum, -1, -1, True, True, True, wtp.greek),
            # This lets us count the order of top poetry words
            ("top_p", 0, poetryNum, -1, -1, False, False, False, wtp.greek),
        ]
    },
    "English": {
        "rawTextLocation": "rawTexts/english/",
        "textLocation": "texts/english/",
        "saveDir": "output/english/",
        "tops": [
            (topStr, topNum, -1, -1, -1, False, False, False, wtp.english),
            (topPlusPStr, topNum, poetryNum, -1, -1, False, False, False, wtp.english),
        ]
    },
    "Icelandic": {
        "rawTextLocation": "rawTexts/icelandic/",
        "textLocation": "texts/icelandic/",
        "saveDir": "output/icelandic/",
        "tops": [
            (topStr, topNum, -1, -1, -1, False, False, False, wtp.icelandic),
        ]
    }
}

# By default we don't consider a subset of the author's work or split authors.
subsetSize = -1;
splitParameter = -1;

addPoetry = True

# =====

textLocation = languageInfo[language]["textLocation"]
tops = languageInfo[language]["tops"]

# get the poper save directory
def getSaveDir(lang, langInfo, splitParam):
    saveDir = langInfo[lang]["saveDir"]

    # separate data based on how authors were split
    if (splitParam == -1):
        splitStr = "no_split"
    else:
        splitStr = "split%d" % splitParam
    saveDir += splitStr

    saveDir += "/"
    return saveDir
