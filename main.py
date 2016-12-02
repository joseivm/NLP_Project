from data import *

from sklearn.metrics import classification_report
from sklearn.svm import SVC

def SVM_test(X_train, Y_train, X_test,Y_test):
    svm = SVC(C=10**8)
    svm.fit(X_train,Y_train)

    y_pred = svm.predict(X_test)
    class_labels = ['not population', 'population']

    print classification_report(Y_test,y_pred,target_names=class_labels)

article_dir = 'all_articles_text/'
answer_key = 'GoldStandardSorted.txt'

data = Data(answer_key, article_dir, small=True)

print data.trainX.shape
print data.trainY.shape
print data.testX.shape
print data.testY.shape
SVM_test(data.trainX, data.trainY, data.testX, data.testY)