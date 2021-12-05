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
files = ['barackobama.csv', 
         "aoc.csv",
         "berniesanders.csv",
         "joebiden.csv",
         "kamalaharris.csv",
         "mikepence.csv",
         "arnold.csv",
         "donaldtrump.csv"]

path = r"C:\Users\marle\Downloads"

def read_files(fname, path):
    import os
    csv = pd.read_csv(os.path.join(path, fname))
    return csv

def create_total_engagement_column(df):
    df['Total_Engagement'] = df['commentCount'] + df['likeCount']
    return df

def build_csv(files, path):
    dfs = [read_files(fname, path) for fname in files]
    dfs = [create_total_engagement_column(df) for df in dfs]
    dfs = [df.nlargest(5, 'Total_Engagement') for df in dfs]
    csv = pd.concat(dfs)
    csv = csv.reset_index(drop=False)
    csv = csv[['postUrl', 'index', 'Total_Engagement', 'commentCount']]
    return csv

csv = build_csv(files = files, path = path)
csv.to_csv(r"C:\Users\marle\Documents\Github\CommentAnalysisProject\poststoscrape.csv")
    

