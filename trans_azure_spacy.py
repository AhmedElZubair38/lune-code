import pandas as pd
import requests
from tqdm import tqdm
import time
import spacy
from ollama import Client

nlp = spacy.load("en_core_web_sm")

AZURE_KEY = "EZ3y444FXd1GNZF0OUNjGuDipN8YIeKp5xBXRgU67JsZLHdy3NJYJQQJ99BEACF24PCXJ3w3AAAbACOGicj1"
AZURE_REGION = "uaenorth"
TRANSLATE_URL = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=ar"
TRANSLITERATE_URL = "https://api.cognitive.microsofttranslator.com/transliterate?api-version=3.0&language=ar&fromScript=Latn&toScript=Arab"

def is_brand_name(text):
    doc = nlp(text)
    return any(ent.label_ == "ORG" for ent in doc.ents)

def azure_translate(text):
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_REGION,
        "Content-Type": "application/json"
    }
    body = [{"Text": text}]
    try:
        resp = requests.post(TRANSLATE_URL, headers=headers, json=body, timeout=10)
        resp.raise_for_status()
        return resp.json()[0]['translations'][0]['text']
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return text

def azure_transliterate(text):
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_REGION,
        "Content-Type": "application/json"
    }
    body = [{"Text": text}]
    try:
        resp = requests.post(TRANSLITERATE_URL, headers=headers, json=body, timeout=10)
        resp.raise_for_status()
        return resp.json()[0]['text']
    except Exception as e:
        print(f"Error transliterating '{text}': {e}")
        return text

input_file = 'TRANS/input_file.xlsx'
output_excel = 'TRANS/output_file_encoded.xlsx'

df = pd.read_excel(input_file)

arabic_cols = []
start = time.time()
for name in tqdm(df['NAME'], desc="Processing Full Dataset"):
    if is_brand_name(name):
        arabic_cols.append(azure_transliterate(name))
    else:
        arabic_cols.append(azure_translate(name))
df['Arabic'] = arabic_cols
elapsed = time.time() - start

df.to_excel(output_excel, index=False)
print(f"\nDone in {elapsed:.1f}s - Excel: {output_excel}")