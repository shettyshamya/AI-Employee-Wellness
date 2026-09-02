import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


# Load NLP resources
STOP_WORDS = set(stopwords.words("english"))

# Preserve negation words because they can change emotional meaning
NEGATION_WORDS = {"not", "no", "never", "neither", "nor"}
STOP_WORDS = STOP_WORDS - NEGATION_WORDS
LEMMATIZER = WordNetLemmatizer()


def preprocess_text(text):
    """
    Preprocess employee feedback while preserving
    important emotional signals such as emojis.
    """

    # 1. Validate empty input
    if text is None or not text.strip():
        return None

    # 2. Remove repeated spaces
    text = re.sub(r"\s+", " ", text.strip())

    # 3. Convert text to lowercase
    text = text.lower()

    # 4. Tokenize
    tokens = word_tokenize(text)

    processed_tokens = []

    for token in tokens:

        # Preserve emojis and Unicode characters
        if any(ord(char) > 127 for char in token):
            processed_tokens.append(token)
            continue

        # Remove punctuation
        if re.fullmatch(r"[^\w\s]+", token):
            continue

        # Remove stop words
        if token in STOP_WORDS:
            continue

        # Keep words only
        if token.isalpha():

            # Lemmatization
            lemma = LEMMATIZER.lemmatize(token)

            processed_tokens.append(lemma)

    return " ".join(processed_tokens)