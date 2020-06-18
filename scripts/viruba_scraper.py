import requests, json
import sys, os
from os.path import join
from bs4 import BeautifulSoup
from tqdm import tqdm

PREFIX_URL = 'http://www.viruba.com/Dictionaries/Page.aspx?ID='
START_PAGE, END_PAGE = 3, 24

def viruba_crawl():
    indic2tamil, indic2tamil_pairs, uniq_tamil = {}, [], set()
    for page_id in tqdm(range(START_PAGE, END_PAGE+1)):
        dump_html = requests.get(PREFIX_URL + str(page_id)).text
        soup_dump = BeautifulSoup(dump_html, 'html.parser')
        rows = soup_dump.find_all('table', {'id': 'ContentPlaceHolder1_TabContainer1_TabPanel1_STD1938WordsByPageNumber'})[0].find_all('tr')

        for row in rows:
            indic, _, tamil = [column.text.strip() for column in row.find_all('td')]
            if indic not in indic2tamil:
                indic2tamil[indic] = []
            indic2tamil[indic].append(tamil)
            uniq_tamil.add(tamil)
            indic2tamil_pairs.append((indic, tamil))
    return indic2tamil, indic2tamil_pairs, uniq_tamil

def pretty_write_json(data, outfile, sort_keys=False):
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=sort_keys)
    return

def process_viruba(output_folder='data/viruba/'):
    
    indic2tamil, indic2tamil_pairs, uniq_tamil = viruba_crawl()
    print('Total Pairs:\t', len(indic2tamil_pairs))
    print('Indic Words:\t', len(indic2tamil))
    print('Tamil Words:\t', len(uniq_tamil))
    
    os.makedirs(output_folder, exist_ok=True)
    pretty_write_json(indic2tamil, join(output_folder, 'indic2tamil.json'), True)
    
    csv_string = 'INDIC,TAMIL\n'
    csv_string += '\n'.join(','.join(pair) for pair in indic2tamil_pairs)
    with open(join(output_folder, 'indic2tamil.csv'), 'w', encoding='utf-8') as f:
        f.write(csv_string)
    
    indic_words_txt = '\n'.join(list(indic2tamil.keys()))
    tamil_words_txt = '\n'.join(uniq_tamil)
    
    with open(join(output_folder, 'unique_tamil_words.txt'), 'w', encoding='utf-8') as f:
        f.write(tamil_words_txt)
    
    with open(join(output_folder, 'unique_indic_words.txt'), 'w', encoding='utf-8') as f:
        f.write(indic_words_txt)
    
    return

if __name__ == '__main__':
    process_viruba()
    