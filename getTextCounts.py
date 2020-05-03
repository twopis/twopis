# -*- coding: utf-8 -*-
# Get word count dictionaries for all texts.
import re
import subprocess
import os

import utils
import mainParams as mp

# Calculate token frequencies for all given texts and save them in textCounts.
def getTextCounts(textLocation, saveDir):
    subprocess.run("cp %savailable.json %savailable.json" % (textLocation, saveDir), shell=True)

    available = utils.getContent(textLocation + "available.json", True)
    # For each available text
    for i, o in enumerate(available):
        if (i % 20 == 0):
            print(i, end=" ", flush=True)

        workLocs = o["works"]

        # Process each work
        for w in workLocs:
            t = utils.getContent(w["location"], True)

            booksRaw = t["booksRaw"]
            booksCounts = []
            for b in booksRaw:
                rawTokens = re.sub(r'\.,;:᾽῾\'', "", b["bookText"]).split(" ")
                tokenCounts = {}
                for token in rawTokens:
                    if (token == ""):
                        continue

                    if not(token in tokenCounts):
                        tokenCounts[token] = 1
                    else:
                        tokenCounts[token] += 1

                bookWithCounts = {}
                bookWithCounts["bookNumber"] = b["bookNumber"]
                bookWithCounts["bookTokenCounts"] = tokenCounts
                bookWithCounts["bookText"] = ""

                booksCounts.append(bookWithCounts)

            t["booksRaw"] = booksCounts

            # Remove "texts/" from start
            filename = "textCounts/" + w["location"][6:]
            utils.safeWrite(filename, t, True)


languages = ["Greek", "English", "Icelandic"]
for language in languages:
    textLocation = mp.languageInfo[language]["textLocation"]

    saveDir = "textCounts/%s/" % language.lower()
    if not(os.path.exists(saveDir)):
        subprocess.run("mkdir " + saveDir, shell=True)

    print("Getting token counts for each %s texts..." % language)
    getTextCounts(textLocation, saveDir)
