from multi_rake import Rake;
import re


def get_keywords(pr):
    text_keywords = ''

    for item in pr:
        if type(item) is str:
            text_keywords += item + " "
        elif type(item) is list:
            for item2 in item:
                text_keywords += item2 + " "

    return text_keywords

def get_spam_keywords(spam_features, ham_features):
    #POPULATE THE SPAM AND HAM TEXT BLOBS
    text_spam = ''
    text_ham = ''

    for pr in spam_features:
        text_spam += get_keywords(pr)

    for pr in ham_features:
        text_ham += get_keywords(pr)

    text_spam =  re.sub('[^a-zA-Z0-9 \n\.]', ' ', text_spam)
    text_ham  = re.sub('[^a-zA-Z0-9 \n\.]', ' ', text_ham)
    # print(text_spam,"\n------------------------------------------\n",text_ham)
    #INITIALISE RAKE FOR POPULAR WORDS
    rake = Rake(max_words=2, min_freq=5)

    #EXTRACT POPULAR KEYWORDS FOR SPAM AND HAM
    keywords_spam = rake.apply(text_spam.lower())
    keywords_ham = rake.apply(text_ham.lower())

    # print(keywords_ham)
    # print(keywords_spam)

    spam = [spam_keyword[0] for spam_keyword in keywords_spam[:50]]
    ham = [ham_keyword[0] for ham_keyword in keywords_ham[:50]]

    #STORE TOP 30 SPAM AND HAM KEYWORDS
    # for i in range(0, 30):
    #     spam.append(keywords_spam[i][0])
    #     ham.append(keywords_ham[i][0])

    # GENERATE KEYWORDS PRESENT IN SPAM WHICH ARE NOT PRESENT IN HAM
    spam_final = []
    for word in spam:
        if word not in ham:
            spam_final.append(word)

    # print(spam_final)
    return spam_final
