import json
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
                final_dict[key].add(value)
                unique_pairs.add((key, value))
                unique_values.add(value)
    final_dict = {k:list(v) for k,v in final_dict.items()}
    return final_dict, unique_pairs, unique_values

def merge_sources(json_files, output_folder='data/combined/'):
    dictionaries = []
    for file in json_files:
        with open(file, encoding='utf-8') as f:
            dictionaries.append(json.load(f))
    
    indic2tamil, indic2tamil_pairs, uniq_tamil = merge_dictionaries(dictionaries)
    print('Total Pairs:\t', len(indic2tamil_pairs))
    print('Indic Words:\t', len(indic2tamil))
    print('Tamil Words:\t', len(uniq_tamil))
    
    os.makedirs(output_folder, exist_ok=True)
    
    # Write JSON
    with open(join(output_folder, 'indic2tamil.json'), 'w', encoding='utf-8') as f:
        json.dump(indic2tamil, f, ensure_ascii=False, indent=4, sort_keys=True)
    
    # Write CSV
    csv_string = 'INDIC,TAMIL\n'
    csv_string += '\n'.join(','.join(pair) for pair in indic2tamil_pairs)
    with open(join(output_folder, 'indic2tamil.csv'), 'w', encoding='utf-8') as f:
        f.write(csv_string)
    
    # Write word files
    indic_words_txt = '\n'.join(list(indic2tamil.keys()))
    tamil_words_txt = '\n'.join(uniq_tamil)
    
    with open(join(output_folder, 'unique_tamil_words.txt'), 'w', encoding='utf-8') as f:
        f.write(tamil_words_txt)
    
    with open(join(output_folder, 'unique_indic_words.txt'), 'w', encoding='utf-8') as f:
        f.write(indic_words_txt)
    
    return

if __name__ == '__main__':
    json_files = [
        'data/viruba.com/indic2tamil.json',
        'data/tamilchol.com/indic2tamil.json'
    ]
    merge_sources(json_files, 'data/combined_viruba+tamilchol/')