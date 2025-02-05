import nltk
import string

nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))

def tokenize(text):
    """Tokenize un texte et enlève la ponctuation."""
    tokens = word_tokenize(text.lower())  # Mise en minuscule et tokenization
    tokens = [token for token in tokens if token not in string.punctuation]  # Supprimer la ponctuation
    return tokens

def remove_stopwords(tokens):
    """Supprime les stopwords de la liste des tokens."""
    return [token for token in tokens if token not in STOPWORDS]