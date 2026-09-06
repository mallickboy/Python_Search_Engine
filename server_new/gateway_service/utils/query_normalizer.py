import os
import re
import json
import spacy
import nltk
from nltk.corpus import wordnet
from symspellpy import SymSpell, Verbosity
from config import (
    FREQUENCY_DICTIONARY_PATH,
    USER_QUERY_FREQUENCY_PATH
)

nltk.download('wordnet')
nltk.download('omw-1.4')

class QueryRefinementPipeline:
    def __init__(self):
        # 1. Initialize SymSpell for spelling correction
        self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        # load a frequency dictionary:
        self.sym_spell.load_dictionary(FREQUENCY_DICTIONARY_PATH, 0, 1)
        
        # 2. Initialize spaCy
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy model...")
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def clean_and_normalize(self, text):
        """Step 1: Lowercase, remove special chars, and normalize whitespace."""
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def correct_spelling(self, text):
        """Step 2: Correct spelling using SymSpell."""
        # Note: SymSpell works best on individual tokens or 'lookup_compound'
        suggestions = self.sym_spell.lookup_compound(text, max_edit_distance=2)
        return suggestions[0].term if suggestions else text

    def extract_linguistic_hints(self, text):
        """Step 3: Extract Entities and Key POS tags using spaCy."""
        doc = self.nlp(text)
        entities = [ent.text for ent in doc.ents]
        # Keep nouns and adjectives as core keywords
        keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "ADJ"]]
        return {"tokens": [t.text for t in doc], "entities": entities, "keywords": keywords}

    def expand_query(self, keywords):
        """Step 4: Expand query using WordNet synonyms."""
        expanded_terms = set(keywords)
        for word in keywords:
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    # Add synonyms that are single words
                    if "_" not in lemma.name():
                        expanded_terms.add(lemma.name())
        return list(expanded_terms)
    
    def normalize(self, query):
        doc = self.nlp(query)   # NLP

        lemmas = []
        for t in doc:
            if t.is_stop:
                continue
            if t.is_punct:
                continue
            lemmas.append(t.lemma_)

        normalized = " ".join(lemmas)

        return normalized

    def process(self, query):
        """Execute the full pipeline."""
        # 1. Clean
        cleaned = self.clean_and_normalize(query)
        
        # 2. Correct
        corrected = self.correct_spelling(cleaned)
        
        # 3. Linguistic Analysis
        hints = self.extract_linguistic_hints(corrected)
        
        # 4. Expansion
        expanded = self.expand_query(hints['keywords'])

        # 4. Normalization
        normalized = self.normalize(corrected)
        
        return {
            "original": query,
            "refined": corrected,
            "entities": hints['entities'],
            "expanded_terms": expanded,
            "normalized": normalized,
        }

def save_query_frequency(text):
    file_path= USER_QUERY_FREQUENCY_PATH
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    text = text.strip().lower()

    # load existing data
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # update count
    if text in data:
        data[text]["count"] += 1
    else:
        data[text] = {
            "query": text,
            "count": 1
        }

    # save back
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# qr_pipeline = QueryRefinementPipeline()

if __name__=="__main__":
    pipeline = QueryRefinementPipeline()
    user_query = "Best smartfone for phottography in New York!!"
    user_query = "\t How to \t revarse \nAn arraayy?"
    result = pipeline.process(user_query)

    print(f"Original: {result['original']}")
    print(f"Cleaned/Corrected: {result['refined']}")
    print(f"Entities: {result['entities']}")
    print(f"Expanded Keywords: {result['expanded_terms']}")
    print(f"Normalized: {result['normalized']}")
