#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 21:46:36 2018

@author: ronak
"""
import arxivscraper
import pandas as pd
import numpy as np

scraper = arxivscraper.Scraper(category='stat',date_from='2017-07-21',date_until='2017-08-10',t=10, filters={'categories':['stat.ap'],'abstract':['learning']})
output = scraper.scrape()

cols = ('id', 'title', 'categories', 'abstract', 'doi', 'created', 'updated', 'authors')
df = pd.DataFrame(output,columns=cols)

adjacency_list = {}
def add_to_adList(auth_list):
    for authors in auth_list:
        for author in authors:
            if author not in adjacency_list:
                adjacency_list[author] = [x for x in authors if x != author]
            else:
                temp = [x for x in authors if x != author] + adjacency_list[author]
                temp = list(set(temp))
                adjacency_list[author] = temp
add_to_adList(df['authors'].tolist())

auth_lookup = {}
for key in adjacency_list:
    auth_lookup[key] = list(adjacency_list.keys()).index(key)

n = len(adjacency_list)
adj_matrix = np.zeros((n, n))
np.fill_diagonal(adj_matrix,0)

for author in adjacency_list:
        auth_idx = auth_lookup[author]
        for peer in adjacency_list[author]:
            peer_idx = auth_lookup[peer]
            adj_matrix[auth_idx, peer_idx] = 1

df = pd.DataFrame(adj_matrix)
df.to_csv('dataMatrix.csv')