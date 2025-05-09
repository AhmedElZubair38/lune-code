# import pandas as pd
# import arabic_reshaper
# from bidi.algorithm import get_display
# from google.transliteration import transliterate_text
# import re

# # Function to handle transliteration, reshaping, and trimming
# # Function to handle transliteration, reshaping, and trimming
# def transliterate_to_arabic(text):
#     # Trim and clean the input text
#     text = re.sub(r"[.,;:\"'/\\()\[\]{}<>|+=_`~^°§]", "", text)  # Remove unwanted characters
#     text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    
#     # Transliterate to Arabic
#     result = transliterate_text(text, lang_code='ar')
    
#     # Reshape for correct RTL display
#     reshaped_text = arabic_reshaper.reshape(result)
#     bidi_text = get_display(reshaped_text)
#     return bidi_text

# # Load the Excel file (use your actual file path here)
# input_file = 'TRANS/input_file.xlsx'  # Replace with your file path
# df = pd.read_excel(input_file)

# # Assuming the column you want to transliterate is named 'English', adjust accordingly
# df['Arabic'] = df['brand_labels'].apply(transliterate_to_arabic)

# # Save the output to a new Excel file
# output_file = 'TRANS/output_file.xlsx'  # Replace with your desired output file path
# df.to_excel(output_file, index=False)

# print(f"Transliteration completed. Output saved to {output_file}")







import pandas as pd
import re
from google.transliteration import transliterate_text
from tqdm import tqdm
import time

# Function to handle transliteration and trimming
def transliterate_to_arabic(text):
    # Trim and clean the input text
    text = re.sub(r"[.,;:\"'/\\()\[\]{}<>|+=_`~^°§]", "", text)  # Remove unwanted characters
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return transliterate_text(text, lang_code='ar')

# Load the Excel file (use your actual file path here)
input_file = 'TRANS/input_file.xlsx'  # Replace with your file path
df = pd.read_excel(input_file)

# Get the total number of rows for the progress bar
total_rows = len(df)

# Add a progress bar
start_time = time.time()
arabic_list = []
for label in tqdm(df['brand_labels'], desc="Transliterating", total=total_rows):
    arabic_list.append(transliterate_to_arabic(label))

# Add the Arabic column
df['Arabic'] = arabic_list

# Save the output to a new Excel file
output_file = 'TRANS/output_file_raw.xlsx'  # Replace with your desired output file path
df.to_excel(output_file, index=False, encoding='utf-8-sig')

end_time = time.time()
elapsed_time = end_time - start_time

print(f"\nTransliteration completed in {elapsed_time:.2f} seconds. Output saved to {output_file}")