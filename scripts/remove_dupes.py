import json

def remove_duplicates(entries):
    unique_entries = []
    seen = set()
    for entry in entries:
        # Check if the entry's "word" and "meaning" are not already seen
        key = (entry["word"], entry["meaning"])
        if key not in seen:
            unique_entries.append(entry)
            seen.add(key)
    return unique_entries

# Load existing entries from the JSON file
with open("dictionary.json", "r", encoding="utf-8") as file:
    entries = json.load(file)

# Remove duplicates from the entries
entries = remove_duplicates(entries)

# Write the updated entries back to the JSON file
with open("dictionary.json", "w", encoding="utf-8") as file:
    json.dump(entries, file, ensure_ascii=False, indent=4)

