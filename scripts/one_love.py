import json
import os
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

# Specify the directory containing your JSON files
directory = './format_words_output'

# Specify the output file
output_file = 'combined_output.json'

# Create an empty list to store individual JSON entries
combined_data = []

# Initialize a variable to store the encoding of the first file
first_file_encoding = None

# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        
        # Detect the encoding of each file
        encoding = detect_encoding(file_path)
        
        # Store the encoding of the first file
        if first_file_encoding is None:
            first_file_encoding = encoding
        
        # Read the content of each file using the detected encoding
        with open(file_path, 'r', encoding=encoding) as file:
            file_content = json.load(file)
            combined_data.append(file_content)

# Write the combined data to the output file using the encoding of the first file
with open(output_file, 'w', encoding=first_file_encoding) as output:
    json.dump(combined_data, output, ensure_ascii=False, indent=2)

print(f"Combination completed. Result saved to {output_file}")

