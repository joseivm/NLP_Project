import os
from sets import Set
from collections import defaultdict
import re
import pandas as pd
cwd = ' '+os.getcwd()

def make_list():
	articles = []
	with open(os.getcwd()+'/GoldStandard.txt') as infile:
		for line in infile:
			split_line = line.split()
			article_name = split_line[0]
			article_name = article_name[:-4]
			article_name += '.pdf'
			articles.append(article_name)

	return Set(articles)

def article_pops():
	name_to_pop = {}
	with open(os.getcwd()+'/GoldStandard.txt') as infile:
		for line in infile:
			split_line = line.split()
			article_name = split_line[0]
			article_pop = split_line[1]
			name_to_pop[article_name] = article_pop

	return name_to_pop

def convert_to_txt(filepath):
	name_to_pop = article_pops()
	split_path = filepath.split('/')
	gene = split_path[2]
	cancer = split_path[3]
	with open('GoldStandardAll.txt','a') as outfile:
		cwd = ' '+os.getcwd()
		articles = [file for file in os.listdir(os.getcwd()+filepath) if ".pdf" in file]
		if '.DS_Store' in articles: articles.remove('.DS_Store')
		for article in articles:
			population = '-1'
			new_article_name = article[:-4]
			new_article_name += '.txt'
			if new_article_name in name_to_pop: 
				population = name_to_pop[new_article_name]
			outfile.write(new_article_name+' '+population+' '+cancer+' '+gene+'\n')
			# pdftotext os.getcwd+/PDFs/Melanoma/bla.pdf os.getcwd/pdftotext/bla.txt
			print new_article_name
			os.system('pdftotext'+cwd+filepath+'/'+article+cwd+'/all_articles_text/'+new_article_name)

def get_all_PDFs():
	num_pdfs = 0
	all_PDFs = []
	directory = os.getcwd()+'/LiteratureReview' 
	gene_folders = [file for file in os.listdir(directory) if os.path.isdir(directory+'/'+file) and file.isupper()]
	for gene_folder in gene_folders:
		cancer_folders = [file for file in os.listdir(directory+'/'+gene_folder) if os.path.isdir(directory+'/'+gene_folder+'/'+file)]
		for cancer_folder in cancer_folders:
			PDFs = [file for file in os.listdir(directory+'/'+gene_folder+'/'+cancer_folder)if '.pdf'in file]
			all_PDFs += PDFs
			# print cancer_folder, gene_folder
			# convert_to_txt('/LiteratureReview/'+gene_folder+'/'+cancer_folder)
	print len(Set(all_PDFs))

def change_names():
	directory = os.getcwd()+'/LiteratureReview'
	gene_folders = [file for file in os.listdir(directory) if os.path.isdir(directory+'/'+file) and file.isupper()]
	for gene_folder in gene_folders:
		cancer_folders = [file for file in os.listdir(directory+'/'+gene_folder) if os.path.isdir(directory+'/'+gene_folder+'/'+file)]
		for cancer_folder in cancer_folders:
			PDFs = [file for file in os.listdir(directory+'/'+gene_folder+'/'+cancer_folder)if '.pdf'in file]
			for PDF in PDFs:
				if ' ' in PDF:
					new_PDF = re.sub(' ','',PDF)
					print PDF
					# print new_PDF
					original_filepath = directory+'/'+gene_folder+'/'+cancer_folder+'/'+PDF
					# new_filepath = directory+'/'+gene_folder+'/'+cancer_folder+'/'+new_PDF
					original_filepath = re.sub(' ','\ ',original_filepath)
					print original_filepath
					# os.system('mv '+original_filepath+' '+new_filepath)

def trim():
	converted_articles = [file for file in os.listdir(os.getcwd()+'/all_articles_text') if '.txt' in file]
	converted_articles = Set(converted_articles)
	converted = {}
	for article in converted_articles:
		converted[article] = False
	with open('GoldStandardAll.txt') as infile:
		with open('GoldStandardAll2.txt','w') as outfile:
			i = 0
			for line in infile:
				split_line = line.split()
				article_name = split_line[0]
				if article_name in converted_articles and not converted[article_name]:
					i+=1
					converted[article_name] = True
					outfile.write(line)
	print i

articles = []
short_to_long = defaultdict(list)
long_to_short = {}
year_template = re.compile('\d{4}')
with open(os.getcwd()+'/GoldStandardSorted.txt') as infile:
	for line in infile:
		split_line = line.split()
		article_name = split_line[0]
		if 'etal' in article_name:
			split_name = article_name.split('etal')
			name = split_name[0]
			year = split_name[1][:4]
			

		else:
			
			match = re.search(year_template,article_name)
			if match:
				name = article_name[:match.start()]
				year = article_name[match.start():match.end()]
			else:
				print article_name
				name = article_name
				year = '0000'

		short_name = name+' '+year
		short_to_long[short_name].append(article_name)
		long_to_short[article_name] = short_name

		articles.append(article_name)

long_names = []
short_names = []
populations = []
genes = []
cancers = []
isWeird = []
with open(os.getcwd()+'/GoldStandardSorted.txt') as infile:
	for line in infile:
		split_line = line.split()
		if len(split_line) < 5: 
			split_line += ['-1','-1','-1']

		long_name = split_line[0]
		short_name = long_to_short[long_name]
		population = split_line[1]
		cancer = split_line[2]
		gene = split_line[3]
		if split_line[4] != '-1':
			weird = False
		else:
			weird = True


		long_names.append(long_name)
		short_names.append(short_name)
		populations.append(population)
		genes.append(gene)
		cancers.append(cancer)
		isWeird.append(weird)

BabyDataSet = zip(short_names,long_names,populations,genes,cancers,isWeird)
df = pd.DataFrame(data=BabyDataSet, columns=['Paper','FileName','TotalPopulation','Gene','CancerType','IsWerid'])


df.to_csv(os.getcwd()+'/annotations.csv',index=False,header=['Paper','FileName','TotalPopulation','Gene','CancerType','IsWerid'])



	


'''
====Tasks====
1. Find out how to use RobotReviewer

2. Annotate!

3. Convolutional Neural Network??


Possible problems: some articles can't be converted, the error might make the thing exit out of the for loop
and it will be hard to know what articles weren't converted. 

Solutions: make a list of all the articles, and after the first pass just target those, in that pass check for problem articles maybe? 



'''
