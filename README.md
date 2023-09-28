# gutenberg-scraping

## Installation

Install dependencies using `pip`

```sh
pip install -r requirements.txt
```

## Scraping

Run the scraper using the following command:

```sh
python scrap_books.py
```

This will save the scrapped books in a temporary file and will try to upload it to cloudinary:

Example output:

```sh
...
Books scrapped successfully!
Books temporary saved in /tmp/gutenberg_6kbw9xcu.json
Books saved in the url : https://res.cloudinary.com/dt7vlqkfj/raw/upload/v1695928056/i9kxprjqgfqxe2japbhh.json
```

## Language analysis

Run the analysis using the following command:

```sh
python scrap_books.py
```

Example output:

```sh
Processing books (5/6)
[nltk_data] Downloading package punkt to /home/echo/nltk_data...
[nltk_data]   Package punkt is already up-to-date!
[nltk_data] Downloading package stopwords to /home/echo/nltk_data...
[nltk_data]   Package stopwords is already up-to-date!
Processing sentences (119669/119669)
Tokenizing sentences (119669/119669)

Lemmatization:
        Vocabulary: 42839 words
        Common tokens [('thou', 5070), ('thy', 4078), ('shall', 3783), ('thee', 3542), ('would', 3158), ('good', 2720), ('love', 2532), ('one', 2456), ('Enter', 2363), ('man', 2329)]

Stemming:
        Vocabulary: 24465 words
        Common tokens: [('thou', 6152), ('thi', 4542), ('shall', 4312), ('come', 3936), ('lord', 3749), ('thee', 3563), ('would', 3471), ('good', 3441), ('love', 3404), ('king', 3357)]

Tagging:
        Vocabulary: 58471 words
        Common tokens: [(('thy', 'PRON'), 3959), (('shall', 'AUX'), 3781), (('would', 'AUX'), 3175), (('good', 'ADJ'), 2543), (('man', 'NOUN'), 2280), (('one', 'NUM'), 2207), (('lord', 'PROPN'), 2107), (('must', 'AUX'), 2038), (('may', 'AUX'), 1943), (('know', 'VERB'), 1936)]
```
