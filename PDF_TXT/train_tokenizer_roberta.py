""" Scipt to train a tokenizer for RoBERTa"""

from pathlib import Path

from tokenizers import ByteLevelBPETokenizer
from os import makedirs

paths = [str(x) for x in Path("./RESULTS/SETS/full").glob("**/*.raw")]

# Initialize a tokenizer
tokenizer = ByteLevelBPETokenizer()

# Customize training
tokenizer.train(files=paths, vocab_size=52_000, min_frequency=2, special_tokens=[
    "<s>",
    "<pad>",
    "</s>",
    "<unk>",
    "<mask>",
])

TOKENIZER_NAME = "cliretoberta_cased"
SAVE_PATH = "RESULTS/VOCABS/"

makedirs(SAVE_PATH+TOKENIZER_NAME, exist_ok=True)

tokenizer.save_model(SAVE_PATH+TOKENIZER_NAME+"/")
tokenizer.save(SAVE_PATH+TOKENIZER_NAME+"/")
tokenizer.save(SAVE_PATH+TOKENIZER_NAME+"/")
