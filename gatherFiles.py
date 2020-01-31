# -*- coding: utf-8 -*-
# After execution of the main pipeline, files are organized in a variety of
# locations, and some information is spread across multiple files. This
# gathers various charts and creates tables using provided data, storing it
# all in folders organized by paper section.
import utils
import graphUtils
import numpy as np
import scipy.stats as stats
import os
import re
import subprocess

import mainParams as mp
from groupWords import getWordGroupsRangeTest


# ==============================================================================
# ==============================================================================

# Color constants for heat-map tables
COLOR_BLUE = (66, 134, 244)
COLOR_ORANGE = (244, 179, 66)
COLOR_GRAY = (239, 239, 239)

# given a start color, an end color, and a current value within a min-max
# range, find a linear interpolation between start and end color
def colorConvert(min, max, current, startColor, endColor):
    sr, sg, sb = startColor
    er, eg, eb = endColor
    scale = (current - min) / (max - min)
    red = sr + scale*(er-sr)
    green = sg + scale*(eg-sg)
    blue = sb + scale*(eb-sb)
    return (red/255, green/255, blue/255)


# create tables with information evaluating given metrics
def makeMetricEvalTables(suffix, topStr, comparableTopStr, topNum, poetryNum, comparableNum, simMetrics, baseFolder):
    baseScoreInfo = [
        ("Cosine", 0),
        ("Burrows' Delta", 0),
    ]

    bestMetricName = "Jensen-Shannon (250)" #Jensen-Shannon+p
    bestMetricSigWork = []
    bestMetricSigAuthor = []

    evalTableOutput = []
    evalTableOutput.append("""\\begin{table}[!bt]
  \\centering
  \\def\\arraystretch{1}
  \\begin{tabular}{| l | r | r |}
\\hline
 & \\multicolumn{2}{c|}{\\textbf{Percentage of segments most similar to a segment...}} \\\\

\\textbf{Metric}& \\textbf{from the same work} & \\textbf{by the same author} \\\\\\hline
""")


    sameWorkTableOutput = []
    sameAuthorTableOutput = []
    temp = """\\begin{table}[!bt]
  \\centering
  \\def\\arraystretch{1}
  \\begin{tabular}{| l | c | c | c |}
\\hline
    """
    sameWorkTableOutput.append(temp)
    sameAuthorTableOutput.append(temp)

    temp = "& & \\textbf{Top %d +} & \\\\" % (topNum)
    sameWorkTableOutput.append(temp)
    sameAuthorTableOutput.append(temp)

    temp = "\\textbf{Metric}& \\textbf{Top %d} & \\textbf{Top %d in Poetry} & \\textbf{Top %d} \\\\\\hline" % (topNum, poetryNum, comparableNum)
    sameWorkTableOutput.append(temp)
    sameAuthorTableOutput.append(temp)

    workSigReport = []
    authorSigReport = []


    # & \\textbf{Sim to another work} & \\textbf{Closest to diff author} & \\textbf{Median}

    # Get the list of authors and works the metric got correct
    scoreLists = {}
    for simMetric in simMetrics:
        dir, metricName = simMetric
        scoreLists[metricName] = {}
        for i, params in enumerate([(False, False), (True, False), (False, True), ]):
            name = metricName
            addP, comparable = params
            metricTopStr = topStr
            if addP:
                metricTopStr += "+p"
                name += "+p"
            # look at comparable number of non-poetry words
            elif comparable:
                metricTopStr = comparableTopStr
                name += " (%d)" % comparableNum
            else:
                name += " (%d)" % topNum

            fname = "output/greek/no_split/%s/%s/metric/Books/scores.json" % (metricTopStr, dir)
            scores = utils.getContent(fname, True)
            scoreLists[metricName][i] = scores
            scoreLists[metricName][i]["name"] = name

    baseScores = []
    for bsi in baseScoreInfo:
        baseScoreMetric, baseScoreIndex = bsi
        baseScores.append(scoreLists[baseScoreMetric][baseScoreIndex])

    # Create a table of the information using the provided scores
    for metricName in scoreLists:
        cell2 = "\\textbf{%s}" % (metricName)
        cell3 = "\\textbf{%s}" % (metricName)
        for i in scoreLists[metricName]:
            currentScores = scoreLists[metricName][i]
            authorScores = currentScores["author"]
            workScores = currentScores["work"]
            name = currentScores["name"]
            sameWork = "%.2f%%" % (100*np.mean(workScores))
            sameAuth = "%.2f%%" % (100*np.mean(authorScores))
            # sameWork = "%.2f%%, (%d/%d)" % (100*np.mean(workScores), np.sum(workScores), len(workScores))
            # sameAuth = "%.2f%%, (%d/%d)" % (100*np.mean(authorScores), np.sum(authorScores), len(authorScores))

            # cell = "%s & %s & %s & %s & %s & %s" % (name, sameAuth, sameWork, otherWork, diffAuthClosest, median)
            cell = "%s & %s & %s" % (name, sameWork, sameAuth)
            cell = cell.replace("%", "\\%")
            evalTableOutput.append("%s\\\\\\hline" % cell)

            cell2 += " & %s" % (sameWork) # work_p
            cell3 += " & %s" % (sameAuth) # , author_p)

            for j, baseScore in enumerate(baseScores):
                a = baseScore["work"]
                b = currentScores["work"]
                work_t, work_p = stats.ttest_rel(a, b)
                workSigReport.append(name)
                # Degrees of freedom
                df = len(b) - 1
                workSig = "  (M=%.3f, SD=%.3f) t(%d)=%.3f, p=%.3e" % (np.mean(b), np.std(b), df, work_t, work_p)
                workSigReport.append(workSig)


                a = baseScore["author"]
                b = currentScores["author"]
                author_t, author_p = stats.ttest_rel(a, b)
                authorSigReport.append(name)
                # Degrees of freedom
                df = len(b) - 1
                authorSig = "  (M=%.3f, SD=%.3f) t(%d)=%.3f, p=%.3e" % (np.mean(b), np.std(b), df, author_t, author_p)
                authorSigReport.append(authorSig)

                if (name == bestMetricName or name == baseScore["name"]):
                    bestMetricSigWork.append("%s vs %s" % (name, baseScore["name"]))
                    bestMetricSigWork.append(workSig)

                    bestMetricSigAuthor.append("%s vs %s" % (name, baseScore["name"]))
                    bestMetricSigAuthor.append(authorSig)

                #print("  Author: t-statistic = %6.3f pvalue = %f" %  stats.ttest_rel(a, b))

                # Significance notes
                if (j == 0):
                    if (work_p < 0.01):
                        cell2 += "\\textbf{†}"
                    elif (work_p < 0.05):
                        cell2 += "\\textbf{*}"
                    if (author_p < 0.01):
                        cell3 += "\\textbf{†}"
                    elif (author_p < 0.05):
                        cell3 += "\\textbf{*}"
                else:
                    if (work_p < 0.01):
                        cell2 += "\\textbf{‡}"
                    if (author_p < 0.01):
                        cell3 += "\\textbf{‡}"



        cell2 = cell2.replace("%", "\\%")
        sameWorkTableOutput.append("%s\\\\\\hline" % cell2)

        cell3 = cell3.replace("%", "\\%")
        sameAuthorTableOutput.append("%s\\\\\\hline" % cell3)

    evalTableOutput.append("""
      \\end{tabular}
      \\caption{How well similarity metrics identify whether two segments come from the same work or the same author.}
      \\label{table:metric_eval}
    \\end{table}
    """)

    utils.safeWrite("%smetric/extraInfo/metricEvalTable%s.tex" % (baseFolder, suffix), "\n".join(evalTableOutput))

    sameWorkTableOutput.append("\\end{tabular}")
    sameWorkTableOutput.append("\\caption[How well similarity metrics based on a given set of words identify whether two segments come from the same work.]{")
    sameWorkTableOutput.append("How well similarity metrics based on a given set of words identify whether two segments come from the same work. \\newline")
    sameWorkTableOutput.append("†: Results very significant (p < 0.01) when compared to %s. \\newline" % baseScores[0]["name"])
    sameWorkTableOutput.append("*: Results significant (p < 0.05) when compared to %s. \\newline" % baseScores[0]["name"])
    sameWorkTableOutput.append("‡: Results very significant (p < 0.01) when compared to %s. " % baseScores[1]["name"])
    sameWorkTableOutput.append("}")
    sameWorkTableOutput.append("\\label{table:metric_eval_work}")
    sameWorkTableOutput.append("\\end{table}")

    utils.safeWrite("%smetric/sameWorkEvalTable%s.tex" % (baseFolder, suffix), "\n".join(sameWorkTableOutput))


    sameAuthorTableOutput.append("\\end{tabular}")
    sameAuthorTableOutput.append("\\caption[How well similarity metrics based on a given set of words identify whether two segments come from the same author.]{")
    sameAuthorTableOutput.append("How well similarity metrics based on a given set of words identify whether two segments come from the same author. \\newline")
    sameAuthorTableOutput.append("†: Results very significant (p < 0.01) when compared to %s. \\newline" % baseScores[0]["name"])
    sameAuthorTableOutput.append("*: Results significant (p < 0.05) when compared to %s. \\newline" % baseScores[0]["name"])
    sameAuthorTableOutput.append("‡: Results very significant (p < 0.01) when compared to %s. " % baseScores[1]["name"])
    sameAuthorTableOutput.append("}")
    sameAuthorTableOutput.append("\\label{table:metric_eval_author}")
    sameAuthorTableOutput.append("\\end{table}")

    utils.safeWrite("%smetric/sameAuthorEvalTable%s.tex" % (baseFolder, suffix), "\n".join(sameAuthorTableOutput))


    sigReport = "Work:\n" + ("\n".join(bestMetricSigWork)) + "\n\n-------------\n\nAuthor:\n" + ("\n".join(bestMetricSigAuthor))
    utils.safeWrite("%smetric/bestMetricSignificance%s.txt" % (baseFolder, suffix), sigReport)
    # utils.safeWrite("%smetric/bestMetricSignificanceWork%s.txt" % (baseFolder, suffix), "\n".join(bestMetricSigWork))
    # utils.safeWrite("%smetric/bestMetricSignificanceAuthor%s.txt" % (baseFolder, suffix), "\n".join(bestMetricSigAuthor))


    utils.safeWrite("%smetric/extraInfo/metricSignificanceReportWork%s.txt" % (baseFolder, suffix), "\n".join(workSigReport))
    utils.safeWrite("%smetric/extraInfo/metricSignificanceReportAuthor%s.txt" % (baseFolder, suffix), "\n".join(authorSigReport))




