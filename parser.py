#!/usr/bin/env python
# encoding: utf-8

import bibtexparser
import sys
import os
import re
import unidecode

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

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
	
	#print(bib_database.entries[0]['journal']).encode('ascii', 'ignore').decode('unicode_escape').strip()
	print("Total: " + str(len(bib_database.entries)))
	i = 1
	for entrie in bib_database.entries:
		r2b_write(entrie,bib)
		if (i != len(bib_database.entries)):
			bib.write(",\n")
		i = i + 1

	bib.write("\n")
	bib.write(']')
	bib.close()	
	
def r2b_write(entrie,bib):
	bib.write('\t{\n') # get surname of first author slicing to ','
	id = entrie['ID'].replace(" ", "").replace("'", "").replace("-","").replace("/","").replace("_","").replace(".","").encode('utf-8').strip()
	bib.write('\t\t"id": "' + id + '"')
	bib.write(',\n\t\t"source_id": "' + entrie['ID'].encode('utf-8').strip() + '"')
	if 'ENTRYTYPE' in entrie:
		bib.write(',\n\t\t"type": "' + entrie['ENTRYTYPE'] + '"')
	if 'title' in entrie:
		title = entrie['title'].replace("{\_}", "_").replace("{","").replace("}","").replace("'","").replace("\"","").replace("\\","").replace("{\$}{\$}{\\backslash}mathcal{\{}PI{\}}{\$}{\$}", "PI").replace("{\\'{c}}", "c").replace("{\"u}", "u").replace("{\\&}", "&").replace("T{\\\"u}", "Tu").encode('utf-8').strip()
		bib.write(',\n\t\t"title": "' + title.replace('"', '\\"') + '"')
	if 'author' in entrie:
		author = entrie['author'].replace("{","").replace("}","").replace("'","").replace("\"","").replace("\\","").replace("{\\o}","o").replace("{\\v{s}}","s").replace("{\\u{g}}", "g").replace("{\\v{Z}}", "Z").replace("{\\l}", "l").replace("{\\i}","i").replace("{\\\"O}","O").replace("\\\"u}","u").replace("{\.{I}}","I").replace("{\\v{z}}","").replace("{\\v{e}}","").replace("{\\`A}", "A").replace("{\\ae}", "e").replace("{\\v{E}}","E").replace("{\\~{n}}", "n").replace("{\\`o}","o").replace("{\\aa}","a").replace("{\\c{c}}","c").replace("{\\'{c}}", "c").replace("{\\'u}", "u").replace("{\\'i}", "i").replace("{\\`e}","e").replace("{\\'o}", "o").replace("{\\'a}", "a").replace("{\\v{n}}","n").replace("{\\v{c}}","c").replace("{\\v{n}}", "n").replace("{\~a}", "a").replace("{\\`a}", "a").replace("{\\'A}", "A").replace("{\\'e}", "e").encode('utf-8').strip()
		bib.write(',\n\t\t"author": "' + author.replace('\n', ', ') + '"')	
	if 'keywords' in entrie:
		bib.write(',\n\t\t"keywords": "' + entrie['keywords'].strip().encode('utf-8').strip().replace('\r\n',"").replace(" ,", ", ").replace("{","").replace("}","").replace("'","").replace("\"","").replace("\\","") + '"')
	if 'author_keywords' in entrie:
		bib.write(',\n\t\t"keywords": "' + entrie['author_keywords'].strip().encode('utf-8').strip().replace('\r\n',"").replace(" ,", ", ").replace("{","").replace("}","").replace("'","").replace("\"","").replace("\\","") + '"')		
	if 'publisher' in entrie:
		bib.write(',\n\t\t"publisher": "' + entrie['publisher'] + '"')
	if 'doi' in entrie:
		bib.write(',\n\t\t"doi": "' + entrie['doi'] + '"')
	if 'isbn' in entrie:
		bib.write(',\n\t\t"isbn": "' + entrie['isbn'] + '"')	
	if 'abstract' in entrie:
		abstract = entrie['abstract'].replace('\r\n',"").replace("{","").replace("\\","").replace("}","").replace("{\\{}", "").replace("{\\}}", "").replace("{\\$}","").replace("Prot{\\e}g{\\e}","Protege").encode('utf-8').strip()
		bib.write(',\n\t\t"abstract": "' + abstract.replace('\r', '').replace('\n', ' ').replace("{\$}{\$}{\\backslash}mathcal{\{}PI{\}}{\$}{\$}", "PI").replace("{\\&}", "&").replace('{\\e}',"e").replace("{\\ldots}", "").replace('"', '\\"').replace("`","'").replace("'","").replace("{\\thinspace}", "").replace("{\\%}", "%").replace("{\_}", "_") + '"')
	if 'pages' in entrie:
		bib.write(',\n\t\t"pages": "' + entrie['pages'].encode('utf-8') + '"')
	if 'year' in entrie:
		bib.write(',\n\t\t"year": "' + entrie['year'] + '"')
	if 'url_article' in entrie:
		bib.write(',\n\t\t"url_article": "' + entrie['url_article'] + '"')
	elif 'url_article' not in entrie and 'doi' not in entrie:
		bib.write(',\n\t\t"url_article": "https://doi.org/' + entrie['ID'].encode('utf-8').strip() + '"')
	elif 'url' in entrie:
		bib.write(',\n\t\t"url_article": "' + entrie['url'] + '"')
	elif 'url' not in entrie and 'doi' in entrie:
		bib.write(',\n\t\t"url_article": "https://doi.org/' + entrie['doi'].encode('utf-8').strip() + '"')			
	if 'journal' in entrie:
		bib.write(',\n\t\t"journal": "' + entrie['journal'].replace("{\\&}", "&").replace("{\\'e}","e").replace("{","").replace("}","").replace("'","").replace("\"","").replace("\\","").encode('utf-8').strip() + '"')
	if 'month' in entrie:
		bib.write(',\n\t\t"month": "' + entrie['month'] + '"')
	if 'volume' in entrie:
		bib.write(',\n\t\t"volume": "' + entrie['volume'] + '"')
	if 'day' in entrie:
		bib.write(',\n\t\t"day": "' + entrie['day'] + '"')
	if 'citations' in entrie:
		bib.write(',\n\t\t"citations": "' + entrie['citations'] + '"')
	if 'downloads' in entrie:
		bib.write(',\n\t\t"downloads": "' + entrie['downloads'] + '"')									
	bib.write("\n\t}")
	
if __name__ == '__main__':
	main()	
		
	