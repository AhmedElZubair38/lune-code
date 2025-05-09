# import pandas as pd
# import re
# import urllib.parse
# import requests
# from tqdm import tqdm
# import time

# SPECIAL_CHAR_MAP = {
#     '&': 'و'
# }

# G_API_DEFAULT = 'https://inputtools.google.com/request?text=%s&itc=%s-t-i0&num=1'

# def clean_text(text: str) -> str:
#     """Remove truly unwanted characters but keep hyphens, ampersands, numbers, etc."""
#     # Replace special characters first
#     for char, replacement in SPECIAL_CHAR_MAP.items():
#         text = text.replace(char, replacement)
#     # Remove punctuation that never belongs in a brand name
#     text = re.sub(r"[.,;:\"'/\\\[\]{}<>|+=_`~^°§]", "", text)
#     # Collapse multiple spaces
#     return re.sub(r"\s+", " ", text).strip()

# def transliterate_full_phrase(phrase: str, lang_code: str = 'ar') -> str:
#     """Transliterate the entire phrase at once for best context."""
#     cleaned = clean_text(phrase)
#     encoded = urllib.parse.quote(cleaned)
#     url = G_API_DEFAULT % (encoded, lang_code)
#     try:
#         resp = requests.get(url, timeout=5)
#         resp.raise_for_status()
#         data = resp.json()
#         # data[1][0][1] is a list of suggestions for that phrase
#         suggestions = data[1][0][1]
#         if suggestions:
#             return suggestions[0]
#     except Exception as e:
#         print(f"Error transliterating '{phrase}': {e}")
#     # fallback to cleaned input if something goes wrong
#     return cleaned

# # ————— Main Script —————

# input_file  = 'TRANS/input_file.xlsx'
# output_excel = 'TRANS/output_file_encoded.xlsx'

# df = pd.read_excel(input_file)

# arabic_cols = []
# start = time.time()
# for name in tqdm(df['NAME'], desc="Transliterating Full Dataset"):
#     arabic_cols.append(transliterate_full_phrase(name))
# df['Arabic'] = arabic_cols
# elapsed = time.time() - start

# # write out
# df.to_excel(output_excel, index=False)

# print(f"\nDone in {elapsed:.1f}s — Excel: {output_excel}")







import pandas as pd
import re
import urllib.parse
import requests
from tqdm import tqdm
import time

SPECIAL_CHAR_MAP = {
    '&': 'و'
}

KNOWN_PATTERNS = {
    r"\bAl\s+": "ال",
    r"\bEl\s+": "ال",
    r"Bakery\b": "مخبز",
    r"Suites\b": "أجنحة",
    r"Market\b": "سوق",
    r"Laundry\b": "مصبغة",
    r"Landry\b": "مصبغة",
    r"Group\b": "مجموعة",
    r"Funding\b": "تمويل",
    r"Services\b": "خدمات",
    r"Sports\b": "رياضة",
}

G_API_DEFAULT = 'https://inputtools.google.com/request?text=%s&itc=%s-t-i0&num=1'

def clean_text(text: str) -> str:
    """Remove truly unwanted characters but keep hyphens, ampersands, numbers, etc."""
    # Replace special characters first
    for char, replacement in SPECIAL_CHAR_MAP.items():
        text = text.replace(char, replacement)
    # Apply known pattern replacements for better Arabic context
    for pattern, replacement in KNOWN_PATTERNS.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    # Remove unnecessary punctuation
    text = re.sub(r"[.,;:\"'/\\()\[\]{}<>|+=_`~^°§]", "", text)
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
    except Exception as e:
        print(f"Error transliterating '{phrase}': {e}")
    # fallback to cleaned input if something goes wrong
    return cleaned

# ————— Main Script —————

input_file  = 'TRANS/input_file.xlsx'
output_excel = 'TRANS/output_file_encoded.xlsx'

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