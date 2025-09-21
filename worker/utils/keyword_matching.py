import ahocorasick
import os
from typing import List, Tuple

def load_keywords_from_file(path: str, tag: str) -> List[Tuple[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        return [(line.strip().lower(), tag) for line in f if line.strip() and not line.startswith("#")]

def build_tagged_automaton(keywords_with_tags: List[Tuple[str, str]]) -> ahocorasick.Automaton:
    A = ahocorasick.Automaton()
    for _, (keyword, tag) in enumerate(keywords_with_tags):
        A.add_word(keyword, (tag, keyword))
    A.make_automaton()
    return A

# Get path relative to this file (keyword_matching.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

allowed_keywords = load_keywords_from_file(os.path.join(STATIC_DIR, "allow.txt"), tag="allow")
blocked_keywords = load_keywords_from_file(os.path.join(STATIC_DIR, "block.txt"), tag="block")
all_keywords = allowed_keywords + blocked_keywords

KEYWORD_MATCHING = build_tagged_automaton(all_keywords)



# keywords = [
#     ("python", "allow"),
#     ("pygame", "allow"),
#     ("machine-learning", "allow"),
#     ("logout", "block"),
#     ("ads", "block"),
#     ("cart", "block"),
# ]