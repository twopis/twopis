# Go through all downloaded raw texts and convert them to simple text, removing punctuation, etc
import utils
import unicodedata
import os
import re

from icelandicTextList import icepahcList, sagasList, modernBookList

def parseIcelandic():
    RAW_FOLDER = "../rawTexts/icelandic/"
    PARSED_FOLDER = "icelandic/"

    authors = {}
    allBooks = []
    numTexts = 0
    numTexts2 = 0
    available = []

    allNames = []

    # ==============================================================================
    # ==============================================================================
    # get texts from icepahc
    icepahcFolder = RAW_FOLDER + "icepahc-v0.9/txt/"

    for text in icepahcList:
        numTexts += 1
        authorName = text["author"]
        workName = text["title"]
        id = text["id"]

        textName = id + ".txt"
        allNames.append(workName)
        newLocation = "%s%s-%s.json" % (PARSED_FOLDER, authorName, workName)
        workObject = {"name": workName, "location": "texts/" + newLocation}
        if authorName in authors:
            authors[authorName]["works"].append(workObject)
        else:
            authors[authorName] = {"author": authorName, "works": [workObject]}

        t = utils.IcepahcText(authorName, workName, icepahcFolder + textName)
        res = t.convert()
        allBooks.extend(res["booksRaw"])
        utils.safeWrite(newLocation, res, True)


    # ==============================================================================
    # ==============================================================================
    # get texts from sagas
    sagasFolder = RAW_FOLDER + "textar/fornritin/xml/"

    for text in sagasList:
        numTexts += 1
        if (text["id"] == "F1E"):
            authorName == "Snorri_Sturluson"
        else:
            authorName = "Anon_" + text["id"]
        workName = text["title"].strip().replace(" ", "_")
        allNames.append(workName + "#" + text["id"])
        newLocation = "%s%s-%s.json" % (PARSED_FOLDER, authorName, workName)
        workObject = {"name": workName, "location": "texts/" + newLocation}
        if authorName in authors:
            authors[authorName]["works"].append(workObject)
        else:
            authors[authorName] = {"author": authorName, "works": [workObject]}

        t = utils.SagasText(authorName, workName, sagasFolder + text["id"] + ".xml")
        res = t.convert()
        allBooks.extend(res["booksRaw"])
        utils.safeWrite(newLocation, res, True)

    # ==============================================================================
    # ==============================================================================
    # get books from MIM corpus
    modernBooksFolder = RAW_FOLDER + "MIM/baekur/"

    # For each text in the list, download it
    for text in modernBookList:
        numTexts += 1
        authorName = text["author"].strip().replace(" ", "_")
        workName = text["title"].strip().replace(" ", "_")

        allNames.append(workName + "#" + text["id"])
        newLocation = "%s%s-%s.json" % (PARSED_FOLDER, authorName, workName)
        workObject = {"name": workName, "location": "texts/" + newLocation}
        if authorName in authors:
            authors[authorName]["works"].append(workObject)
        else:
            authors[authorName] = {"author": authorName, "works": [workObject]}

        # MIM texts are in the same format as Saga texts so this works fine.
        t = utils.SagasText(authorName, workName, modernBooksFolder + text["id"] + ".xml")
        res = t.convert()
        allBooks.extend(res["booksRaw"])
        utils.safeWrite(newLocation, res, True)

    for author in authors:
        available.append(authors[author])

    utils.safeWrite(PARSED_FOLDER + "available.json", available, True)
    print("Done.")


    # Optionally count the characters in the corpus. This is done to find weird
    # Unicode artifacts to make sure it gets removed in the cleaning step.
    countChars = False#True#
    if countChars:
        print("Counting Chars")
        chars = {}
        for b in allBooks:
            bookText = b["bookText"]
            for char in bookText:
                chars[char] = True

        sortedChars = sorted(list(chars.keys()))


        for c in sortedChars:
            utils.printUnicodeChar(c)
        print("======")

        # If true, show the set of unique characters when things are decomposed
        if False:
            decomposedChars = {}
            for c in sortedChars:
                res = utils.fullyDecomposeUnicodeChar(c)
                for newC in res:
                    decomposedChars[newC] = True

            sortedDecompChars = sorted(list(decomposedChars.keys()))

            for c in sortedDecompChars:
                utils.printUnicodeChar(c)

if __name__ == "__main__":
    parseIcelandic()
