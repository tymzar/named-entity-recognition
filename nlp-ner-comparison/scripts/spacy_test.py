#make a exemplaty spacy model

import spacy

nlp = spacy.load("pl_core_news_lg")

doc = nlp("Siema wszystkim, to jest jakiś tekst.")

print(doc.char_span(0, 5, label="ORG").vocab.lang)
        