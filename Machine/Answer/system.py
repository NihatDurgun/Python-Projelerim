import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize

def make_tokenize(msg):
    tokens = word_tokenize(msg)
    return tokens

def words_cleaner(tokens):
    stop_words = set(stopwords.words('english'))
    clean_tokens = [w for w in tokens if not w in stop_words]
    return clean_tokens

def make_grubs(clean_words):
    grubs = nltk.pos_tag(clean_words)
    return grubs

def introduce_words(grubs):
    chunker = nltk.ne_chunk(grubs)
    return chunker

message = input();

tokens = make_tokenize(message)
print(tokens)

clean_words = words_cleaner(tokens)
print(clean_words)

grubs = make_grubs(clean_words)
print(grubs)

chunker = introduce_words(grubs)
print(chunker)

chunker =str(chunker)
parcala = chunker.split(" ")
i = 0
while i < len(parcala):
    i= i+1
    metin = parcala[i].split("/")
    print(metin)
