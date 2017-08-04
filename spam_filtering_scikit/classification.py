import pickle
from spam_filtering_scikit.train import count_words

def classification(mail_body):
    """

    :param mail_body:
    :return: label
    """

    # load it again into gnb_loaded
    with open('/Users/PycharmProjects/sicurezza/spam_filtering_scikit/my_dumped_classifier.pkl', 'rb') as fid:
        clf_loaded = pickle.load(fid)

    with open('/Users/PycharmProjects/sicurezza/spam_filtering_scikit/my_dumped_dictionary.pkl', 'rb') as fid:
        dict_loaded = pickle.load(fid)

    feature_vec = count_words(mail_body, dict_loaded)

    return clf_loaded.predict(feature_vec)