# create tables with information evaluating performance of each metric with/without
# smoothing and remainder words
def makeMetricInternalTables(suffix, topStr, simMetrics, baseFolder):
    metricInternalTables = []
    for simMetric in simMetrics:
        dir, metricName = simMetric

        # skip Jensen-Shannon
        if metricName == "Jensen-Shannon":
            continue

        tableOutput = []
        temp = """
\\begin{table}[!bt]
  \\centering
  \\def\\arraystretch{1}
  \\begin{tabular}{| l | c | c | c |}
\\hline
        """
        tableOutput.append(temp)

        temp = "\\textbf{Metric Options} & \\textbf{Author} & \\textbf{Work} & \\textbf{Total} \\\\\\hline"
        tableOutput.append(temp)

        workSigReport = []
        authorSigReport = []
        totalSigReport = []

        # & \\textbf{Sim to another work} & \\textbf{Closest to diff author} & \\textbf{Median}

        metricOptions = [
            ("Baseline", "-remainder-smoothed"),
            ("+1 Smoothing", "-remainder+smoothed"),
            ("Remainder", "+remainder-smoothed"),
            ("Both", "+remainder+smoothed")
        ]

        # Get the list of authors and works the metric got correct
        scoreLists = {}
        for _, opt in metricOptions:
            scoreLists[opt] = {}
            name = opt
            # Use Poetry Words
            metricTopStr = topStr

            fname = "output/greek/no_split/%s/%s/metric%s/Books/scores.json" % (metricTopStr, dir, opt)
            scores = utils.getContent(fname, True)
            scoreLists[opt] = scores
            scoreLists[opt]["name"] = name

        baseScore = scoreLists["-remainder-smoothed"]
        # baseScores = []
        # for bsi in baseScoreInfo:
        #     baseScoreMetric, baseScoreIndex = bsi
        #     baseScores.append(scoreLists[baseScoreMetric][baseScoreIndex])

        # Create a table of the information using the provided scores
        for optName, opt in metricOptions:
            cell = "\\textbf{%s}" % (optName)

            currentScores = scoreLists[opt]
            authorScores = currentScores["author"]
            workScores = currentScores["work"]
            name = currentScores["name"]
            sameWork = "%.2f%%, (%d/%d)" % (100*np.mean(workScores), np.sum(workScores), len(workScores))
            sameAuth = "%.2f%%, (%d/%d)" % (100*np.mean(authorScores), np.sum(authorScores), len(authorScores))
            all = np.concatenate((workScores, authorScores))
            total = "%.2f%%, (%d/%d)" % (100*np.mean(all), np.sum(all), len(all))

            wrk = " & %s" % (sameWork)
            auth = " & %s" % (sameAuth)
            tot = " & %s" % (total)


            # Calculate significance
            a = baseScore["work"]
            b = currentScores["work"]
            work_t, work_p = stats.ttest_rel(a, b)
            workSigReport.append(name)
            # Degrees of freedom
            df = len(b) - 1
            workSig = "  (M=%.3f, SD=%.3f) t(%d)=%.3f, p=%.3e" % (np.mean(b), np.std(b), df, work_t, work_p)
            workSigReport.append(workSig)


            a = baseScore["author"]
            b = currentScores["author"]
            author_t, author_p = stats.ttest_rel(a, b)
            authorSigReport.append(name)
            # Degrees of freedom
            df = len(b) - 1
            authorSig = "  (M=%.3f, SD=%.3f) t(%d)=%.3f, p=%.3e" % (np.mean(b), np.std(b), df, author_t, author_p)
            authorSigReport.append(authorSig)


            a = np.concatenate((baseScore["work"], baseScore["author"]))
            b = np.concatenate((currentScores["work"], currentScores["author"]))
            all_t, all_p = stats.ttest_rel(a, b)
            totalSigReport.append(name)
            # Degrees of freedom
            df = len(b) - 1
            totalSig = "  (M=%.3f, SD=%.3f) t(%d)=%.3f, p=%.3e" % (np.mean(b), np.std(b), df, all_t, all_p)
            totalSigReport.append(totalSig)


            # if (name == bestMetricName or name == baseScore["name"]):
            #     bestMetricSigWork.append("%s vs %s" % (name, baseScore["name"]))
            #     bestMetricSigWork.append(workSig)
            #
            #     bestMetricSigAuthor.append("%s vs %s" % (name, baseScore["name"]))
            #     bestMetricSigAuthor.append(authorSig)

            #print("  Author: t-statistic = %6.3f pvalue = %f" %  stats.ttest_rel(a, b))

            # Significance notes
            if (work_p < 0.01):
                wrk += "\\textbf{†}"
            elif (work_p < 0.05):
                wrk += "\\textbf{*}"
            if (author_p < 0.01):
                auth += "\\textbf{†}"
            elif (author_p < 0.05):
                auth += "\\textbf{*}"
            if (all_p < 0.01):
                tot += "\\textbf{†}"
            elif (all_p < 0.05):
                tot += "\\textbf{*}"

            # wrk += " %.4f" % work_p
            # auth += " %.4f" % author_p
            # tot += " %.4f" % all_p

            cell += "%s%s%s" % (wrk, auth, tot)

            cell = cell.replace("%", "\\%")
            tableOutput.append("%s\\\\\\hline" % cell)

        tableOutput.append("\\end{tabular}")
        tableOutput.append("\\caption{")
        tableOutput.append("How well %s performs with the remainder words and smoothing included. " % metricName)
        tableOutput.append("†: Results very significant (p < 0.01) when compared to baseline. ")
        tableOutput.append("*: Results significant (p < 0.05) when compared to baseline. ")
        tableOutput.append("}")
        tableOutput.append("\\label{table:metric_options_eval_%s}" % dir)
        tableOutput.append("\\end{table}")

        tableOutput.append("")
        tableOutput.append("")
        metricInternalTables.append("\n".join(tableOutput))
        utils.safeWrite("%smetric/%s_optionsEvalTable%s.tex" % (baseFolder, metricName, suffix), "\n".join(tableOutput))

        # sigReport = "Work:\n" + ("\n".join(bestMetricSigWork)) + "\n\n-------------\n\nAuthor:\n" + ("\n".join(bestMetricSigAuthor))
        # utils.safeWrite("%smetric/bestMetricSignificance%s_2.txt" % (baseFolder, suffix), sigReport)

        # utils.safeWrite("%smetric/extraInfo/metricSignificanceReportWork%s_2.txt" % (baseFolder, suffix), "\n".join(workSigReport))
        # utils.safeWrite("%smetric/extraInfo/metricSignificanceReportAuthor%s_2.txt" % (baseFolder, suffix), "\n".join(authorSigReport))
    utils.safeWrite("%smetric/extraInfo/optionsEvalTables%s.tex" % (baseFolder, suffix), "\n".join(metricInternalTables))


