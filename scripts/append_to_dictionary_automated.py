import json
import csv

def convert_to_unicode(text):
    unicode_text = text.encode('unicode-escape').decode()
    return unicode_text

# Open the CSV file and read its contents
with open("sheet.csv", "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header row if present
    next(reader, None)

    # Load existing entries from the JSON file
    with open("dictionary.json", "r", encoding="utf-8") as file:
        entries = json.load(file)

    # Iterate over the rows in the CSV file
    for row in reader:
        # Extract values from columns B, C, and D
        word = row[1]  # Column B
        meaning = row[2]  # Column C
        source = row[3]  # Column D

        # Convert the word and meaning to Unicode
        unicode_word = convert_to_unicode(word)
        unicode_meaning = convert_to_unicode(meaning)

        # Create a new entry object
        entry = {"word": unicode_word, "meaning": unicode_meaning, "source": source}

        # Append the new entry to the existing entries
        entries.append(entry)

# Write the updated entries back to the JSON file
with open("dictionary.json", "w", encoding="utf-8") as file:
    json.dump(entries, file, ensure_ascii=False, indent=4)
