import os
import nltk
import numpy as np
from sklearn.feature_extraction import DictVectorizer

from word_features import *

class Data:

    def __init__(self, answer_key, article_dir, small=False):
        print "Preparing data..."

        self.article_dir = article_dir
        self.answer_key = answer_key

        # dic: article => pop
        self.article_pops = self.get_article_pops()

        self.articles = self.get_good_articles(self.article_pops.keys())
        if small:
            self.articles = self.articles[:30]

        training_size = int((0.9)*len(self.articles)) # num of articles to train with
        self.training_articles = self.articles[:training_size]
        self.test_articles = self.articles[training_size:]

        # context size 3
        n = 3
        self.featurizer = Featurizer(3)

        self.vectorizer = DictVectorizer(sparse=True)
        # Build training set
        self.trainX = None
        self.trainY = None
        self.build_training_set()

        self.testX = None
        self.testY = None
        self.build_test_set()

        print "Done."


    def build_training_set(self):
        train_features = []
        train_target = []
        for article in self.training_articles:
            target_word = self.article_pops[article]
            with open(os.path.join(self.article_dir,article)) as f:
                article_lines = [line.decode('latin-1') for line in f.readlines()]
                article_features,article_target = self.featurizer.build_all_features(article_lines, target_word)

                train_features += article_features
                train_target += article_target

        self.trainX = self.vectorizer.fit_transform(train_features)
        self.trainY = np.array(train_target)

    def build_test_set(self):
        test_features = []
        test_target = []
        for article in self.test_articles:
            target_word = self.article_pops[article]
            with open(os.path.join(self.article_dir,article)) as f:
                article_lines = [line.decode('latin-1') for line in f.readlines()]
                article_features,article_target = self.featurizer.build_all_features(article_lines, target_word)

                test_features += article_features
                test_target += article_target
        self.testX = self.vectorizer.transform(test_features)
        self.testY = np.array(test_target)



    def get_good_articles(self, articles):
        all_articles = os.listdir(self.article_dir)
        return [f for f in articles if f in all_articles]

    def get_article_pops(self):
        name_pop = {}
        with open(self.answer_key) as infile:
            for line in infile:
                if not '*' in line and not '-1' in line: 
                    split_line = line.split()
                    name = split_line[0]
                    pop = split_line[1]
                    name_pop[name] = pop
        return name_pop