# Get author pairs for authors 4 centuries apart with high similarity.
def fourCenturiesTables(topStr, simMetrics, baseFolder):
    comparisonOutput = []
    topSimsToExamine = 100

    # Grab this from the best metric
    authorSims = utils.getContent("output/greek/no_split/%s/jensen-shannon/metric/Authors/sims.txt" % (topStr), False).split("\n")
    topDistantSims = []
    topDistantAuthors = {}
    for i, sim in enumerate(authorSims):
        centuries_apart = int(sim.split("(")[-1].split(" ")[0])
        if (centuries_apart >= 4 and i < topSimsToExamine):
            topDistantSims.append(sim)
            topDistantAuthors[sim[11:]] = {}

        authors = " (".join(sim.split(" - ")[1].split(" (")[:-1])
        if authors == "Isocrates, Lysias" or authors == "Plato, Xenophon" or authors == "AratusSolensis, Callimachus" or authors == "Herodotus, Thucydides":
            comparisonOutput.append("Rank %d: %s" % (i+1, sim))

    fourCenturiesApartOutput = []
    fourCenturiesApartOutput.append("%d of the top %d are at least 4 centuries apart." % (len(topDistantSims), topSimsToExamine))
    fourCenturiesApartOutput.append("---")
    fourCenturiesApartOutput.extend(topDistantSims)

    utils.safeWrite("%swordUse/fourCenturiesApart.txt" % baseFolder, "\n".join(fourCenturiesApartOutput))

    # Comparison to English and Icelandic
    numGreek = len(authorSims)
    fracGreek = topSimsToExamine/numGreek
    numDistantGreek = len(topDistantSims)

    englishSims = utils.getContent("output/english/no_split/%s/jensen-shannon/metric/Authors/sims.txt" % (topStr), False).split("\n")
    numEnglish = len(englishSims)
    topSimsEnglish = int(np.ceil(numEnglish*fracGreek))
    fracEnglish = topSimsEnglish/numEnglish
    numDistantEnglish = 0
    num2English = 0
    for sim in englishSims[:topSimsEnglish]:
        centuries_apart = int(sim.split("(")[-1].split(" ")[0])
        if (centuries_apart >= 2):
            num2English += 1
        if (centuries_apart >= 4):
            numDistantEnglish += 1

    iceSims = utils.getContent("output/icelandic/no_split/%s/jensen-shannon/metric/Authors/sims.txt" % (topStr), False).split("\n")
    numIcelandic = len(iceSims)
    topSimsIcelandic = int(np.ceil(numIcelandic*fracGreek))
    fracIcelandic = topSimsIcelandic/numIcelandic
    numDistantIcelandic = 0
    for sim in iceSims[:topSimsIcelandic]:
        centuries_apart = int(sim.split("(")[-1].split(" ")[0])
        if (centuries_apart >= 4):
            numDistantIcelandic += 1

    comparisonOutput.append("\n=========\n")
    comparisonOutput.append("Top similar pairs")
    comparisonOutput.append("Greek:")
    comparisonOutput.append("  examining top %d of %d pairs (%.2f%%)" % (topSimsToExamine, numGreek, 100*fracGreek))
    comparisonOutput.append("  %d (%.2f%%) are at least 4 centuries apart" % (numDistantGreek, 100*numDistantGreek/topSimsToExamine))
    comparisonOutput.append("English:")
    comparisonOutput.append("  examining top %d of %d pairs (%.2f%%)" % (topSimsEnglish, numEnglish, 100*fracEnglish))
    comparisonOutput.append("  %d (%.2f%%) are at least 4 centuries apart" % (numDistantEnglish, 100*numDistantEnglish/topSimsEnglish))
    comparisonOutput.append("  %d (%.2f%%) are at least 2 centuries apart" % (num2English, 100*num2English/topSimsEnglish))
    comparisonOutput.append("Icelandic:")
    comparisonOutput.append("  examining top %d of %d pairs (%.2f%%)" % (topSimsIcelandic, numIcelandic, 100*fracIcelandic))
    comparisonOutput.append("  %d (%.2f%%) are at least 4 centuries apart" % (numDistantIcelandic, 100*numDistantIcelandic/topSimsIcelandic))

    utils.safeWrite("%swordUse/fourApartComparisonInfo.txt" % baseFolder, "\n".join(comparisonOutput))

    # Table
    for simMetric in simMetrics:
        dir, name = simMetric
        # "" or "+p" depending on which is better
        metricSims = utils.getContent("output/greek/no_split/%s/%s/metric/Authors/sims.txt" % (topStr, dir), False).split("\n")
        for i, sim in enumerate(metricSims):
            pairName = sim[11:]
            if pairName in topDistantAuthors:
                topDistantAuthors[pairName][dir] = i + 1

    # prepare values for coloring table cells
    maxVal = 0
    minVal = 1000000

    for authorPair in topDistantAuthors:
        for simDir, _ in simMetrics:
            val = topDistantAuthors[authorPair][simDir]
            minVal = min(minVal, val)
            maxVal = max(maxVal, val)

    pairRankOutput = []
    pairRankOutputSimple = []
    pairRankOutput.append("""
    \\begin{table}[!bt]
      \\centering
      \\def\\arraystretch{1}
      \\begin{tabular}{| l | c | c | c | c | c | c |}
    \\hline
    & \\multicolumn{5}{c|}{\\textbf{Rank according to}} \\\\
    & \\textbf{Jensen-} & \\textbf{Burrows'} & & & & \\\\
    \\textbf{Authors} & \\textbf{Shannon} & \\textbf{Delta} & \\textbf{Min-Max} & \\textbf{Manhattan} & \\textbf{Canberra} & \\textbf{Cosine} \\\\\\hline
    """)
    pairRankOutputSimple.append("%s,%s,%s,%s,%s,%s,%s" % ("Authors", "Jensen-Shannon", "Burrow's Delta", "Min-Max", "Manhattan", "Canberra", "Cosine"))
    authorConvert = {
        "ApolloniusRhodius": "Apollonius",
        "DionysiusOfHalicarnassus": "Dionysius",
        "EusebiusOfCaesarea": "Eusebius",
        "ClementOfAlexandria": "Clement",
        "BasilBishopOfCaesarea": "Basil",
        "Anonymous(Hymns_Aphrodite)": "Hymns Aphrodite",
        "Anonymous(Hymns_Apollo)": "Hymns Apollo",
        "Anonymous(Hymns_Demeter)": "Hymns Demeter",
        "Anonymous(Hymns_Hermes)": "Hymns Hermes",
        "Anonymous(Hymns_Rest)": "Hymns Rest",
    }
    for authorPair in topDistantAuthors:
        pair = "(".join(authorPair.split(" (")[:-1])
        pairSplit = pair.split(", ")
        author1 = pairSplit[0]
        author2 = pairSplit[1]

        if author1 in authorConvert:
            author1 = authorConvert[author1]
        if author2 in authorConvert:
            author2 = authorConvert[author2]

        pairName = author1 + ", " + author2
        cell = "%s &" % pairName
        cellSimple = "%s," % re.sub(", ", "/", pairName)
        firstVal = None
        for simDir, _ in simMetrics:
            val = topDistantAuthors[authorPair][simDir]

            cutoff = 100
            if (val < cutoff):
                r, g, b = colorConvert(minVal, cutoff, val, COLOR_ORANGE, COLOR_GRAY)
            else:
                r, g, b = colorConvert(cutoff, maxVal, val, COLOR_GRAY, COLOR_BLUE)
            cell += "\\cellcolor[rgb]{%.3f,%.3f,%.3f} " % (r, g, b)

            if (firstVal == None):
                firstVal = val
                cell += "%d & " % (val)
                cellSimple += "%d," % (val)
            else:
                cell += "%d (%+d) & " % (val, firstVal - val)
                rel = "(%d)" % (firstVal - val)
                cellSimple += "%d %s," % (val, rel)
        cell = cell[:-2]
        pairRankOutput.append("%s\\\\\\hline" % cell)
        pairRankOutputSimple.append(cellSimple)
    pairRankOutput.append("""
      \\end{tabular}
      \\caption{Rank of these pair's similarity by different metrics.}
      \\label{table:pair_rank}
    \\end{table}
    """)

    utils.safeWrite("%swordUse/pairRankTable.tex" % baseFolder, "\n".join(pairRankOutput))
    utils.safeWrite("%swordUse/pairRankTableSimple.csv" % baseFolder, "\n".join(pairRankOutputSimple))


