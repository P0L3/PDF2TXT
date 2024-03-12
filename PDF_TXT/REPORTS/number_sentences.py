import pandas as pd

df = pd.read_pickle("/home/andrija/RAD/PDF_TXT/ResearchPDF2TXT/PDF_TXT/RESULTS/ED4RE/10ksample_sentence_number.pickle")
print(df["N_sentences"].sum() + (df["N_sentences"]==0).sum())