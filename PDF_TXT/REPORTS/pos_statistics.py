



from flair.models import SequenceTagger
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

pos_entity = ["CD", "DT", "FW", "HYPH", "JJ", "NN", "POS", "SYM"]
pos_verb = ["VB", "TO", "RB", "MD"]

df = pd.read_pickle("/PDF_TXT/RESULTS/ED4RE/full_10ksample.pickle")
# df = df.sample(1, random_state = 3005)
# df_sample.to_pickle("/PDF_TXT/RESULTS/ED4RE/full_10ksample.pickle")

data_list = []
for title, text in tqdm(zip(df.Title, df.Content)):

    # initialize sentence splitter
    splitter = SegtokSentenceSplitter()

    # use splitter to split text into list of sentences
    sentences = splitter.split(text)

    print("Number of sentences to be tagged: ", len(sentences))
    
    # Load the English POS tagger
    tagger = SequenceTagger.load('pos')
    tagger.predict(sentences)
    
    for sentence in sentences:
        s_text = sentence.text
        # Initialize variables
        entities = []
        current_entity = []
        verbs = []
        current_verb = []

        # Iterate through the words in the sentence with POS tags
        for word in sentence:
            if any(word.get_label('pos').value.startswith(pos) for pos in pos_entity):
                # If the word has a POS tag of noun or adjective, add it to the current entity
                current_entity.append(word.text)
            else:
                # If the word does not have a POS tag of noun or adjective, consider the current entity
                if current_entity:
                    entities.append(' '.join(current_entity))
                    current_entity = []

        # Consider the last entity if the text ends with a noun or adjective
        if current_entity:
            entities.append(' '.join(current_entity))
            
        ######
        
        # Iterate through the words in the sentence with POS tags
        for word in sentence:
            if any(word.get_label('pos').value.startswith(pos) for pos in pos_verb):
                # If the word has a POS tag of verb
                current_verb.append(word.text)
            else:
                # If the word does not have a POS tag of noun or adjective, consider the current entity
                if current_verb:
                    verbs.append(' '.join(current_verb))
                    current_verb = []

        # Consider the last entity if the text ends with a noun or adjective
        if current_verb:
            verbs.append(' '.join(current_verb))
            
        row = {
                "Title": title,
                "Sentence": s_text,
                "Nouns": entities,
                "Verbs": verbs
            }
            
        data_list.append(row)
  
df_pos = pd.DataFrame(data_list)
df_pos.to_pickle("full_poss.pickle") 