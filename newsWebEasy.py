'''
Download easy definitions from NHK News Web Easy
Created on Apr 3, 2015
@author: kqueryful
'''
import re
import csv
import json
import glob
import urllib
import os.path

if __name__ == '__main__':
    # download news-list
	url = "http://www3.nhk.or.jp/news/easy"
	urllib.urlretrieve("%s/news-list.json" % (url), "news/news-list.json")

	# parse news-list
	data = json.loads(open("news/news-list.json").readline()[3:])
	
	for day in data[0]:
		print (day)
		for index, val in enumerate(data[0][day]):
			id = data[0][day][index]["news_id"]
            
			# if new, download dictionary file
			fname = "news/%s.out.dic" % (id)
			if not os.path.isfile(fname):
				print ("downloading %s" % fname)
				urllib.urlretrieve("%s/%s/%s.out.dic" % (url, id, id), fname)
			
    # for each dictionary file
	dict = dict()
	for files in glob.glob("news/*.out.dic"):
		articleDefs = json.load(open(files))

		for id in articleDefs["reikai"]["entries"]:
			# header word
			header = " ".join(articleDefs["reikai"]["entries"][id][0]["hyouki"])

			# consolidate multiple definitions
			defs = ""
			for entry in articleDefs["reikai"]["entries"][id]:
				# convert ruby-formatted furigana to anki format
				strippedDef = re.sub("</*ruby>", "", entry["def"])
				strippedDef = re.sub("</rb>", "", strippedDef)
				strippedDef = re.sub("<rb>", " ", strippedDef)
				strippedDef = re.sub("<rt>", "[", strippedDef)
				strippedDef = re.sub("</rt>", "]", strippedDef)
				defs += strippedDef + "<br>"
			defs = defs[:-4]
			
			# if not seen, add word to dic
			if header not in dict:
				dict[header] = defs
			else:
				if len(defs) < dict[header]:
					dict[header] = defs

	# print out dic to output file
	file = open('output.txt', 'wb')
	writer = csv.writer(file)

	for header in dict:
		writer.writerow([header.encode("utf8"), dict[header].encode("utf8")])
		

	