import pandas as pd
import requests
from tqdm import tqdm
import time

#trabnslate only

# Azure Translator credentials and endpoint
AZURE_KEY = "EZ3y444FXd1GNZF0OUNjGuDipN8YIeKp5xBXRgU67JsZLHdy3NJYJQQJ99BEACF24PCXJ3w3AAAbACOGicj1"
AZURE_REGION = "uaenorth"
AZURE_ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=ar"


def azure_translate(text):
    """Translate English text to Arabic using Azure Translator API."""
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_REGION,
        "Content-Type": "application/json"
    }
    body = [{"Text": text}]
    try:
        response = requests.post(AZURE_ENDPOINT, headers=headers, json=body, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Extract the translated text
        return data[0]['translations'][0]['text']
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return text  # fallback: return original if error

# File paths
input_file = 'TRANS/input_file.xlsx'
output_excel = 'TRANS/azure-output_file_encoded.xlsx'

# Load data
df = pd.read_excel(input_file)

# Translate each name and store in new column
arabic_cols = []
start = time.time()
for name in tqdm(df['NAME'], desc="Translating Full Dataset"):
    arabic_cols.append(azure_translate(name))
df['Arabic'] = arabic_cols
elapsed = time.time() - start

# Save result
df.to_excel(output_excel, index=False)
print(f"\nDone in {elapsed:.1f}s - Excel: {output_excel}")