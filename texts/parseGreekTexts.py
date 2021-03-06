# Go through all downloaded raw texts and convert them to simple text, removing XML and punctuation
import utils
import unicodedata

def parseGreek():
    RAW_FOLDER = "../rawTexts/greek/"
    PARSED_FOLDER = "greek/"

    # given a location, convert it from XML to the format we want
    def convertBook(location):
        filename = loc.replace(RAW_FOLDER, "")
        newLoc = PARSED_FOLDER+filename
        t = utils.XMLText(loc)
        res = t.convertFromXML()
        utils.safeWrite(newLoc, res, True)
        return "texts/" + newLoc, res["booksRaw"]


    available_raw = utils.getContent(RAW_FOLDER + "perseus_texts/available.json", True)
    available = []


    for o in available_raw:
        # if (o['author'] == "Anonymous(Hymns_Dionysus)" or o['author'] == "Euclid"):
        #     continue
        # else:
        available.append(o)


    numTexts = 0
    for o in available:
        workLocs = o["works"]
        for w in workLocs:
            numTexts += 1

    i = 1
    allBooks = []
    for o in available:
        workLocs = o["works"]
        for w in workLocs:
            if (i % 20 == 0):
                print("%d out of %d (%.2f%%)" % (i, numTexts, (100*i/numTexts)))
            loc = RAW_FOLDER + w["location"]
            newLoc, books = convertBook(loc)
            allBooks.extend(books)
            w["location"] = newLoc
            i += 1

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
    parseGreek()
