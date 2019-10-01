import string
import re
import nltk
from nltk.tag import pos_tag
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')


PUNCTUATION = string.punctuation

RE_HASHTAG = r'#\S+' #hashtags
RE_AT = r'@\S+'      #@
RE_NB = " \d+"       #numbers
UNK = ""

def standardize_text(sentence):
    """
        Standardize sentence
    """
    
    sentence = sentence.replace("can't", "can not").replace("n't", " not")\
                       .replace("\\n"," ").replace("\n", " ")\
                       .replace("\'", " ").replace("-"," ")\
                       .replace("_"," ").replace('"', " ")
    
    for x in PUNCTUATION:
        sentence = sentence.replace(x , " ")
    
    sentence = re.sub(RE_HASHTAG, UNK, sentence)
    sentence = re.sub(RE_AT     , UNK, sentence)
    sentence = re.sub(RE_NB     , UNK, sentence)
    
    sentence = sentence.lower()
    
    return sentence

def get_wordnet_pos(treebank_tag):
    """Map ['NN', 'NNS', 'NNP', 'NNPS'] to NOUN....."""
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

tokenizer = RegexpTokenizer(r'\w+')
lemmatiser = WordNetLemmatizer()
stop = stopwords.words('english')
stop.remove('not')

def processing_sentence(sentence):
    """
        Apply NLP techniques to sentence
    """
    "Standardize"
    sentence = standardize_text(sentence)
    
    "Tokenization"
    sentence = tokenizer.tokenize(sentence)
    
    "Lemmatization"
    tokens_pos = pos_tag(sentence)
    tokens_pos = [(w,get_wordnet_pos(p)) for (w,p) in tokens_pos]
    sentence = [lemmatiser.lemmatize(w, pos=p) for (w,p) in tokens_pos if p != None]
    
    "Stopwords removing"
    sentence = [x for x in sentence if x not in stop]

    return ' '.join(sentence)


def processing_text(text):
    new_sentences = ''
    for sentence in text.split('.'):
        new_sentences += processing_sentence(sentence)
        new_sentences += ' '
    return new_sentences
