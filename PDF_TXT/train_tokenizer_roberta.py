""" Scipt to train a tokenizer for RoBERTa"""

from pathlib import Path

from tokenizers import ByteLevelBPETokenizer

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

# Save files to disk
tokenizer.save_model(".", "esperberto")

