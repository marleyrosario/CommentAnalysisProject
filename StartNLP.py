# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 17:37:22 2021

@author: marle
"""

import pandas as pd
import os
import PyPDF2 
import spacy
import itertools
import pandas as pd
from statistics import mean
import string as str
import numpy as np
from spacymoji import Emoji
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import matplotlib.pyplot as plt

path = r"C:\Users\marle\Downloads"

def open_csvs(fname, path):
    df = pd.read_csv(os.path.join(path, fname))
    return df

def create_list_of_dfs():
    fname = "csv"
    list_of_fnames = []
    for i in range(1,2):
        list_of_fnames.append(fname + f" ({i})")
    list_of_fnames.append(fname)    
    list_of_fnames = [fname + ".csv" for fname in list_of_fnames]
    list_of_dfs = [open_csvs(fname, path = path) for fname in list_of_fnames]
    return list_of_dfs

list_of_dfs = create_list_of_dfs()

def clean_list_of_dfs(list_of_dfs):
    dfs_not_scrapable = []
    for df in list_of_dfs:
        if 'comment' not in df.columns:
            dfs_not_scrapable.append(df)        
    list_of_dfs = [x for x in list_of_dfs if x not in dfs_not_scrapable]
    return list_of_dfs, dfs_not_scrapable

list_of_dfs, dfs_not_scrapable = clean_list_of_dfs(list_of_dfs)

def start_nlp_processing(list_of_dfs):
    list_of_dfs = [df.to_dict() for df in list_of_dfs]
    nlp = spacy.load("en_core_web_sm")
    emoji = Emoji(nlp)
    nlp.add_pipe("emoji", first=True)
    comments = [{k:v for k,v in columns.items() if 'comment' in k} for columns in list_of_dfs]
    comments = [[v for k,v in comment.items()] for comment in comments]
    comments = [comments[0] for comments in comments]
    comments = [[v for k,v in comments.items()] for comments in comments]
    comments = [[nlp(comment) for comment in comments] for comments in comments]
    tokens = [[list(doc) for doc in docs] for docs in comments]
    import itertools
    tokens = [list(itertools.chain.from_iterable(tokens)) for tokens in tokens]
    tokens = [[t for t in list_of_tokens if t.is_stop == False] for list_of_tokens in tokens]
    tokens = [[t for t in list_of_tokens if t.is_punct == False] for list_of_tokens in tokens]
    tokens = [[t for t in list_of_tokens if t.like_num == False] for list_of_tokens in tokens]
    tokens = [[t for t in list_of_tokens if t._.is_emoji==False] for list_of_tokens in tokens]
    text = [[t.text for t in list_of_tokens] for list_of_tokens in tokens]
    return text

text = start_nlp_processing(list_of_dfs)

def main(comment):
    Concordance = { }
    for word in comment:
        if word in Concordance.keys():
            freq = Concordance.get(word)
            freq += 1
            Concordance[word]= freq
        else:
            freq = 1
            Concordance[word]= freq
    return Concordance

def send_analysis_to_dict(text):
    text = [main(comment) for comment in text]
    list_of_political_topics = ['immigration', 'election', 'econ']
    text = [{k:v for k,v in comment.items() if k in list_of_political_topics} for comment in text]
    vis = [pd.DataFrame(comment, index=[0]) for comment in text]
    vis = [comment.T for comment in vis]
    vis = [comment.reset_index(drop=False) for comment in vis]
    vis = [comment.rename(columns = {"index":"comment", 0:"Freq"}) for comment in vis]
    for i in range(len(text)):
        list_of_dfs[i].update({"comment":text[i]})
    return vis, list_of_dfs

vis, list_of_dfs = send_analysis_to_dict(text)

def build_go_figure(df):
    fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns,
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.comment, df.Freq],
                   fill_color='lavender',
                   align='left'))])
    fig.update_layout(title_text='Comments and Frequency')
    pio.renderers.default='browser'
    fig.show()


for df in vis:
    build_go_figure(df)



