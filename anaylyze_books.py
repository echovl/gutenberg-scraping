import json
import re
import sys

import nltk
import requests
import spacy

BOOKS_FILENAME = "/tmp/gutenberg_6kbw9xcu.json"
BOOKS_URL = "https://res.cloudinary.com/dt7vlqkfj/raw/upload/v1695928056/i9kxprjqgfqxe2japbhh.json"


def print_inline(message):
    sys.stdout.write("\033[K" + message + "\r")


def get_books_content(path: str):
    books_text = ""
    books = []

    if "https://" in path:
        books = json.loads(requests.get(path).text)
    else:
        with open(path, "r") as file:
            books = json.load(file)

    for [idx, book] in enumerate(books):
        print_inline(f"Processing books ({idx+1}/{len(books)})")

        books_text += book["content"]

    print()

    return books_text


def preprocess_sentences(sentences: list[str]):
    for [idx, sentence] in enumerate(sentences):
        print_inline(f"Processing sentences ({idx+1}/{len(sentences)})")

        clean_sentence = sentence
        # Remove punctuations
        clean_sentence = re.sub(r"[^\w\s]|_", "", clean_sentence)
        # Remove escape characters
        clean_sentence = re.sub(r"\r\n", " ", clean_sentence)
        # Remove multiple spaces
        clean_sentence = re.sub(r"\s+", " ", clean_sentence)
        # Remove leading and trailing spaces
        sentences[idx] = clean_sentence.strip()

    print()


def tokenize_sentences(
    sentences: list[str], porter: nltk.stem.PorterStemmer, stopwords: list[str]
):
    nlp = spacy.load("en_core_web_md")
    tokens = []
    stemmed_tokens = []
    tagged_tokens = []
    tokenized_sentences = []

    for [idx, sentence] in enumerate(sentences):
        print_inline(f"Tokenizing sentences ({idx+1}/{len(sentences)})")

        sentence_tokens = []
        for token in nltk.word_tokenize(sentence):
            if token.lower() not in stopwords:
                tokens.append(token)
                stemmed_tokens.append(porter.stem(token))
                sentence_tokens.append(token)

        tokenized_sentence = " ".join(sentence_tokens)
        tokenized_sentences.append(tokenized_sentence)

        for token in nlp(tokenized_sentence):
            tagged_tokens.append((token.text, token.pos_))

    return (tokenized_sentences, tokens, stemmed_tokens, tagged_tokens)


if __name__ == "__main__":
    all_books_text = get_books_content(BOOKS_URL)

    nltk.download("punkt")
    nltk.download("stopwords")

    stopwords = nltk.corpus.stopwords.words("english")
    porter = nltk.stem.PorterStemmer()
    sentences = nltk.sent_tokenize(all_books_text)

    # Clean sentences
    preprocess_sentences(sentences)

    (tokenized_sentences, tokens, stemmed_tokens, tagged_tokens) = tokenize_sentences(
        sentences, porter, stopwords
    )

    # Sort tokens by frequency
    tokens = nltk.FreqDist(tokens)
    stemmed_tokens = nltk.FreqDist(stemmed_tokens)
    tagged_tokens = nltk.FreqDist(tagged_tokens)

    print("\n\nLemmatization:")
    print(f"\tVocabulary: {len(tokens)} words")
    print("\tCommon tokens", tokens.most_common(10))

    print("\nStemming:")
    print(f"\tVocabulary: {len(stemmed_tokens)} words")
    print("\tCommon tokens:", stemmed_tokens.most_common(10))

    print("\nTagging:")
    print(f"\tVocabulary: {len(tagged_tokens)} words")
    print("\tCommon tokens:", tagged_tokens.most_common(10))
