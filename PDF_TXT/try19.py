from nltk.stem import WordNetLemmatizer
from nltk.corpus import words

"""
Failure fi to
4). fi Figure
no fi population
to fi 2010
study fi the
magni fi es
identi fi ed
heatfi fi related
in fl uencing
for fi the
modi fi ed
coef fi cient;
re fl ects
"""


lemmatizer = WordNetLemmatizer()

word = "influencing"
print(word)
word = lemmatizer.lemmatize(word)#, pos='v')
print(word)

if word in words.words():
    print("True")
else:
    print("False")