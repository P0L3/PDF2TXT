""" Scipt to train a tokenizer """

from tokenizers import Tokenizer
from tokenizers.models import WordPiece

bert_tokenizer = Tokenizer(WordPiece(unk_token="[UNK]"))


from tokenizers import normalizers
from tokenizers.normalizers import Lowercase, NFD, StripAccents

bert_tokenizer.normalizer = normalizers.Sequence([NFD(), Lowercase(), StripAccents()])


from tokenizers.pre_tokenizers import Whitespace

bert_tokenizer.pre_tokenizer = Whitespace()


from tokenizers.processors import TemplateProcessing

bert_tokenizer.post_processor = TemplateProcessing(
    single="[CLS] $A [SEP]",
    pair="[CLS] $A [SEP] $B:1 [SEP]:1",
    special_tokens=[
        ("[CLS]", 1),
        ("[SEP]", 2),
    ],
)


from tokenizers.trainers import WordPieceTrainer

trainer = WordPieceTrainer(
    vocab_size=30522, special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"]
)
files = [f"RESULTS/SETS/full_10ksample/{split}.raw" for split in ["test", "train", "val"]]
bert_tokenizer.train(files, trainer)

bert_tokenizer.save("RESULTS/VOCABS/sciclimbert_v1.json")