from docx import Document
import csv
from datetime import datetime

def count_word_occurrences_in_tables(doc_path, word_pairs):
    document = Document(doc_path)
    counts = {pair: 0 for pair in word_pairs}

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                cell_text = cell.text.lower()
                for pair in word_pairs:
                    if all(word.lower() in cell_text for word in pair):
                        counts[pair] += 1

    return counts

doc_path = ''
word_pairs = [('', ''), ('', '')]
counts = count_word_occurrences_in_tables(doc_path, word_pairs)

# Generate date stamp
date_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Write results to a CSV file with date stamp
csv_file = f'word_occurrences_{date_stamp}.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Sprint', 'Engineer', 'Occurrences', 'Timestamp'])
    for pair, count in counts.items():
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([pair[0], pair[1], count, timestamp])

for pair, count in counts.items():
    print(f"Occurrences of both '{pair[0]}' and '{pair[1]}' in the same cell: {count}")

print(f"Results exported to {csv_file}")
