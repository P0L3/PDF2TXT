"""
SpringerNatrue tryout
"""
import sys
sys.path.append('../') # Adds parent directory to path
import re
import pandas as pd 
from parser_pdf import char_number2words_pages
import matplotlib.pyplot as plt
import seaborn as sns
from os import listdir
print(listdir())

file = "/PDF_TXT/RESULTS/ED4RE/full.pickle"
df = pd.read_pickle(file)
# for i, r in enumerate(df["References"][0]):
#     print(i, "   ", r)
    

lengths = df["Content"].apply(lambda x: len(str(x)))
# print(lengths)
# print(df.keys())

# print("Title:")
# print(30*"-")
# for title in df.Title:
#     print(title)
# print(30*"-")

# print("Content:")
# print(30*"-")
# for content, title, doi in zip(df.Content, df.Title, df.DOI):
#     # print(content)
#     if not char_number2words_pages(len(content)):
#         print(title)
#         print(doi)

#
average_content_length = df['Content'].apply(len).mean()

print(f'Average Content Length: {average_content_length}')

char_number2words_pages(average_content_length)

#
content_lengths = df['Content'].apply(len)

# Create a KDE plot
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.kdeplot(content_lengths, fill=True, color='skyblue')

# Limits
plt.xlim(0, 120000)  # Replace 0 and 1000 with your desired range for the x-axis
plt.ylim(0, 0.00007)   # Replace 0

# Set labels and title
plt.xlabel('Content Length')
plt.ylabel('Density')
plt.title('Kernel Density Estimation of Content Length')

# Show the plot
plt.show()
# exit()
## 

from flair.data import Sentence
from flair.nn import Classifier
from flair.splitter import SegtokSentenceSplitter
from tqdm import tqdm
import pickle
data_list = []
for title, text in tqdm(zip(df.Title, df.Content)):

    # initialize sentence splitter
    splitter = SegtokSentenceSplitter()

    # use splitter to split text into list of sentences
    sentences = splitter.split(text)

    print("Number of sentences to be tagged: ", len(sentences))
    # predict tags for sentences
    tagger = Classifier.load('ner')
    tagger.predict(sentences)
    
    for sentence in tqdm(sentences):
        s_text = sentence.text
        spans = sentence.get_spans("ner")
        # if len(spans) > 0:
        #     print(s_text)
        #     print(spans)
        # else:
        #     print("-")

        for i in range(len(spans)):
            spans_dict = spans[i].to_dict()
            
            row = {
                "Title": title,
                "Sentence": s_text,
                "Entity": spans_dict["text"],
                "Tag": spans_dict["labels"][0]["value"]
            }
            
            data_list.append(row)
      
df_ner = pd.DataFrame(data_list)
try:
    df_ner.to_pickle("{}_ner.pickle".format(file.split("_")[1].split(".")[0]))          
except:
    df_ner.to_pickle("unnamed.pickle")
    # with open("{}.pickle".format(title[0].replace(" ", "_")), "wb") as f:
    #     pickle.dump(sentences, f)
