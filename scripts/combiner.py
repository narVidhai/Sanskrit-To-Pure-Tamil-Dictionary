import csv
import os
from os.path import join

def merge_dictionaries(list_of_dicts):
    unique_values, unique_pairs = set(), set()
    final_dict = {}
    for data in list_of_dicts:
        
        for key, values in data.items():
            if key not in final_dict:
                final_dict[key] = set()
            for value in values:
                value = value.strip()
                if not value:
                    continue
                final_dict[key].add(value)
                unique_pairs.add((key, value))
                unique_values.add(value)
    final_dict = {k:list(v) for k,v in final_dict.items()}
    return final_dict, unique_pairs, unique_values

def merge_sources(csv_files, outfile='combined.csv', output_folder='data/'):
    fields = ['INDIC', 'TAMIL']
    dictionaries = []
    for file in csv_files:
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f, fields)
            reader.__next__()
            dictionaries.append({row['INDIC']: row['TAMIL'].split(',') for row in reader})
    
    indic2tamil, indic2tamil_pairs, uniq_tamil = merge_dictionaries(dictionaries)
    print('Total Pairs:\t', len(indic2tamil_pairs))
    print('Indic Words:\t', len(indic2tamil))
    print('Tamil Words:\t', len(uniq_tamil))
    
    os.makedirs(output_folder, exist_ok=True)
    
    # Write CSV
    with open(join(output_folder, outfile), 'w', newline="\n", encoding='utf-8') as f:
        fields = ['INDIC', 'TAMIL']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for key in indic2tamil:
            writer.writerow({'INDIC': key, 'TAMIL': ",".join(indic2tamil[key])})
    
    return

if __name__ == '__main__':
    csv_files = [
        'data/viruba.csv',
        'data/tamilchol.csv'
    ]
    merge_sources(csv_files, 'combined_viruba+tamilchol.csv')
