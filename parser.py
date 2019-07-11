#!/usr/bin/env python
# encoding: utf-8

import bibtexparser
import sys
import os
import re
import unidecode

def main(argv = sys.argv):

	argc = len(argv)
	if (argc == 1):
		print "Usage is ris2bib.py [FILE]"
	else:
		with open(argv[1]) as bibtex_file:
			bib_database = bibtexparser.load(bibtex_file)

	bib_filename = argv[1][:-4]+'.json' # strip and replace extension
	open(bib_filename,'w+') # strip and replace extension
	bib = open(bib_filename,'a') # strip and replace extension
	bib.write('[\n')
	
	for entrie in bib_database.entries:
		r2b_write(entrie,bib)

	bib.write(']')
	bib.close()	
	
def r2b_write(entrie,bib):
	bib.write('\t{\n') # get surname of first author slicing to ','
	id = entrie['ID'].replace(" ", "").replace("'", "").replace("-","").replace("/","").replace("_","").replace(".","").encode('utf-8').strip()
	bib.write('\t\t"id": "' + id + '",\n')
	if 'title' in entrie:
		title = entrie['title'].encode('utf-8').strip()
		bib.write('\t\t"title": "' + title.replace('"', '\\"') + '",\n')
	if 'author' in entrie:
		author = entrie['author'].encode('utf-8').strip()
		bib.write('\t\t"author": "' + author.replace('\n', ', ') + '",\n')		
	if 'publisher' in entrie:
		bib.write('\t\t"publisher": "' + entrie['publisher'] + '",\n')
	if 'doi' in entrie:
		bib.write('\t\t"doi": "' + entrie['doi'] + '",\n')	
	if 'isbn' in entrie:
		bib.write('\t\t"isbn": "' + entrie['isbn'] + '",\n')	
	if 'abstract' in entrie:
		abstract = entrie['abstract'].encode('utf-8').strip()
		bib.write('\t\t"abstract": "' + abstract.replace('"', '\\"').replace("`","'") + '",\n')
	if 'pages' in entrie:
		bib.write('\t\t"pages": "' + entrie['pages'] + '",\n')
	if 'year' in entrie:
		bib.write('\t\t"year": "' + entrie['year'] + '",\n')
	if 'url_article' in entrie:
		bib.write('\t\t"url_article": "' + entrie['url_article'] + '",\n')
	if 'journal' in entrie:
		bib.write('\t\t"journal": "' + entrie['journal'] + '",\n')
	if 'month' in entrie:
		bib.write('\t\t"month": "' + entrie['month'] + '",\n')
	if 'volume' in entrie:
		bib.write('\t\t"volume": "' + entrie['volume'] + '",\n')
	if 'day' in entrie:
		bib.write('\t\t"day": "' + entrie['day'] + '",\n')
	bib.write("\t},\n")
	
if __name__ == '__main__':
	main()	
		
	