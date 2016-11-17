import os
from sets import Set
import re
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

# change_names()
# get_all_PDFs()
# trim()

name_to_pop = article_pops()
converted_articles = []
with open('GoldStandardAll2.txt') as infile:
	for line in infile:
		split_line = line.split()
		article_name = split_line[0]
		converted_articles.append(article_name)

directory = os.getcwd()+'/pdftotext/'
new_directory = os.getcwd()+'/all_articles_text/'
more_articles = []
converted_articles = Set(converted_articles)
name_to_line = {}
with open('GoldStandard.txt') as infile:
	for line in infile:
		split_line = line.split()
		name = split_line[0]
		name_to_line[name] = line



with open('GoldStandardAll2.txt','a') as outfile:
	for name in name_to_pop.keys():
		if name not in converted_articles:
			os.system('cp '+directory+name+' '+new_directory+name)
			outfile.write(name_to_line[name])

	


'''
Possible problems: some articles can't be converted, the error might make the thing exit out of the for loop
and it will be hard to know what articles weren't converted. 

Solutions: make a list of all the articles, and after the first pass just target those, in that pass check for problem articles maybe? 



'''