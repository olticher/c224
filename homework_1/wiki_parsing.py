import wikipediaapi as wikiapi
from urllib.request import urlopen
import requests
import json


wiki = wikiapi.Wikipedia("ru")
page = wiki.page("Северодвинск")
if page.exists():
	data = page.summary
data_size = len(data)

json_data = {
	
}

json_data["Северодвинск"]=data


links = page.links
ru_links = [i for i in sorted(list(links.keys())) if (ord(i[0]) >= 1040
            and ord(i[-1]) >= 1040)]



for j in range (0,200):
	page_new = wiki.page(ru_links[j])
	data_new = page_new.summary
	json_data[ru_links[j]] = data_new
	data_size+=len(data_new)
print('Количество слов:', data_size)
print('Медианное количество слов в каждом тексте:', data_size/201)

with open("Severodvinsk.json", "w", encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False)