# Get info on number of words used and create the table of top words
def getWordUseInfo(topStr, baseFolder):
    # total +p words
    tops = utils.getContent("output/greek/no_split/%s/wordInfo_%s.txt" % (topStr, topStr), False).split("\n")[1:]
    poetrys = utils.getContent("output/greek/no_split/top_p/wordInfo_top_p.txt", False).split("\n")[1:]
    # Top plus poetry
    totals = utils.getContent("output/greek/no_split/%s+p/wordInfo_%s+p.txt" % (topStr, topStr), False).split("\n")[1:]

    numWordsOutput = []
    numWordsOutput.append("Number of Top Words: %d" % len(tops))
    numWordsOutput.append("Number of Poetry Words: %d" % len(poetrys))
    numWordsOutput.append("Total Number of Words: %d" % len(totals))
    utils.safeWrite("%s/wordUse/totalWords.txt" % baseFolder, "\n".join(numWordsOutput))


    # Create Table of words
    topRanks = {}
    poetryRanks = {}

    for i, line in enumerate(tops):
        w = line.split(":")[0]
        topRanks[w] = i + 1

    for i, line in enumerate(poetrys):
        w = line.split(":")[0]
        poetryRanks[w] = i + 1

    rankInfo = []
    for line in totals:
        w = line.split(":")[0]
        topRank = ""
        if w in topRanks:
            topRank = "%d" % topRanks[w]
        poetryRank = ""
        if w in poetryRanks:
            poetryRank = "%d" % poetryRanks[w]

        rankInfo.append((w, topRank, poetryRank))


    rankTableOutput = []
    rankTableOutput.append("""
    \\begin{table}[!hbt]
      \\centering
      \\def\\arraystretch{1}
      \\begin{tabular}{| l | l | l ||| l | l | l ||| l | l | l ||| l | l | l |}
    \\hline

    \\textbf{Token} & \\textbf{A} & \\textbf{P} & \\textbf{Token} & \\textbf{A} & \\textbf{P} & \\textbf{Token} & \\textbf{A} & \\textbf{P} & \\textbf{Token} & \\textbf{A} & \\textbf{P}\\\\\\hline
    """)


    columnHeight = 43;
    for i in range(columnHeight):
        cells =  []
        for j in range(4):
            index = i + j*columnHeight
            cell = ""
            if (index < len(rankInfo)):
                cell = "%s & %s & %s" % rankInfo[index]

            cells.append(cell)
        rankTableOutput.append("%s \\\\\\hline" % (" & ".join(cells)))

    rankTableOutput.append("""
      \\end{tabular}
      \\caption{List of tokens used, along with their rank in the top 150 tokens found in all texts (\\textbf{A}) and rank in the top 100 tokens found in poetry texts (\\textbf{P}).}
      \\label{table:top_words}
    \\end{table}
    """)

    utils.safeWrite("%swordUse/topWordsTable.tex" % baseFolder, "\n".join(rankTableOutput))


