import numpy as np 
import os
from sklearn.feature_extraction import DictVectorizer
from nltk import tokenize
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.svm import SVC
import nltk

'''This function will create a training matrix to feed in to whatever classifier we pick. '''


def generate_feature_vector(word_index,sentence,n,word_pos):
	feature_vector = {}
	word = sentence[word_index]
	feature_vector['isDigit'] = word.isdigit()
	feature_vector['word'] = word

	if (word_index+1) <= (len(sentence)-1):
		feature_vector['next_word'] = sentence[word_index+1]
		feature_vector['next_word_pos'] = word_pos[sentence[word_index+1]]
	else:
		feature_vector['next_word'] = "end"
		feature_vector['next_word_pos'] = ''

	for j in range(1,n):
		feat_word = 'word-' + str(j)
		feat_pos = 'pos-'+str(j)
		feat_next = 'word+'+str(j)
		feat_next_pos = 'pos+'+ str(j)
		if word_index-j >= 0:
			feature_vector[feat_word] = sentence[word_index-j]
			feature_vector[feat_pos] = word_pos[sentence[word_index-j]]

		else:
			feature_vector[feat_word] = ''
			feature_vector[feat_pos] = ''

		# if (word_index+j) <= (len(sentence)-1):
		# 	feature_vector[feat_next] = sentence[word_index+j]
		# 	feature_vector[feat_next_pos] = word_pos[sentence[word_index+j]]

		# else:
		# 	feature_vector[feat_next] = ''
		# 	feature_vector[feat_next_pos] = ''




	return feature_vector

def create_matrix(articles, n,train=True,dict_vect=None,no_stop=False):
	stop_words = set(nltk.corpus.stopwords.words('english'))
	feature_vectors = []
	for article in articles:
		print article
		with open(os.getcwd()+article_paths+article) as infile:
			sentences = []
			for line in infile:
				line = line.decode('latin-1')
				line_sentences = tokenize.sent_tokenize(line)
				sentences += line_sentences

			for sentence in sentences:
				sentence_words = sentence.split()
				if no_stop:
					sentence_words = [word for word in sentence_words if not word in stop_words]
				pos_tags = nltk.pos_tag(sentence_words)
				word_to_pos = dict(pos_tags)


				for i in range(len(sentence_words)):
					feature_vector = generate_feature_vector(i,sentence_words,n,word_to_pos)
					feature_vectors.append(feature_vector)

	if train:
		v = DictVectorizer(sparse=True)
		X = v.fit_transform(feature_vectors)
	else:
		v = dict_vect
		X = v.transform(feature_vectors)

	return X,v

def create_target_vector(articles,name_pop,no_stop=False,zero_one=True):
	stop_words = set(nltk.corpus.stopwords.words('english'))
	target_vector = []
	for article in articles:
		sentences = []
		with open(os.getcwd()+article_paths+article) as infile:
			for line in infile:
				line = line.decode('latin-1')
				line_sentences = tokenize.sent_tokenize(line)
				sentences += line_sentences

			population = name_pop[article]
			for sentence in sentences:
				sentence_words = sentence.split()
				if no_stop:
					sentence_words = [word for word in sentence_words if not word in stop_words]
				pos_tags = nltk.pos_tag(sentence_words)

				for i in range(len(sentence_words)):
					if sentence_words[i].lower() == population:
						target_vector.append(1)
					else:
						target_vector.append(-1)

	target_vector = np.array(target_vector)
	if zero_one: 
		target_vector = (target_vector+1)/2

	return target_vector

def get_article_pops():
	name_pop = {}
	with open(os.getcwd()+answer_key) as infile:
		for line in infile:
			if not '*' in line and not '-1' in line: 
				split_line = line.split()
				name = split_line[0]
				pop = split_line[1]
				name_pop[name] = pop

	return name_pop

def LR_test(X_train, Y_train, X_test,Y_test):
	model = LogisticRegression(C=10**5)
	model.fit(X_train,Y_train)

	y_pred = model.predict(X_test)
	class_labels = ['not population', 'population']
	print 'sum:', np.sum(y_pred), 'real sum:', np.sum(Y_test)
	print classification_report(Y_test,y_pred,target_names=class_labels)

def SVM_test(X_train, Y_train, X_test,Y_test):
	svm = SVC(C=10**8)
	svm.fit(X_train,Y_train)

	y_pred = svm.predict(X_test)
	class_labels = ['not population', 'population']

	print classification_report(Y_test,y_pred,target_names=class_labels)

def create_SVM_XY(train_articles, test_articles, name_pop):
	X_train,dict_vect = create_matrix(train_articles,2,no_stop=True)
	Y_train = create_target_vector(train_articles,name_pop, zero_one=False, no_stop=True)

	X_test, dict_vect2 = create_matrix(test_articles,2,False,dict_vect,no_stop=True)
	Y_test = create_target_vector(test_articles,name_pop,zero_one=False, no_stop=True)
	return X_train,Y_train,X_test,Y_test

def create_LR_XY(train_articles, test_articles, name_pop):
	X_train,dict_vect = create_matrix(train_articles,2,no_stop=True)
	Y_train = create_target_vector(train_articles,name_pop,no_stop=True)
	X_test, dict_vect2 = create_matrix(test_articles,2,False,dict_vect,no_stop=True)
	Y_test = create_target_vector(test_articles,name_pop,no_stop=True)
	return X_train,Y_train,X_test,Y_test


if __name__ == "__main__":
	article_paths = '/all_articles_text/'
	answer_key = '/GoldStandardSorted.txt'

	name_pop = get_article_pops()
	all_articles = name_pop.keys()
	converted_articles = [file for file in os.listdir(os.getcwd()+article_paths) if '.txt' in file]
	all_articles = [file for file in all_articles if file in converted_articles]
	test_split = (len(all_articles)/10)*9
	train_articles = all_articles[:test_split]
	test_articles = all_articles[test_split:]
	print 'about to train'
	# X_train,Y_train,X_test,Y_test = create_LR_XY(train_articles, test_articles, name_pop)
	X_train,Y_train,X_test,Y_test = create_SVM_XY(train_articles, test_articles, name_pop)
	print 'about to test'
	SVM_test(X_train, Y_train, X_test, Y_test)
	# LR_test(X_train, Y_train)



