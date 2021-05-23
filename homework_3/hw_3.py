import re
import json
import pymorphy2
import string
import requests

with open("Severodvinsk.json", encoding="utf8") as f:
	corpus = json.load(f)

"""Почистим наш словарь:"""

texts = list(corpus.values())
keys = [x for x in range (0, len(corpus.keys()))] 
values = [] # здесь будут лежать тексты статей
for text in texts:
	text = re.sub(r'\n', ' ', text)
	text = re.sub(r'\([^()]*\)', '', text)
	text = re.sub(r'\([^{}]*\)', '', text)
	text = re.sub(r'==', '', text)
	text = re.sub(r'а́', 'а', text)
	text = re.sub(r'А́', 'А', text)
	text = re.sub(r'е́', 'е', text)
	text = re.sub(r'É', 'Е', text)
	text = re.sub(r'и́', 'и', text)
	text = re.sub(r'И́', 'И', text)
	text = re.sub(r'о́', 'о', text)
	text = re.sub(r'О́', 'О', text)
	text = re.sub(r'у́', 'у', text)
	text = re.sub(r'У́', 'У', text)
	text = re.sub(r'ы́', 'ы', text)
	text = re.sub(r'Ы́', 'Ы', text)
	text = re.sub(r'ю́', 'ю', text)
	text = re.sub(r'Ю́', 'Ю', text)
	text = re.sub(r'э́', 'э', text)
	text = re.sub(r'Э́', 'Э', text)
	text = re.sub(r'я́', 'я', text)
	text = re.sub(r'Я́', 'Я', text)
	values.append(text)

"""Создадим новый чистый корпус"""

new_corpus = dict(zip(keys, values))
new_corpus[0]
with open('new_corpus.json', 'w', encoding = 'utf-8') as f:
    json.dump(new_corpus, f, ensure_ascii=False)
import nltk
import string
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

dictionary = {}
for i in range (0, len(keys)):
    doc = values[i]
    dictionary[i] = doc

"""Токенизация"""

import pymorphy2
analyzer = pymorphy2.MorphAnalyzer()

punct = string.punctuation + "—" + "«" + "»"
tokens = []
for documents in dictionary.values():
    documents_token = documents.split()
    tokens.append([x for x in documents_token if x not in punct])

"""Убираем стоп-слова"""

from nltk.corpus import stopwords
stopwords_list = stopwords.words("russian")
wout_sw = []
for x in range (0, len(tokens)):
	wout_sw.append([word for word in tokens[x] if word not in stopwords_list])

"""С помощью расстояния Левинштейна найдем id документов, в которых лежит искомое слово"""

from nltk.metrics import edit_distance
def searching_word(input_word: str):
	id = []
	similar_words = ''
	for doc_num in range (0, len(keys)):
		if input_word in wout_sw[doc_num]:
			id.append(doc_num)
	if not id:
		for doc_num in range (0, len(keys)):
			for word in wout_sw[doc_num]:
				if edit_distance(input_word, word) <= 2:
					similar_words = word
					id.append(doc_num)
	print(input_word)
	print(f'Воможно, вы имели в виду это слово: {similar_words}')
	return set(id)

searching_word('Сегеродвинск')
searching_word('США')