# Get author and book counts for our languages for the data section
def getAuthorBookCounts(baseFolder):
    ab_counts_output = []
    splitter = "\n------\n"

    ab_counts_output.append("Greek:\n")
    ab_counts_output.append(utils.getContent("output/greek/numberOfAuthors_Books.txt", False))
    ab_counts_output.append(utils.getContent("output/greek/numberOfTypes_Tokens.txt", False))
    ab_counts_output.append(splitter)
    ab_counts_output.append("English:\n")
    ab_counts_output.append(utils.getContent("output/english/numberOfAuthors_Books.txt", False))
    ab_counts_output.append(utils.getContent("output/english/numberOfTypes_Tokens.txt", False))
    ab_counts_output.append(splitter)
    ab_counts_output.append("Icelandic:\n")
    ab_counts_output.append(utils.getContent("output/icelandic/numberOfAuthors_Books.txt", False))
    ab_counts_output.append(utils.getContent("output/icelandic/numberOfTypes_Tokens.txt", False))
    ab_counts_output.append(splitter)

    utils.safeWrite("%s/AuthorBookNumbers.txt" % baseFolder, "\n".join(ab_counts_output))

# Get word overlap info
def getOverlapInfo(baseFolder):
    output = []
    splitter = "\n------\n"

    output.append("Greek:\n")
    output.append(utils.getContent("output/greek/topWordOverlapOverTime.txt", False))
    output.append(splitter)
    output.append("English:\n")
    output.append(utils.getContent("output/english/topWordOverlapOverTime.txt", False))
    output.append(splitter)
    output.append("Icelandic:\n")
    output.append(utils.getContent("output/icelandic/topWordOverlapOverTime.txt", False))
    output.append(splitter)

    utils.safeWrite("%s/topWordOverlapOverTime.txt" % baseFolder, "\n".join(output))

