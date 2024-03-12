import pandas as pd

df = pd.read_pickle("/PDF_TXT/RESULTS/ED4RE/full_sentence_number.pickle")
print(df["N_sentences"].mean())