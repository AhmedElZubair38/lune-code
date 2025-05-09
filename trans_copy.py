import pandas as pd
import re
import urllib.parse
import requests
from tqdm import tqdm
import time

G_API_DEFAULT = 'https://inputtools.google.com/request?text=%s&itc=%s-t-i0&num=1'

def clean_text(text: str) -> str:
    """Remove truly unwanted characters but keep hyphens, ampersands, numbers, etc."""
    # Remove punctuation that never belongs in a brand name
    text = re.sub(r"[.,;:\"'/\\\[\]{}<>|+=_`~^°§]", "", text)
    # Collapse multiple spaces
    return re.sub(r"\s+", " ", text).strip()

def transliterate_full_phrase(phrase: str, lang_code: str = 'ar') -> str:
    """Transliterate the entire phrase at once for best context."""
    cleaned = clean_text(phrase)
    encoded = urllib.parse.quote(cleaned)
    url = G_API_DEFAULT % (encoded, lang_code)
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        # data[1][0][1] is a list of suggestions for that phrase
        suggestions = data[1][0][1]
        if suggestions:
            return suggestions[0]
    except Exception:
        pass
    # fallback to cleaned input if something goes wrong
    return cleaned

# ————— Main Script —————

input_file  = 'TRANS/input_file.xlsx'
output_excel = 'TRANS/output_file_encoded.xlsx'

df = pd.read_excel(input_file)

df = pd.read_excel(input_file)

arabic_cols = []
start = time.time()
for name in tqdm(df['NAME'], desc="Transliterating Full Dataset"):
    arabic_cols.append(transliterate_full_phrase(name))
df['Arabic'] = arabic_cols
elapsed = time.time() - start

# write out
df.to_excel(output_excel, index=False)

print(f"\nDone in {elapsed:.1f}s — Excel: {output_excel}")