# Get information about words that were skipped
def getSkippedWordInfo(baseFolder):
    output = []
    splitter = "\n------\n"

    output.append("Greek:\n")
    output.append(utils.getContent("output/greek/no_split/top250/chosenWordInfo.txt", False))
    output.append("\nPoetry:")
    output.append(utils.getContent("output/greek/no_split/top250+p/chosenWordInfoPoetry.txt", False))
    output.append(splitter)
    output.append("English:\n")
    output.append(utils.getContent("output/english/no_split/top250/chosenWordInfo.txt", False))
    output.append("\nPoetry:")
    output.append(utils.getContent("output/english/no_split/top250+p/chosenWordInfoPoetry.txt", False))
    output.append(splitter)
    output.append("Icelandic:\n")
    output.append(utils.getContent("output/icelandic/no_split/top250/chosenWordInfo.txt", False))
    output.append(splitter)

    utils.safeWrite("%s/skippedWords.txt" % baseFolder, "\n".join(output))

def getDataInfo(topStr, baseFolder):
    baseFolder = baseFolder + "/data"

    getAuthorBookCounts(baseFolder)

    getOverlapInfo(baseFolder)

    getSkippedWordInfo(baseFolder)

    subprocess.run("cp output/greek/no_split/%s/wordsTable.csv %s/wordsTableGreek_%s.csv" % (topStr, baseFolder, topStr), shell=True)
    subprocess.run("cp output/english/no_split/%s/wordsTable.csv %s/wordsTableEnglish_%s.csv" % (topStr, baseFolder, topStr), shell=True)
    subprocess.run("cp output/icelandic/no_split/%s/wordsTable.csv %s/wordsTableIcelandic_%s.csv" % (topStr, baseFolder, topStr), shell=True)

# Get information on the top authors
def makeTopAuthorTable(topStr, baseFolder):
    # Grab this from the best metric
    fname = "output/greek/no_split/%s/jensen-shannon/metric/Authors/sims.txt" % (topStr)
    allAuthorSims = utils.getContent(fname, False).split("\n")

    topAuthorPairs = []

    topAuthorPairs.append("""\\begin{table}[!bt]
  \\centering
  \\def\\arraystretch{1.2}
  \\begin{tabular}{| r | l | l | l | l |} \\hline
  & \\textbf{Author 1} & \\textbf{Author 2} & \\textbf{Score} & \\textbf{Notes}  \\\\\\hline
""")


    for i, pair in enumerate(allAuthorSims[:10]):
        splt1 = pair.split(" - ")
        sim = splt1[0]
        auths = splt1[1].split(" (")[0].split(", ")
        topAuthorPairs.append("  %.2d & %s & %s & %s & TODO \\\\\\hline" % (i+1, auths[0], auths[1], sim))

    topAuthorPairs.append("""
  \\end{tabular}
  \\caption{Top author pairs by similarity score according to Jensen-Shannon Similarity.}
  \\label{table:top_author_pairs}
\\end{table}
    """)

    utils.safeWrite("%smetric/topAuthorPairs.tex" % baseFolder, "\n".join(topAuthorPairs))



# create tables showing performance of light machine learning algorithms on predicting various categories
def makeMLTable(source, norm, filename):
    output = []

    output.append("""\\begin{table}[!bt]
  \\centering
  \\def\\arraystretch{1.2}
""")

    # No naive bayes if normed due to negative data
    if norm:
        output.append("  \\begin{tabular}{| r | l | l |} \\hline")
        output.append("  \\textbf{Prediction Task} & \\textbf{Majority Class} & \\textbf{KNN}  \\\\\\hline")
    else:
        output.append("  \\begin{tabular}{| r | l | l | l |} \\hline")
        output.append("  \\textbf{Prediction Task} & \\textbf{Majority Class} & \\textbf{KNN} & \\textbf{Naive Bayes}  \\\\\\hline")


    for t in ["Authors", "Books", "Books_2"]:
        cats = ["genre", "dialect", "timeframe"]
        if (t == "Books"):
            cats.append("author")
        if (t == "Books_2"):
            cats = ["work", "genre", "dialect", "timeframe", "author"]

        for cat in cats:
            fname = source + "res_%s_%s.txt" % (cat, t)
            lines = utils.getContent(fname, False).split("\n")
            maj_class = lines[1].split(" - ")[0].strip()
            knn = lines[2].split(" - ")[0].strip()
            naive_bayes = lines[3].split(" - ")[0].strip()

            t_name = t
            if t_name == "Books":
                t_name = "Segments"
            if t_name == "Books_2":
                t_name = "Segments*"
            if norm:
                output.append(" %s of %s & %s & %s \\\\\\hline" % (cat, t_name, maj_class, knn))
            else:
                output.append(" %s of %s & %s & %s & %s \\\\\\hline" % (cat, t_name, maj_class, knn, naive_bayes))

    output.append("""
  \\end{tabular}
  \\caption{Results of running simple machine learning on the frequency data.}
  \\label{table:ml+p}
\\end{table}
    """)

    utils.safeWrite(filename, "\n".join(output))

# =============================================================================
# =============================================================================

# Get information on genre
def getGenreInfo(topStr, baseFolder):
    # 2-dimensional tSNE projection
    subprocess.run("cp output/greek/no_split/%s/authors/tSNE/genre_tSNE_2D_no_labels.pdf %sgenre/tSNE_topWords_nolabels.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s/authors/tSNE/genre_tSNE_2D_labels.pdf %sgenre/tSNE_topWords_labels.pdf" % (topStr, baseFolder), shell=True)


