import requests
from bs4 import BeautifulSoup
import os
import csv

output_folder = 'data/tamilmandram.com/'
os.makedirs(output_folder, exist_ok=True)

URL = 'http://www.tamilmantram.com/vb/showthread.php/21268-%E0%AE%A4%E0%AF%82%E0%AE%AF-%E0%AE%A4%E0%AE%AE%E0%AE%BF%E0%AE%B4%E0%AF%8D%E0%AE%9A%E0%AF%8D%E0%AE%9A%E0%AF%8A%E0%AE%B1%E0%AF%8D%E0%AE%95%E0%AE%B3%E0%AF%8D'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html5lib')

lines = []
for i in soup.find_all("blockquote", {"class": "postcontent restore"}):
    lines.extend(i.get_text().splitlines())

#Some basic cleaning        
lines = [line.strip() for line in lines]
lines = [item.replace(',\\', ", ") for item in lines]
lines = [item for item in lines if item != "பிறமொழிச்சொல் - தமிழ்"]

filtered_lines = []
for line in lines:
    if line.count("-") > 0 and line.count("-") <= 2 and line[len(line)-1] != "-" and len(line.split()) <= 7:
        filtered_lines.append(line)

indic_to_tamil = dict(map(str.strip, line.split("-"))
                      for line in filtered_lines)
    
with open(output_folder + 'indic2tamil.csv', 'w', encoding='utf-8', newline='') as f:
    fields = ['INDIC','TAMIL']
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for key in indic_to_tamil:
        writer.writerow({'INDIC': key, 'TAMIL': indic_to_tamil[key]})
