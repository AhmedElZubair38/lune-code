# import arabic_reshaper
# from bidi.algorithm import get_display
# from google.transliteration import transliterate_text

# result = transliterate_text('AlAmer Pharmacy', lang_code='ar')
# reshaped_text = arabic_reshaper.reshape(result)
# bidi_text = get_display(reshaped_text)
# print(bidi_text)

import pandas as pd
import arabic_reshaper
from bidi.algorithm import get_display
from google.transliteration import transliterate_text

# Function to handle transliteration and reshaping
def transliterate_to_arabic(text):
    result = transliterate_text(text, lang_code='ar')  # Transliterate to Arabic
    reshaped_text = arabic_reshaper.reshape(result)  # Reshape the Arabic text
    bidi_text = get_display(reshaped_text)  # Correct the display order for RTL
    return bidi_text

# Load the Excel file (use your actual file path here)
input_file = 'input_file.xlsx'  # Replace with your file path
df = pd.read_excel(input_file)

# Assuming the column you want to transliterate is named 'English', adjust accordingly
df['Arabic'] = df['English'].apply(transliterate_to_arabic)

# Save the output to a new Excel file
output_file = 'output_file.xlsx'  # Replace with your desired output file path
df.to_excel(output_file, index=False)

print(f"Transliteration completed. Output saved to {output_file}")