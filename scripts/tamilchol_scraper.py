import requests, json
import os

JSON_URL = 'http://tamilchol.com/app/words'
data = requests.get(JSON_URL).json()

output_folder = 'data/tamilchol.com/'
os.makedirs(output_folder, exist_ok=True)

with open(output_folder + 'raw.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

indic2tamil, indic2tamil_pairs, uniq_tamil = {}, [], set()

for sample in data:
    indic, tamil = sample['name'].strip(), sample['tamil_word'].strip()
    if indic not in indic2tamil:
        indic2tamil[indic] = []
    indic2tamil[indic].append(tamil)
    uniq_tamil.add(tamil)
    indic2tamil_pairs.append((indic, tamil))

print('Total Pairs:\t', len(indic2tamil_pairs))
print('Indic Words:\t', len(indic2tamil))
print('Tamil Words:\t', len(uniq_tamil))

with open(output_folder + 'indic2tamil.json', 'w', encoding='utf-8') as f:
    json.dump(indic2tamil, f, ensure_ascii=False, indent=4, sort_keys=True)

csv_string = 'INDIC,TAMIL\n'
csv_string += '\n'.join(','.join(pair) for pair in indic2tamil_pairs)
with open(output_folder + 'indic2tamil.csv', 'w', encoding='utf-8') as f:
    f.write(csv_string)

indic_words_txt = '\n'.join(list(indic2tamil.keys()))
tamil_words_txt = '\n'.join(uniq_tamil)

with open(output_folder + 'unique_tamil_words.txt', 'w', encoding='utf-8') as f:
    f.write(tamil_words_txt)

with open(output_folder + 'unique_indic_words.txt', 'w', encoding='utf-8') as f:
    f.write(indic_words_txt)