# Get information on the metrics
def getMetricInfo(topStr, comparableTopStr, topNum, poetryNum, comparableNum, simMetrics, baseFolder):
    # Copy full eval files for jensen-shannon
    subprocess.run("cp output/greek/no_split/%s/jensen-shannon/metric/Books/comparisonInfo.txt %smetric/extraInfo/metricEvaluation_tops.txt" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s+p/jensen-shannon/metric/Books/comparisonInfo.txt %smetric/extraInfo/metricEvaluation_+p.txt" % (topStr, baseFolder), shell=True)

    # Grab median distance
    fname = "output/greek/no_split/%s/jensen-shannon/metric/Books/comparisonInfo.txt" % (topStr)
    metricEvalInfo = utils.getContent(fname, False).split("=========")[-2].split("\n")[2:-1]
    sameAuthorRanks = []
    for i, line in enumerate(metricEvalInfo):
        sameAuthorRank = line.split("with same author: ")[1].split(".")[0]
        sameAuthorRanks.append(int(sameAuthorRank))

    median = np.median(sameAuthorRanks)

    utils.safeWrite("%smetric/extraInfo/medianForDifferentAuthor.txt" % (baseFolder), "Median distance for closest author: %f" % median)

    # get info on the indica
    subprocess.run("cp output/greek/no_split/%s/jensen-shannon/metric/Books/sims/Arrian.Indica.1.txt %smetric/extraInfo/arrianIndica.txt" % (topStr, baseFolder), shell=True)


    # Info on book distance
    # Grab this from the best metric
    fname = "output/greek/no_split/%s/jensen-shannon/metric/Books/sims.txt" % (topStr)
    allBookSims = utils.getContent(fname, False).split("\n")

    utils.safeWrite("%smetric/lowestSimilarity.txt" % (baseFolder), "Lowest similarity between segments: %s" % allBookSims[-1])

    # Info on top similar authors
    makeTopAuthorTable(topStr, baseFolder)

    # ===============================


    makeMetricEvalTables("", topStr, comparableTopStr, topNum, poetryNum, comparableNum, simMetrics, baseFolder)

    # baseScoreMetric = "Burrows' Delta"
    # baseScoreIndex = 1
    # makeMetricEvalTables("_cmp_burrows", topStr, comparableTopStr, topNum, poetryNum, comparableNum, simMetrics, baseScoreMetric, baseScoreIndex)

# Get information comparing various texts across centuries
def getCenturyInfo(topStr, baseFolder):
    subprocess.run("cp output/greek/no_split/%s/jensen-shannon/metric/Authors/century_sims_overall_no_labels.pdf %scentury/centuriesGreek.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s/jensen-shannon/metric/Authors/century_sims_overall_labels.pdf %scentury/extraInfo/Greek_CenturyOverall_Label.pdf" % (topStr, baseFolder), shell=True)

    subprocess.run("cp output/greek/no_split/%s/jensen-shannon/metric/Authors/simRange.txt %scentury/extraInfo/Greek_SimRange.txt" % (topStr, baseFolder), shell=True)


    # -------------------------
    # Century similarity data
    subprocess.run("cp output/greek/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_no_labels.pdf %scentury/extraInfo/Greek_Century_No_Label.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_labels.pdf %scentury/extraInfo/Greek_Century_Label.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s+p/jensen-shannon/metric/Authors/century_sims_genre_no_labels.pdf %scentury/extraInfo/Greek+p_Century_No_Label.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s+p/jensen-shannon/metric/Authors/century_sims_genre_labels.pdf %scentury/extraInfo/Greek+p_Century_Label.pdf" % (topStr, baseFolder), shell=True)

    subprocess.run("cp output/greek/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_under_9_no_labels.pdf %scentury/extraInfo/Greek_Century_Cutoff_No_Label.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_under_9_labels.pdf %scentury/extraInfo/Greek_Century_Cutoff_Label.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s+p/jensen-shannon/metric/Authors/century_sims_genre_under_9_no_labels.pdf %scentury/extraInfo/Greek+p_Century_Cutoff_No_Label.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s+p/jensen-shannon/metric/Authors/century_sims_genre_under_9_labels.pdf %scentury/extraInfo/Greek+p_Century_Cutoff_Label.pdf" % (topStr, baseFolder), shell=True)



    subprocess.run("cp output/greek/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_under_9_no_labels.pdf %scentury/centuriesGreek2.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_under_9_no_labels_violin.pdf %scentury/centuriesGreekViolin.pdf" % (topStr, baseFolder), shell=True)


    subprocess.run("cp output/english/no_split/%s/jensen-shannon/metric/Authors/simRange.txt %scentury/extraInfo/English_SimRange.txt" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/english/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_no_labels.pdf %scentury/centuriesEnglish.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/english/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_no_labels_violin.pdf %scentury/centuriesEnglishViolin.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/english/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_labels.pdf %scentury/extraInfo/English_Century_Label.pdf" % (topStr, baseFolder), shell=True)

    subprocess.run("cp output/icelandic/no_split/%s/jensen-shannon/metric/Authors/simRange.txt %scentury/extraInfo/Icelandic_SimRange.txt" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/icelandic/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_no_labels.pdf %scentury/centuriesIcelandic.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/icelandic/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_no_labels_violin.pdf %scentury/centuriesIcelandicViolin.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/icelandic/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_labels.pdf %scentury/extraInfo/Icelandic_Century_Label.pdf" % (topStr, baseFolder), shell=True)


    # Get pvalue + other regression information for charts
    greekPval = utils.getContent("output/greek/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_under_9_pslope.txt" % (topStr), False)
    englishPval = utils.getContent("output/english/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_pslope.txt" % (topStr), False)
    icelandicPval = utils.getContent("output/icelandic/no_split/%s/jensen-shannon/metric/Authors/century_sims_genre_pslope.txt" % (topStr), False)

    pvalOutput = []
    pvalOutput.append("Greek:")
    pvalOutput.append(greekPval)
    pvalOutput.append("English:")
    pvalOutput.append(englishPval)
    pvalOutput.append("Icelandic:")
    pvalOutput.append(icelandicPval)

    utils.safeWrite("%scentury/century_pvals.txt" % baseFolder, "\n".join(pvalOutput))

# Get charts on word usage across authors and by specific author pairs
def getWordUsageInfo(topStr, baseFolder):
    # Word usage charts
    # Grab these from the best metric
    subprocess.run("cp output/greek/no_split/%s/wordImportance/Jensen-shannon-sorted/ignoreBestWords.pdf %swordUse/ignoreBestWords.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s/wordImportance/Jensen-shannon-sorted/all-diffs-cumul-cloud.pdf %swordUse/extraInfo/broadWordUsage.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s/wordImportance/Jensen-shannon-sorted/all-diffs-cumul.pdf %swordUse/extraInfo/all-diffs-cumul.pdf" % (topStr, baseFolder), shell=True)


    # Word organization charts
    subprocess.run("cp output/greek/no_split/%s/textsOnlyTopWords/9_group/tSNE/Word_Groupings_tSNE_2D_labels.pdf %swordUse/wordGroups.pdf" % (topStr, baseFolder), shell=True)

    subprocess.run("cp output/greek/no_split/%s/textsOnlyTopWords/9_group/images/dhct.pdf %swordUse/eightUp_9Group.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s/textsOnlyTopWords/pos_group/images/dhct.pdf %swordUse/eightUp_posGroup.pdf" % (topStr, baseFolder), shell=True)

# create each of the folders in a list if they do not exist yet
def createFolders(folders, baseFolder):
    for folder in folders:
        if not(os.path.exists(baseFolder + folder)):
            subprocess.run("mkdir " + baseFolder + folder, shell=True)

# =============================================================================
# =============================================================================
# =============================================================================

# List of similarity metrics
SIM_METRICS = [
    ("jensen-shannon", "Jensen-Shannon"),
    ("burrowsdelta", "Burrows' Delta"),
    ("minmax", "Min-Max"),
    ("cityblock", "Manhattan"),
    ("canberra", "Canberra"),
    ("cosine", "Cosine"),
]


# Gather full set of files
def gatherFilesFull(topStr, topNum, comparableTopStr, comparableNum, poetryNum):
    baseFolder = "output/full/"


    folders = [
        "",
        "data",
        "genre",
        "metric",
        "metric/extraInfo",
        "century",
        "century/extraInfo",
        "wordUse",
        "wordUse/extraInfo",
        "wordUse/grouping",
    ]
    createFolders(folders, baseFolder)

    # Get info for the data section
    getDataInfo(topStr, baseFolder)

    # Get info for approach section
    getWordUseInfo(topStr, baseFolder)

    # Get genre info
    getGenreInfo(topStr, baseFolder)
    # Gather 4up tsne charts for standard data and data normalized by genre
    # Grab this from the best metric
    subprocess.run("cp output/greek/no_split/%s/Authors/tSNE/info_no_labels_4Up.pdf %sgenre/groupings.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s/Books/tSNE/outliers4up.pdf %sgenre/bookOutliers.pdf" % (topStr, baseFolder), shell=True)

    # Get book tsne charts
    # Grab this from the best metric
    subprocess.run("cp output/greek/no_split/%s/Books/tSNE/tSNE_2D_no_labels.pdf %sgenre/books_tSNE_no_labels.pdf" % (topStr, baseFolder), shell=True)
    subprocess.run("cp output/greek/no_split/%s/Books/tSNE/tSNE_2D_labels.pdf %sgenre/books_tSNE_labels.pdf" % (topStr, baseFolder), shell=True)
    # To get a look at these, run python3 visualizeBooks


    # Get info for standard and normalized by poetry
    makeMLTable("output/greek/no_split/%s/dataPreds/" % (topStr), False, "%sgenre/ml_table.tex" % baseFolder)
    # makeMLTable("output/greek/no_split/%s+p/dataPreds/" % (topStr), False, "%sgenre/ml_table+p.tex" % baseFolder)

    # =========================

    # Get info for results section

    # -----------
    # Metric
    getMetricInfo(topStr, comparableTopStr, topNum, poetryNum, comparableNum, SIM_METRICS, baseFolder)

    makeMetricInternalTables("", topStr, SIM_METRICS, baseFolder)
    makeMetricInternalTables("", topStr + "+p", SIM_METRICS, baseFolder)

    # -----------
    # Century
    # Get information on century comparison
    getCenturyInfo(topStr, baseFolder)
    # Get pvalue + other regression information for charts that are + p
    greekPval = utils.getContent("output/greek/no_split/%s+p/jensen-shannon/metric/Authors/century_sims_genre_under_9_pslope.txt" % (topStr), False)
    englishPval = utils.getContent("output/english/no_split/%s+p/jensen-shannon/metric/Authors/century_sims_genre_pslope.txt" % (topStr), False)

    pvalOutput = []
    pvalOutput.append("Greek:")
    pvalOutput.append(greekPval)
    pvalOutput.append("English:")
    pvalOutput.append(englishPval)

    utils.safeWrite("%scentury/century_pvals+p.txt" % baseFolder, "\n".join(pvalOutput))

    # -------------------------
    # Grab this from the best metric
    subprocess.run("cp output/greek/no_split/%s/jensen-shannon/metric/Authors/sims.txt %swordUse/authorSims.txt" % (topStr, baseFolder), shell=True)

    fourCenturiesTables(topStr, SIM_METRICS, baseFolder)

    # get word usage charts and info
    getWordUsageInfo(topStr, baseFolder)

    # We didn't end up using grouping charts
    # groups = getWordGroupsRangeTest(topNum)
    # for g in groups:
    #     subprocess.run("cp output/greek/no_split/%s+p/textsOnlyTopWords/%d_group/images/groupingCompare.png %swordUse/grouping/%.2d.png" % (topStr, g, baseFolder, g), shell=True)

if __name__ == "__main__":
    #gatherFiles(mp.topStr, mp.topNum, mp.comparableTopStr, mp.comparableTopNum, mp.poetryNum)
    gatherFilesFull(mp.topStr, mp.topNum, mp.comparableTopStr, mp.comparableTopNum, mp.poetryNum)
