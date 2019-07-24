# Display the pre-calculated tSNE chart with clickable icons.

import numpy as np

import utils
import graphUtils
import genre

# Get precalculated data
saveDir = "output/greek/no_split/top145+p/Books/tSNE/"
precalcFilename = saveDir + "tSNE_2D_data.txt"

precalculated = utils.getContent(precalcFilename, True)
tsneX = np.array(precalculated["x"], dtype=np.float64)
preY = np.array(precalculated["y"], dtype=np.float64)
names = precalculated["names"]

print("Precalculateds loaded")

targets = []
targets.append({"name":"_", "target":preY, "labels":[]})

dataSet = graphUtils.Dataset(tsneX, targets)

graphUtils.clickable_tSNE_2D(dataSet, names, -1, saveDir, False)
