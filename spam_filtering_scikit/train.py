import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.svm import SVC, NuSVC, LinearSVC
from sklearn.metrics import confusion_matrix
import pickle


def train():
    def make_Dictionary(train_dir):
        emails = [os.path.join(train_dir, f) for f in os.listdir(train_dir)]
        all_words = []
        for mail in emails:
            with open(mail) as m:
                for i, line in enumerate(m):
                    if i == 2:  # Body of email is only 3rd line of text file
                        words = line.split()
                        all_words += words

        dictionary = Counter(all_words)
        # Paste code for non-word removal here(code snippet is given below)
        return dictionary

    # Create a dictionary of words with its frequency

    train_dir = 'dataset/train-mails'
    test_dir = 'dataset/test-mails'

    dictionary = make_Dictionary(train_dir)

    list_to_remove = dictionary.keys()
    for item in list_to_remove:
        if item.isalpha() == False:
            del dictionary[item]
        elif len(item) == 1:
            del dictionary[item]
    dictionary = dictionary.most_common(3000)

    # print dictionary

    def extract_features(mail_dir):
        files = [os.path.join(mail_dir, fi) for fi in os.listdir(mail_dir)]
        features_matrix = np.zeros((len(files), 3000))
        docID = 0;
        for fil in files:
            with open(fil) as fi:
                for i, line in enumerate(fi):
                    if i == 2:
                        words = line.split()
                        for word in words:
                            wordID = 0
                            for i, d in enumerate(dictionary):
                                if d[0] == word:
                                    wordID = i
                                    features_matrix[
                                        docID, wordID] = words.count(word)
                                    # print "Reading: " + fil

                docID = docID + 1
        print features_matrix
        return features_matrix

    # Prepare feature vectors per training mail and its labels
    train_labels = np.zeros(702)
    train_labels[351:701] = 1
    train_matrix = extract_features(train_dir)

    # Training SVM and Naive bayes classifier

    model1 = MultinomialNB()
    model2 = LinearSVC()
    model1.fit(train_matrix, train_labels)
    model2.fit(train_matrix, train_labels)

    # Classifier Percistence
    # save the classifier
    with open('my_dumped_classifier.pkl', 'wb') as fid:
        pickle.dump(model2, fid)

    # save the dictionary
    with open('my_dumped_dictionary.pkl', 'wb') as fid:
        pickle.dump(dictionary, fid)

    # load it again into gnb_loaded
    with open('my_dumped_classifier.pkl', 'rb') as fid:
        gnb_loaded = pickle.load(fid)

    # Test the unseen mails for Spam
    # test_dir = 'test-mails'
    test_matrix = extract_features(test_dir)
    test_labels = np.zeros(260)
    test_labels[130:260] = 1
    result1 = model1.predict(test_matrix)
    result2 = model2.predict(test_matrix)
    print "confusion_matrix(test_labels,result1)", confusion_matrix(
        test_labels, result1)
    print "confusion_matrix(test_labels,result2)", confusion_matrix(
        test_labels, result2)

    return
