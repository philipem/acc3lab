#!usr/bin/env python3

from __future__ import absolute_import, unicode_literals
from flask import Flask, jsonify, send_file
from celery import Celery
from create_celery import make_celery
from plot_bar import plot_bars
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import io

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL="pyamqp://localhost//",
    CELERY_RESULT_BACKEND="redis://"
)
celery = make_celery(flask_app)


# Flask methods
@flask_app.route('/', methods=['GET'] )
def get_count():
    cwd = os.getcwd()
    data_path = cwd + '/data/'
    result = get_noun_count.delay(data_path)
    res =result.get()
    return jsonify(res)

@flask_app.route('/plot', methods=['GET'])
def get_count_plot():
    cwd = os.getcwd()
    data_path = cwd + '/data/'
    result = get_noun_plot.delay(data_path)
    res =result.get()

# Celery tasks 
@celery.task(name='create_celery.get_noun_count')
def get_noun_count(file_path):
    df, rows = read_to_df(file_path)  # although rows is not used here, it should be passed as the second argument to plot_bars()
    tot_count, dict_of_rowcount = count_pronouns(df, pronouns, row_dict)
    print('Number of pronouns: ', tot_count)
    return tot_count

# helper functions
pronouns = {'han': 0, 'hon': 0, 'den': 0, 'det': 0, 'denna': 0, 'denne': 0, 'hen': 0}
row_dict = {}
cwd = os.getcwd()

data_path = cwd + '/data/'

def read_to_df(directory):
    my_df = pd.DataFrame()

    for file in os.listdir(directory):

        df = pd.read_json(directory + file, lines=True)

        # select useful columns
        df_stripped = df[['text', 'retweet_count']]
        df_stripped = df_stripped[df_stripped['retweet_count'] == 0]
        print(df_stripped)
        my_df = my_df.append(df_stripped)
        print(my_df)
    rows = len(my_df.index)
    return my_df, rows


def count_pronouns(df, words_total, words_row):

    for index, row in df.iterrows():
        row_key = 'tweet%d' % index
        row_val = {'han': 0, 'hon': 0, 'den': 0, 'det': 0, 'denna': 0, 'denne': 0, 'hen': 0}

        for char in row['text']:
            # print(char.isalnum())
            if char.isalnum() is False and char != ' ':
                # print('first ', type(char))
                row['text'] = row['text'].replace(char, '')
                # print(row['text'])

        row['text'] = row['text'].strip()
        tokenized = row['text'].split(' ')

        for token in tokenized:
            if token in words_total:
                words_total[token] += 1
                row_val[token] += 1

                words_row[row_key] = row_val

    return words_total, words_row


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0',debug=True)
                                                        
