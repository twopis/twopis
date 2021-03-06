# Code for Like Two Pis in a Pod

This repository contains the code for the paper Like Two Pis in a Pod: Author Similarity in the Ancient Greek Corpus.

There are a few steps to get this running:

## Install Required Libraries

See `requirements.txt` for a list of packages.

## Download Corpora

See `rawTexts/README.md` for information on downloading the corpora needed for this code. Because the corpora are large or only available under certain licenses, they are not included in this directory and must be acquired separately.

Alternatively, if acquiring these corpora is not possible, download `textsCounts.zip` from the dataset on the Cultural Analytics website and unzip it into this folder. This contains the processed token counts for all the texts. If you are using `textsCounts.zip`, change `USE_TEXT_COUNTS` at the top of `runAll.py` to `True`.

## Preprocess Text Files

Run `python parseAll.py` in the `texts/` folder to convert from the raw corpora to the data used by the code.

## Run Full Pipeline

Run `python runAll.py` at the top level. To run all of the code. Results will be in the `output/` folder, with the items used in the paper in the `output/full/` folder.
