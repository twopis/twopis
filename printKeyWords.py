# -*- coding: utf-8 -*-
# print occurrences of the key words calculated by
# makeBasicGraphs and placed at output/_sub_/wordImportance/keyWords
import utils
import os
from printWordOccurrences import printWordOccurrences as printOccs
import mainParams as mp

# Print the saved list of keywords
def printKeyWords(dataSplit, top, subsetSize, language, saveDirBase):
    topName, _, _ = top
    # calculate save directory based on input parameters
    saveDir = saveDirBase + "%s" % (topName)

    keyWordsDir = saveDir+"/wordImportance/keyWords/"

    # find all the relevant json files
    files = os.listdir(keyWordsDir)
    for f in files:
        if f[-5:] == ".json":
            nameCore = f.split(".json")[0]

            # get the word info for this author pair
            words = utils.getContent(keyWordsDir + f, True)

            # get the authors
            authors = nameCore.split("_")
            a1 = authors[0]
            a2 = authors[1]
            print(a1, a2)

            # save dir for new files
            wordsDir = keyWordsDir + nameCore + "/"

            # gather the list of words and print them out along with percentiles
            wordList = []
            out = ["index, percentile, token"]
            for word in words:
                wordList.append("%03d_%s" % (words[word][0]+1, word))
                out.append("%d, %.2f, %s" % (words[word][0], words[word][1], word))

            utils.safeWrite(wordsDir + "words.txt", "\n".join(out))

            # get the info for each occurrence of the given words
            # associated with these authors
            target = {
                a1: wordList,
                a2: wordList,
            }
            printOccs(wordsDir, target, language)



if __name__ == "__main__":
    for top in mp.tops:
        name, topWords, poetryWords, subsetSize, splitParameter, includeBooks, includeGraphs, _, _ = top
        newTop = (name, topWords, poetryWords)
        saveDir = mp.getSaveDir(mp.language, mp.languageInfo, splitParameter)

        printKeyWords(plitParameter, newTop, subsetSize, mp.language, saveDir)
