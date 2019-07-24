# Go through all English texts and convert them to simple text, removing punctuation, etc
import utils
import unicodedata
import os
import re
from modernEnglishTextList import authorWorks


def parseEnglish():
    # If True we split each author into author_prose and author_poetry based on text genre
    # If False, we determine majority class and remove texts not of that work
    splitGenre = False


    RAW_FOLDER = "../rawTexts/english/"
    PARSED_FOLDER = "english/"

    authors = {}
    allBooks = []
    numTexts = 0
    numTexts2 = 0
    available = []

    # ==============================================================================
    # ==============================================================================
    # get all Gutenberg texts
    gutenbergFolder = RAW_FOLDER + "Gutenberg/txt/"
    textList = os.listdir(gutenbergFolder)

    i = 0;
    for author in authorWorks:
        baseAuthorName = author["authorName"]

        # determine whether this author has texts of both genre
        numProse = 0
        numPoetry = 0
        for text in author["works"]:
            workName = text["textName"]
            if (text["genre"] == 0):
                numProse += 1
            elif (text["genre"] == 1):
                numPoetry += 1

        specifyGenre = numProse > 0 and numPoetry > 0
        moreProse = numProse > numPoetry


        for text in author["works"]:
            authorName = baseAuthorName

            # if we are splitting authors by genre, append genre to the "author"
            # of this book as necessary
            if (splitGenre):
                if (specifyGenre):
                    if (text["genre"] == 0):
                        authorName += "_Prose"
                    else:
                        authorName +=  "_Poetry"

            else:# ignore texts of minority genre for this author
                if (not(moreProse) and text["genre"] == 0) or (moreProse and text["genre"] == 1):
                    continue


            # Ceate a work with each of the given books
            workName = text["textName"]
            newLocation = "%s%s-%s.json" % (PARSED_FOLDER, authorName, workName)
            workObject = {"name": workName, "location": "texts/" + newLocation}
            numTexts += 1

            books = []
            bookIndex = 1
            for b in text["books"]:
                books.append((gutenbergFolder + b, bookIndex))
                bookIndex += 1

            if authorName in authors:
                authors[authorName]["works"].append(workObject)
            else:
                authors[authorName] = {"author": authorName, "works": [workObject]}



            print(i, end=" ", flush=True)
            # Create a new gutenberg text for this text.
            try:
                t = utils.GutenbergText(authorName, workName, books)
                numTexts2 += len(books)
                res = t.convert()
                allBooks.extend(res["booksRaw"])
                utils.safeWrite(newLocation, res, True)
            except Exception as e:
                print(newLocation)
                print(e)

            i += 1

    # ==============================================================================
    # ==============================================================================
    # get Shakespeare
    for playType in ["comedies", "historical", "tragedies"]:
        shakeFolder = RAW_FOLDER + "ShakespearePlaysPlus/%s/" % playType
        textList = os.listdir(shakeFolder)

        for textName in textList:
            if (textName[-4:] == ".txt"):
                numTexts += 1
                authorName = "Shakespeare"
                workName = textName.replace(" ", "_")
                print(workName)
                newLocation = "%s%s-%s.json" % (PARSED_FOLDER, authorName, workName)
                workObject = {"name": workName, "location": "texts/" + newLocation}
                if authorName in authors:
                    authors[authorName]["works"].append(workObject)
                else:
                    authors[authorName] = {"author": authorName, "works": [workObject]}

                t = utils.ShakespeareText(authorName, workName, shakeFolder + textName)
                res = t.convert()
                allBooks.extend(res["booksRaw"])
                utils.safeWrite(newLocation, res, True)

    # ==============================================================================
    # ==============================================================================
    # get Middle English-y texts
    middleFolder = RAW_FOLDER + "ME/"
    textList = os.listdir(middleFolder)

    for textName in textList:
        split = textName[:-4].split("___")
        if (textName[-4:] == ".txt"):
            numTexts += 1
            authorName = split[0].replace(" ", "_")
            workName = split[1].replace(" ", "_")
            print(workName)
            newLocation = "%s%s-%s.json" % (PARSED_FOLDER, authorName, workName)
            workObject = {"name": workName, "location": "texts/" + newLocation}
            if authorName in authors:
                authors[authorName]["works"].append(workObject)
            else:
                authors[authorName] = {"author": authorName, "works": [workObject]}

            t = utils.METext(authorName, workName, middleFolder + textName)
            res = t.convert()
            allBooks.extend(res["booksRaw"])
            utils.safeWrite(newLocation, res, True)



    # ==============================================================================
    # Old English and 21st century corpus did not end up being included.

    # get 21st century texts
    # tfFolder = RAW_FOLDER + "21st/"
    # textList = os.listdir(tfFolder)
    #
    # for textName in textList:
    #     split = textName[:-4].split("___")
    #     if (textName[-4:] == ".txt"):
    #         numTexts += 1
    #         authorName = split[0].replace(" ", "_")
    #         workName = split[1].replace(" ", "_")
    #         print(workName)
    #         newLocation = "%s%s-%s.json" % (PARSED_FOLDER, authorName, workName)
    #         workObject = {"name": workName, "location": "texts/" + newLocation}
    #         if authorName in authors:
    #             authors[authorName]["works"].append(workObject)
    #         else:
    #             authors[authorName] = {"author": authorName, "works": [workObject]}
    #
    #         t = utils.TFText(authorName, workName, tfFolder + textName)
    #         res = t.convert()
    #         allBooks.extend(res["booksRaw"])
    #         utils.safeWrite(newLocation, res, True)


    # Old English
    # oeFolder = RAW_FOLDER + "OE/"
    # textList = os.listdir(tfFolder)
    #
    # for textName in textList:
    #     split = textName[:-4].split("___")
    #     if (textName[-4:] == ".txt"):
    #         numTexts += 1
    #         authorName = split[0].replace(" ", "_")
    #         workName = split[1].replace(" ", "_")
    #         print(workName)
    #         newLocation = "%s%s-%s.json" % (PARSED_FOLDER, authorName, workName)
    #         workObject = {"name": workName, "location": "texts/" + newLocation}
    #         if authorName in authors:
    #             authors[authorName]["works"].append(workObject)
    #         else:
    #             authors[authorName] = {"author": authorName, "works": [workObject]}
    #
    #         t = utils.OEText(authorName, workName, oeFolder + textName)
    #         res = t.convert()
    #         allBooks.extend(res["booksRaw"])
    #         utils.safeWrite(newLocation, res, True)
    #

    for author in authors:
        available.append(authors[author])

    utils.safeWrite(PARSED_FOLDER + "available.json", available, True)
    print("Done.")

    # Optionally count the characters inthe corpus. This is done to find weird
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
    parseEnglish()
