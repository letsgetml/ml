# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 13:46:10 2019

@author: Admin
"""

import pandas as pd
import numpy as np
df_original = pd.read_table("lenses.tab", header=0, skiprows=(1,2))
df_classific = pd.read_table('result_of_classification.tab')
good = 0
for index in np.arange(df_original['lenses'].size): 
    if df_classific['lenses'][index] == df_original['lenses'][index]: good += 1
total = df_original['lenses'].size
print("OneR:Percentage of errors", (total - good) /total)

#ZERO R
rule = df_original.groupby('lenses')['lenses'].count().idxmax()
good = 0
for index in np.arange(df_original['lenses'].size): 
    if df_original['lenses'][index] == rule: good += 1
print("ZeroR:Percentage of errors", (total - good)/total)