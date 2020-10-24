import requests, csv
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

def process_viruba(output_folder='data/'):
    
    indic2tamil, indic2tamil_pairs, uniq_tamil = viruba_crawl()
    print('Total Pairs:\t', len(indic2tamil_pairs))
    print('Indic Words:\t', len(indic2tamil))
    print('Tamil Words:\t', len(uniq_tamil))
    
    os.makedirs(output_folder, exist_ok=True)
    
    with open(join(output_folder, 'viruba.csv'), 'w', newline="\n", encoding='utf-8') as f:
        fields = ['INDIC', 'TAMIL']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for key in indic2tamil:
            writer.writerow({'INDIC': key, 'TAMIL': ",".join(indic2tamil[key])})
    
    return

if __name__ == '__main__':
    process_viruba()
