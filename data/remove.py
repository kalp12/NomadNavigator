import json

# Load the JSON file
with open(r"C:\Users\kp121\Documents\vs code project\NomadNavigator\data\knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Dictionary to track unique destinations
unique_destinations = {}
filtered_data = []

# Iterate through the data and keep only the first occurrence of each destination
for entry in data:
    destination = entry.get("destination")
    if destination not in unique_destinations:
        unique_destinations[destination] = True  # Mark destination as seen
        filtered_data.append(entry)

# Save the cleaned data back to the file
with open(r"C:\Users\kp121\Documents\vs code project\NomadNavigator\data\knowledge_base_new.json", "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, indent=4)

print("Duplicate destinations removed successfully!")
