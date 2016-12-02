import numpy as np 
import os
from sklearn.linear_model import LogisticRegression
from scipy.sparse import csr_matrix
import nltk
from sklearn.metrics import classification_report

# Things to do now: figure out how to construct training matrix, hold out test files.
# Problems: how to decide size of matrix
# Solution: create features as before, create matrix after the fact. 

'''This creates a dictionary that maps article names to the population size'''





def add_feature(feature, num_feat):
	if feature not in feature_dict:
		feature_dict[feature] = str(num_feat)
		num_feat += 1

def get_article_pops():
	name_pop = {}
	with open(os.getcwd()+'/GoldStandardNew.txt') as infile:
		for line in infile:
			split_line = line.split()
			name = split_line[0]
			pop = split_line[1]
			name_pop[name] = pop

	return name_pop

# Goes through all the articles and creates the feature dictionary 
def get_feature_dict_and_target_vec(articles, name_pop):
	feature_dict = {}
	num_feat = 0
	population_locations = []
	total_word_index = 0
	all_words = []
	stop_words = set(nltk.corpus.stopwords.words('english'))
	for article in articles:
		with open(os.getcwd()+'/pdftotext/'+article) as infile:
			words = []
			population = name_pop[article]
			for line in infile:
				split_line = line.split()
				split_line = [word for word in split_line if not word in stop_words]
				words += split_line
				all_words += split_line

			i = 0
			for word in words:

				if i<1:
					feature1 = "prev_word=start_sym"
					feature2 = "word="+word
					feature3 = "next_word="+words[1]
				elif i<len(words)-1:
					feature1 = "prev_word="+words[i-1]
					feature2 = "word="+word
					feature3 = "next_word="+words[i+1]
				else:
					feature1 = "prev_word="+words[i-1]
					feature2 = "word="+word
					feature3 = "next_word=end_sym"
				if word == population:
					population_locations.append(total_word_index)

				features = [feature1,feature2,feature3]

				for feature in features:
					if feature not in feature_dict:
						feature_dict[feature] = num_feat
						num_feat += 1


				i += 1
				total_word_index += 1


	return feature_dict, population_locations, len(all_words)

def create_training_matrix(articles,feature_dict,n):
	training_matrix = np.zeros([n,len(feature_dict)])
	non_feat = len(feature_dict)
	stop_words = set(nltk.corpus.stopwords.words('english'))

	sample_num = 0
	for article in articles:
		with open(os.getcwd()+'/pdftotext/'+article) as infile:
			words = []
			for line in infile:
				split_line = line.split()
				split_line = [word for word in split_line if not word in stop_words]
				words += split_line

			i = 0
			for word in words:

				if i<1:
					feature1 = "prev_word=start_sym"
					feature2 = "word="+word
					feature3 = "next_word="+words[1]
				elif i<len(words)-1:
					feature1 = "prev_word="+words[i-1]
					feature2 = "word="+word
					feature3 = "next_word="+words[i+1]
				else:
					feature1 = "prev_word="+words[i-1]
					feature2 = "word="+word
					feature3 = "next_word=end_sym"

				features = [feature1,feature2,feature3]

				for feature in features:
					feat_num = feature_dict.get(feature,non_feat)
					if feat_num != non_feat:
						training_matrix[sample_num][feat_num] = 1

				i += 1
				sample_num += 1

	return training_matrix

def curtail_articles(articles, curtail):
	curtailed_articles = {} # Maps articles to a list of words (the article minus stop words)
	stop_words = set(nltk.corpus.stopwords.words('english'))
	all_articles = []
	for article in articles:
		with open(os.getcwd()+'/pdftotext/'+article) as infile:
			words = []
			for line in infile:
				# line = line.lower()
				split_line = line.split()
				if curtail:
					split_line = [word for word in split_line if not word in stop_words]
				words += split_line
				all_articles += split_line

		curtailed_articles[article] = words

	curtailed_articles['all_articles'] = all_articles

	return curtailed_articles

def create_target_vec(pop_locs,n):
	target_vec = np.zeros([n,])
	for location in pop_locs:
		target_vec[location] = 1
	return target_vec








train_articles = [file for file in os.listdir(os.getcwd()+'/Training_Articles')]
if '.DS_Store' in train_articles: train_articles.remove('.DS_Store')

test_articles = [file for file in os.listdir(os.getcwd()+'/Test_Articles')]
if '.DS_Store' in test_articles: test_articles.remove('.DS_Store')

name_pop = get_article_pops()
feature_dict, population_locations,n = get_feature_dict_and_target_vec(train_articles,name_pop)
X = create_training_matrix(train_articles,feature_dict,n)
Y = create_target_vec(population_locations,n)

test_feature_dict, test_population_locations,t_n = get_feature_dict_and_target_vec(test_articles,name_pop)
Xt = create_training_matrix(test_articles,feature_dict,t_n)
Yt = create_target_vec(test_population_locations,t_n)

print 'creating sparse matrices'
spX = csr_matrix(X)
spXt = csr_matrix(Xt)
model = LogisticRegression()
print 'fitting'
model.fit(spX,Y)
print 'done, scoring now'

y_pred = model.predict(spXt)
class_labels = ['not population', 'population']
print 'sum:', np.sum(y_hat)
print classification_report(Yt,y_pred,target_names=class_labels)










