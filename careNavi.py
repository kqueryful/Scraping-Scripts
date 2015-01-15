"""
careNavi.py
	Scrapes the website Nihongo de Care-Navi for 
	words, example sentences and example sentence audio
	
@author 	= kqueryful
@date 		= 1/11/2015
@version 	= 1.0
"""

from bs4 import BeautifulSoup
import requests
import urllib
import csv

file = open('output.txt', 'wb')
writer = csv.writer(file)

# Entries go from 1 to 8329
for num in range(1, 8330):
	pageUrl = "http://eng.nihongodecarenavi.jp/jpn/entry_%s.html" % num
	response = requests.get(pageUrl)
	soup = BeautifulSoup(response.text)
	
	# only save words with example sentences
	example = soup.find('div', id = "example")
	
	if example != None:
		print pageUrl
		
		exUrl = "http://eng.nihongodecarenavi.jp/voice/example/example_%s.mp3" % num
		mp3Name = "example_%s.mp3" % num
		urllib.urlretrieve(exUrl, "mp3/" + mp3Name )
		
		# WORD ===========================================
		basicInfo = soup.find('div', id = "basicInfo")
		
		wordKana = basicInfo.h1.contents[0].strip()
		wordKanji =  basicInfo.find('h2', class_ = "kanji").string
		wordEng = basicInfo.find('h2', class_ = "eng").string
	
		# EXAMPLE SENTENCE ===============================
		exKanji = ""
		exEng = ""
		
		# workaround for multi-line examples
		dialogue = example.find('p', class_ = "kanji")
		for line in dialogue.contents:
			if line.string != None:
				exKanji += line.string.strip()
			
		dialogue = example.find('p', class_ = "eng")
		for line in dialogue.contents:
			if line.string != None:
				exEng += line.string.strip()
	
		# Write to CSV file
		writer.writerow([wordKana.encode('UTF-8'), wordKanji.encode('UTF-8'), 
			wordEng.encode('UTF-8'), exKanji.encode('UTF-8'), exEng.encode('UTF-8'), mp3Name])