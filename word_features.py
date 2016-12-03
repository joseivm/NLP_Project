import nltk

class Featurizer:

    stop_words = set(nltk.corpus.stopwords.words('english'))

    def __init__(self, n, no_stop=False):
        self.n = n
        self.no_stop = no_stop


    def build_all_features(self, article_lines, target_word):
        features = []
        target = []

        sentences = []
        for line in article_lines:
            sentences += nltk.tokenize.sent_tokenize(line)

        for sentence in sentences:
            sentence_features, sentence_target = self.build_sentence_features(sentence, target_word)
            features += sentence_features
            target += sentence_target

        return features,target


    def build_sentence_features(self, sentence, target_word):
        features = []
        target = []
        
        sentence_words = sentence.split()
        pos_tags = dict(nltk.pos_tag(sentence_words))
        if self.no_stop:
            sentence_words = [word for word in sentence_words if not word in Featurizer.stop_words]

        for i in xrange(len(sentence_words)):
            word_feature = self.build_word_features(i, sentence_words, pos_tags)
            features.append(word_feature)
            if sentence_words[i] == target_word:
                target.append(1)
            else:
                target.append(0)

        return features, target


    def build_word_features(self, word_index,sentence,pos_tags):
        features = {}
        word = sentence[word_index]
        pos_tag = pos_tags[word]

        features['isDigit'] = word.isdigit()
        # features['word'] = word

        for i in range(-1*self.n, self.n+1):
            p = i + word_index
            w = ""
            pos = ""
            if p >= 0 and p < len(sentence):
                w = sentence[p]
                pos = pos_tags[w]
            features["w" + str(i)] = w
            features["pos" + str(i)] = pos
        return features

# print range(-3,3)
# print "w"+str(-2)
# f = Featurizer(3)
# sentence = "Testing this sentence to make sure it works"
# features, target = f.build_sentence_features(sentence, "make")
# print target
# for feature in features:
#     print feature