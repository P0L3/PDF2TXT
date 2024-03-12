



# from flair.models import SequenceTagger
from flair.data import Sentence
from flair.splitter import SegtokSentenceSplitter

import sys
sys.path.append('../') # Adds parent directory to path
import re
import pandas as pd 
from parser_pdf import char_number2words_pages
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

from pandas_parallel_apply import DataFrameParallel, SeriesParallel

# pos_entity = ["CD", "DT", "FW", "HYPH", "JJ", "NN", "POS", "SYM"]
# pos_verb = ["VB", "TO", "RB", "MD"]

df = pd.read_pickle("/PDF_TXT/RESULTS/ED4RE/full_title_content.pickle")
# df = df.sample(1, random_state = 3005)
# df_sample.to_pickle("/PDF_TXT/RESULTS/ED4RE/full_10ksample.pickle")

splitter = SegtokSentenceSplitter()
def number_of_sentences(content):
    if len(content) < 100:
        return 0
    else:
        try:
            sentences = splitter.split(content)
            return len(sentences)
        except:
            return -1
tqdm.pandas()
# df["Content"].progress_apply(number_of_sentences)
df["N_sentences"] = df["Content"].progress_apply(number_of_sentences)

df[["Title", "N_sentences"]].to_pickle("/PDF_TXT/RESULTS/ED4RE/full_sentence_number.pickle")