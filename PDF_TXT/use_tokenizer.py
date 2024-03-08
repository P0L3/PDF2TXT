""" Use trained tokenizer """

from tokenizers import Tokenizer
from transformers import PreTrainedTokenizerFast
from time import time

DIR = "./RESULTS/VOCABS/sciclimbert_v1.json"

bert_tokenizer = PreTrainedTokenizerFast(tokenizer_file = DIR)

print(bert_tokenizer.tokenize("This object can now be used with all the methods shared by the 🤗 Transformers tokenizers! Head to the tokenizer page for more information."))


import pandas as pd

df = pd.read_pickle("./RESULTS/ED4RE/full.pickle")

def tokenize_content(content):
    return len(bert_tokenizer.tokenize(content))

print("Starting tokenization ...")
start = time()
df["Content_Tokenized"] = df["Content"].apply(tokenize_content)

sum = df["Content_Tokenized"].sum()

print(f"Total tokens in {len(df)} dataframe: {sum} \t Total time: {time()-start}s")

df.to_pickle("./RESULTS/ED4RE/full_tokenized.pickle")
