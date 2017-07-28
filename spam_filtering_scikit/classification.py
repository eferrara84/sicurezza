import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.svm import SVC, NuSVC, LinearSVC
from sklearn.metrics import confusion_matrix
import pickle



def classification(mail_body):
    """

    :param mail_body:
    :return: label
    """

    # load it again into gnb_loaded
    with open('./percistence/my_dumped_classifier.pkl', 'rb') as fid:
        clf_loaded = pickle.load(fid)

    with open('./percistence/my_dumped_dictionary.pkl', 'rb') as fid:
        dict_loaded = pickle.load(fid)


    print clf_loaded.predict(mail_body)


if __name__ == '__main__':


    classification("ciao")
