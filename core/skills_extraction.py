import pandas as pd
import spacy
from bs4 import BeautifulSoup
from spacy.matcher import PhraseMatcher

from .config import TAXONOMY_PATH

# --- Load NLP model ---
try:
    nlp = spacy.load("xx_ent_wiki_sm")
except:
    raise RuntimeError("Run: python -m spacy download xx_ent_wiki_sm")

# --- Load taxonomy ---
taxonomy_df = pd.read_csv(TAXONOMY_PATH)
skills_list = taxonomy_df["skill"].tolist()

# PhraseMatcher
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(text) for text in skills_list]
matcher.add("SKILLS", patterns)

def clean_html(text):
    return BeautifulSoup(text, "html.parser").get_text(separator=" ") if text else ""

def extract_skills(description):
    doc = nlp(description)
    matches = matcher(doc)
    found = {doc[start:end].text.title() for _, start, end in matches}
    return list(found)
