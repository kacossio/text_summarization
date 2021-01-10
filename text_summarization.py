import trafilatura
import requests
from bs4 import BeautifulSoup
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from flask import Flask

def summarize(text):
	inputs = tokenizer([text], max_length=1024, return_tensors='pt')
	# Generate Summary
	summary_ids = model.generate(inputs['input_ids'], num_beams=4, early_stopping=True)
	return([tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids])

def get_links(query):
	headers = {
	    'Access-Control-Allow-Origin': '*',
	    'Access-Control-Allow-Methods': 'GET',
	    'Access-Control-Allow-Headers': 'Content-Type',
	    'Access-Control-Max-Age': '3600',
	    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
	    }
	url = 'https://duckduckgo.com/html/?q='+query
	page = requests.get(url, headers=headers).text
	soup = BeautifulSoup(page, 'html.parser').find_all("a", class_="result__url", href=True)
	all_links = []
	for link in soup:
	    all_links.append(link['href'])
	return all_links

def tell_me_about(query):
	links = get_links(query)

	for link in links[:5]:
		downloaded = trafilatura.fetch_url(link)
		print(link)
		print(summarize(str(trafilatura.extract(downloaded))))
		print("\n====================================\n")


if __name__ == "__main__":
	start = time.time()

	model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
	tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
	print("model and tokenizer loaded")

	tell_me_about("instagram vulnerabilities")
	print(time.time()-start)