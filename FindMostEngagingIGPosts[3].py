# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 09:59:48 2021

@author: marle
"""

"""
After running ScrapePoliticianIGPosts.py, PhantomBuster will have downloaded
the files to your local machine. Put the path to those files in the path 
variable and the name of the files in the list.
"""

import pandas as pd
import os 

path = r"C:\Users\marle\Downloads"

def open_csvs(fname, path):
    df = pd.read_csv(os.path.join(path, fname))
    return df

def create_list_of_dfs():
    fname = "csv"
    list_of_fnames = []
    for i in range(1,9):
        list_of_fnames.append(fname + f" ({i})")
    list_of_fnames.append(fname)    
    list_of_fnames = [fname + ".csv" for fname in list_of_fnames]
    list_of_dfs = [open_csvs(fname, path = path) for fname in list_of_fnames]
    return list_of_dfs

list_of_dfs = create_list_of_dfs()

def create_total_engagement_column(df):
    df['Total_Engagement'] = df['commentCount'] + df['likeCount']
    return df

def build_csv(list_of_dfs):
    dfs = list_of_dfs
    dfs = [create_total_engagement_column(df) for df in dfs]
    dfs = [df.nlargest(5, 'Total_Engagement') for df in dfs]
    csv = pd.concat(dfs)
    csv = csv.reset_index(drop=False)
    csv = csv[['postUrl', 'index', 'Total_Engagement', 'commentCount', 'query']]
    return csv

csv = build_csv(list_of_dfs)
csv.to_csv(r"C:\Users\marle\Documents\Github\CommentAnalysisProject\poststoscrape.csv")
    

