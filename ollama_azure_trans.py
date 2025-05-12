import pandas as pd
import requests
from tqdm import tqdm
from ollama import Client
import time

# =============== CONFIG ===============
AZURE_KEY = "EZ3y444FXd1GNZF0OUNjGuDipN8YIeKp5xBXRgU67JsZLHdy3NJYJQQJ99BEACF24PCXJ3w3AAAbACOGicj1"
AZURE_REGION = "uaenorth"
TRANSLITERATE_URL = "https://api.cognitive.microsofttranslator.com/transliterate?api-version=3.0&language=ar&fromScript=Latn&toScript=Arab"
TRANSLATE_URL = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=ar"
OLLAMA_MODEL = "phi3"
OLLAMA_ENDPOINT = "http://localhost:11434"

# Known brands (expand as needed)
BRAND_DB = {
    "Uber Eats": "أوبر إيتس",
    "McDonald's": "ماكدونالدز",
    "Starbucks": "ستاربكس",
    "Careem": "كريم",
    "Talabat": "طلبات",
}

# =============== AZURE FUNCTIONS ===============
def azure_transliterate(text):
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_REGION,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            TRANSLITERATE_URL,
            headers=headers,
            json=[{"Text": text}],
            timeout=8
        )
        response.raise_for_status()
        return response.json()[0]['text']
    except Exception as e:
        print(f"Azure transliterate error: {e}")
        return text

def azure_translate(text):
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_REGION,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            TRANSLATE_URL,
            headers=headers,
            json=[{"Text": text}],
            timeout=8
        )
        response.raise_for_status()
        return response.json()[0]['translations'][0]['text']
    except Exception as e:
        print(f"Azure translate error: {e}")
        return text

# =============== OLLAMA LLM REFINEMENT ===============
def llm_refine(english, arabic, mode="auto"):
    client = Client(host=OLLAMA_ENDPOINT)
    prompt = f"""You are an expert in Arabic brand and business naming.
Given the English: '{english}'
And the Arabic output: '{arabic}'
Mode: {mode}
If the Arabic is correct for the brand or meaning, return it as-is.
If you can improve the transliteration or translation for clarity, recognition, or accuracy, do so.
If it's a brand, keep it sounding like the original.
If it's a generic term, make sure it means the same thing.
Return ONLY the improved Arabic."""
    try:
        response = client.generate(
            model=OLLAMA_MODEL,
            prompt=prompt,
            options={'temperature': 0.2, 'num_predict': 50}
        )
        return response['response'].strip()
    except Exception as e:
        print(f"Ollama error: {e}")
        return arabic

# =============== HYBRID LOGIC ===============
def is_brand(text):
    # Simple check: exact match or startswith any known brand
    return any(text.lower().startswith(b.lower()) for b in BRAND_DB)

def hybrid_process(name):
    # 1. Check for exact brand
    if name in BRAND_DB:
        return BRAND_DB[name]
    # 2. If it's a brand, transliterate
    elif is_brand(name):
        arabic = azure_transliterate(name)
        return llm_refine(name, arabic, mode="brand")
    # 3. If it's generic, translate
    else:
        arabic = azure_translate(name)
        return llm_refine(name, arabic, mode="generic")

# =============== MAIN SCRIPT ===============
input_file = 'TRANS/input_file.xlsx'
output_file = 'TRANS/output_hybriddddddd.xlsx'

print("Loading data...")
df = pd.read_excel(input_file)

print("\nProcessing names (Hybrid Azure + Ollama):")
start_time = time.time()
results = []
for name in tqdm(df['NAME'], desc="Processing"):
    results.append(hybrid_process(name))

df['Arabic'] = results
df.to_excel(output_file, index=False)

total_time = time.time() - start_time
print(f"\n✅ Done in {total_time:.1f}s")
print(f"Output saved to: {output_file}")