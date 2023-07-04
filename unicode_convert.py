import json

def convert_to_unicode(text):
    unicode_text = text.encode('unicode-escape').decode()
    return unicode_text

# Prompt the user for the word and meaning in Urdu
word = input("Enter the word in Urdu: ")
meaning = input("Enter the meaning in Urdu: ")
source = input("Enter the source: ")

# Convert the word and meaning to Unicode
unicode_word = convert_to_unicode(word)
unicode_meaning = convert_to_unicode(meaning)
source = input("Enter the source: ")

# Load existing entries from the JSON file
with open("dictionary.json", "r", encoding="utf-8") as file:
    entries = json.load(file)

# Create a new entry object
entry = {"word": unicode_word, "meaning": unicode_meaning, "source": unicode_source}

# Append the new entry to the existing entries
entries.append(entry)

# Write the updated entries back to the JSON file
with open("dictionary.json", "w", encoding="utf-8") as file:
    json.dump(entries, file, ensure_ascii=False, indent=4)

print("Entry added successfully!")

