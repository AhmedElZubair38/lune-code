import pandas as pd

def convert_csv_to_utf8_with_bom(input_file, output_file):
            # Attempt to read the file with the specified encoding
            df = pd.read_csv(input_file, encoding='utf-8-sig')
            # Save it as UTF-8 with BOM
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"Successfully converted")


# Replace with your actual file paths
input_file = 'adib-feedbacks-data.csv'
output_file = 'adib-feedbacks-data-utf8.csv'

convert_csv_to_utf8_with_bom(input_file, output_file)
print("\nConversion completed.")