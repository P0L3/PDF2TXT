"""
Script to assess total number of sentences, noun phrases per sentence, entities per sentence, verbs per sentence, total unique verbs
"""

import pandas as pd
from tqdm import tqdm

### NER
unnamed = pd.read_pickle("unnamed.pickle")

# Total number of sentences by NER
total_number_sentences_ner = len(set(unnamed['Sentence']))
total_entites = len(unnamed['Sentence'])
unique_sentences_ner = list(dict.fromkeys(unnamed['Sentence']))

del unnamed

### POS
## Assesing total number of sentences and number of papers
poss_full = pd.read_pickle("full_poss.pickle")
total_number_sentences_pos = len(poss_full)

# Initialize variables to store total number of nouns and verbs
total_nouns = 0
total_verbs = 0
total_nouns_ner = 0

# Iterate through each sentence and count nouns and verbs
for nouns, verbs, sentence in tqdm(zip(poss_full['Nouns'], poss_full['Verbs'], poss_full['Sentence'])):
    total_nouns += len(nouns)
    total_verbs += len(verbs)

    if sentence in unique_sentences_ner:
        total_nouns_ner += len(nouns)
        unique_sentences_ner.pop(0)

# Calculate the average number of nouns and verbs per sentence
average_nouns_per_sentence_pos = total_nouns / total_number_sentences_pos
average_verbs_per_sentence_pos = total_verbs / total_number_sentences_pos

del poss_full


### NER
# Calculate the average number
average_number_per_sentence_ner = total_entites / total_number_sentences_ner
average_number_per_allsentence_ner = total_entites / total_number_sentences_pos

### NER/POS
average_number_per_sentence_posner = total_nouns_ner / total_number_sentences_ner

# Print the results
print("Total number of sentences pos tagged:        ", total_number_sentences_pos)
print("Total number of sentences ner tagged:        ", total_number_sentences_ner)
print("Average number of nouns per sentence:        ", average_nouns_per_sentence_pos)
print("Average number of nouns per NER sentence:    ", average_number_per_sentence_posner)
print("Average number of entites per sentence:      ", average_number_per_sentence_ner)
print("Average number of entites per all sentences: ", average_number_per_allsentence_ner)
print("Average number of verbs per sentence:        ", average_verbs_per_sentence_pos)