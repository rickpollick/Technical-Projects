import csv
import json

# The path to your CSV file
csv_file_path = ''

# The path to the JSON output file
json_file_path = 'output.json'

# Read the CSV and add the data to a dictionary
data = []
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

# Write the data to a JSON file
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json_file.write(json.dumps(data, indent=4))

print(f'Data has been converted from {csv_file_path} to {json_file_path}')
