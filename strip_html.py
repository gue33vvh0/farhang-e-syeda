import os
import json
from bs4 import BeautifulSoup

input_directory = './format_words_input'
output_directory = './format_words_output'

def process_html_to_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator='', strip=True)

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(input_directory):
    if filename.endswith('.json'):
        input_filepath = os.path.join(input_directory, filename)
        output_filepath = os.path.join(output_directory, 'modified_' + filename)

        with open(input_filepath, 'r') as input_file:
            data = json.load(input_file)

            # Process the "word" section
            if 'word' in data:
                data['word'] = process_html_to_text(data['word'])

            # Write the modified content to the output file
            with open(output_filepath, 'w') as output_file:
                json.dump(data, output_file, indent=2, ensure_ascii=False)

print("Processing completed for all JSON files in the directory.")

