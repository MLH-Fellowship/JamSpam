from __future__ import division
from utils import read_csv, fetch_data_from_github, import_local_dataset, fetch_from_remote
from spam_keywords import get_keywords, get_spam_keywords

import tensorflow as tf
from tensorflow import keras
import tensorflowjs as tfjs
import numpy as np
import tarfile
import os
import matplotlib.pyplot as plt
import time
import re

def print_array(ys):
    for xs in ys:
        print("[")
        print(", ".join(map(str, xs)))
        print("]")

def count_freq(pat, txt):
    M = len(pat)
    N = len(txt)
    res = 0

    # A loop to slide pat[] one by one
    for i in range(N - M + 1):

        # For current index i, check
        # for pattern match
        j = 0
        while j < M:
            if (txt[i + j] != pat[j]):
                break
            j += 1

        if (j == M):
            res += 1
            j = 0
    return res

def main():
  
    ###################
    ### IMPORT DATA ###
    ###################

    def import_data():
        spam_data, ham_data = import_local_dataset()
        # csv_row -> [url, title, body, diffs, commit_messages, files_changed, docs_changed, commits, changes]

        spam_text_corpus = [
            [row[1], row[2], row[4]]  # [title, body, commit_messages]
            for row in spam_data
        ]
        ham_text_corpus = [
            [row[1], row[2], row[4]]  # [title, body, commit_messages]
            for row in ham_data
        ]

        ## TO FETCH FROM REMOTE UNCOMMENT THE BLOCK BELOW
        #
        # spam_feature_array, ham_feature_array = fetch_from_remote(updateLocal=False)
        # spam_text_corpus = [[
        #     pr_feature["title"], pr_feature["body"], pr_feature["commit_messages"]
        # ] for pr_feature in spam_feature_array if type(pr_feature) is dict]
        # ham_text_corpus = [[
        #     pr_feature["title"], pr_feature["body"], pr_feature["commit_messages"]
        # ] for pr_feature in ham_feature_array if type(pr_feature) is dict]

        spam_keywords = get_spam_keywords(spam_text_corpus, ham_text_corpus)

        print(spam_keywords)

        spam_feature_array = []
        ham_feature_array = []

        spam_feature_array.extend([[
            # pr_feature["url"],
            int(pr_feature[5]), int(pr_feature[6]), int(pr_feature[7]), int(pr_feature[8])]  
            # [files_changed, docs_changed, commits, changes]
            for pr_feature in spam_data])
        ham_feature_array.extend([[
            # pr_feature["url"],
            int(pr_feature[5]), int(pr_feature[6]), int(pr_feature[7]), int(pr_feature[8])]  
            # [files_changed, docs_changed, commits, changes]
            for pr_feature in ham_data])

        for i in range(len(spam_text_corpus)):
            num_spam_keywords = 0
            text = re.sub('[^a-zA-Z0-9 \n\.]', '', get_keywords(spam_text_corpus[i]).lower())
            for keyword in spam_keywords:
                num_spam_keywords += count_freq(keyword, text)
            spam_feature_array[i].append(num_spam_keywords)

        for i in range(len(ham_text_corpus)):
            num_spam_keywords = 0
            text = re.sub('[^a-zA-Z0-9 \n\.]', '', get_keywords(ham_text_corpus[i]).lower())
            for keyword in spam_keywords:
                num_spam_keywords += count_freq(keyword, text)
            ham_feature_array[i].append(num_spam_keywords)

        TRAIN_SIZE = 40
        TEST_SIZE = 10

        features_array = spam_feature_array[:TRAIN_SIZE] + ham_feature_array[:TRAIN_SIZE]
        testing_array = spam_feature_array[-TEST_SIZE:] + ham_feature_array[-TEST_SIZE:]
        
        labels_array_train = []
        for spam_pr in spam_feature_array[:TRAIN_SIZE]:
            labels_array_train.append([1])

        for ham_pr in ham_feature_array[:TRAIN_SIZE]:
            labels_array_train.append([0])

        labels_array_test = []
        for spam_pr in spam_feature_array[-TEST_SIZE:]:
            labels_array_test.append([1])

        for ham_pr in ham_feature_array[-TEST_SIZE:]:
            labels_array_test.append([0])

        # print("loading training data")
        trainX = np.array(features_array)
        trainY = np.array(labels_array_train)
        # print(trainX)
        # print(trainY)

        # print("loading test data")
        testX = np.array(testing_array)
        testY = np.array(labels_array_test)
        return trainX,trainY,testX,testY

    trainX,trainY,testX,testY = import_data()
    feature_count = trainX.shape[1]
    label_count = trainY.shape[1]

    model = keras.Sequential([
        # keras.layers.Flatten(input_shape=(5,)),
        keras.layers.Dense(5, activation=tf.nn.relu, input_shape=(5,)),
        keras.layers.Dense(16, activation=tf.nn.relu),
        keras.layers.Dense(16, activation=tf.nn.relu),
        keras.layers.Dense(1, activation=tf.nn.sigmoid),
    ])

    model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

    model.fit(trainX, trainY, epochs=250, batch_size=1)

    test_loss, test_acc = model.evaluate(testX, testY)
    print('Test accuracy:', test_acc)

    print(model.predict(testX), testX)

    tfjs.converters.save_keras_model(model, f'model/{int(time.time())}')

if __name__ == "__main__":
    main()
