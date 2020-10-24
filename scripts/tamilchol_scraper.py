import requests, json, csv
import os

JSON_URL = 'http://tamilchol.com/app/words'
data = requests.get(JSON_URL).json()

output_folder = 'data/'
os.makedirs(output_folder, exist_ok=True)

with open(output_folder + 'tamilchol_raw.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

indic2tamil, indic2tamil_pairs, uniq_tamil = {}, [], set()

for sample in data:
    indic, tamil_words = sample['name'].strip(), sample['tamil_word'].strip()
    tamil_words = [w.strip() for w in tamil_words.split(',')]
    if indic not in indic2tamil:
        indic2tamil[indic] = []
    indic2tamil[indic].extend(tamil_words)
    for tamil in tamil_words:
        uniq_tamil.add(tamil)
        indic2tamil_pairs.append((indic, tamil))

with open(os.path.join(output_folder, 'tamilchol.csv'), 'w', newline="\n", encoding='utf-8') as f:
    fields = ['INDIC', 'TAMIL']
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for key in indic2tamil:
        writer.writerow({'INDIC': key, 'TAMIL': ",".join(indic2tamil[key])})

# Print stats

print('Total Pairs:\t', len(indic2tamil_pairs))
print('Indic Words:\t', len(indic2tamil))
print('Tamil Words:\t', len(uniq_tamil))
