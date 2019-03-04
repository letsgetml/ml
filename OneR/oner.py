# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 11:30:03 2019

@author: Admin
"""
import argparse
import sys

import pandas as pd
import numpy as np
from fractions import Fraction 

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--learning", help="set a learning mode. You have to add location of two required files", nargs=2)
parser.add_argument('--condition', required="--learning" in sys.argv, choices=['confidence', 'error_rate'])
parser.add_argument("-c","--classification", help="set a classification mode. You have to add location of three required files", nargs=3)
args = parser.parse_args()
if args.learning:
    
    # LEARNING MODE
    input_data_file = args.learning[0]
    output_model_file = args.learning[1]
    data = pd.read_table(input_data_file, header=(0), skiprows=(1,2))
    target_data = data[ data.columns[-1] ]
    data.drop( data.columns[-1], axis=1, inplace = True)
    #make frequency tables of each (attr,class)
    freq_tables = []       
    for label, content in data.iteritems():
        crosstab_temp = pd.crosstab(content, target_data)
        freq_tables.append(crosstab_temp)
    def write_rules(output_model_file, idx):
        # WRITE OUR RULES INTO A FILE
        f = open(output_model_file, "w+")
        f.write(data.columns[idx] + "\n")
        for index_name, row in freq_tables[idx].iterrows():
            f.write(index_name + "::" +row.idxmax() + "\n")
        f.close()
    #classification via error_rate
    if args.condition == 'error_rate':
        #computer error rates
        error_rates = []
        for table in freq_tables:
            error_rates.append([])
            for index, row in table.iterrows():
                total = row[:].sum()
                #min error of attr-val
                min_error = None
                # made enumerate(table.columns) because run through each column of row[]
                for key, value in enumerate(table.columns):
                    var_temp = total - row[key], total
                    if not min_error: min_error = var_temp
                    elif Fraction(min_error[0], min_error[1]) > Fraction(var_temp[0], var_temp[1]): 
                        min_error = var_temp
                error_rates[-1].append(min_error)
        #choose the attribute-class that has the least error 
        min_error = None
        min_error_idx = 0
        for index, innerArr in enumerate(error_rates):
            numerator = 0
            denominator = 0
            for value in innerArr:
                numerator += value[0]
                denominator += value[1]
            if not min_error: 
                min_error = numerator, denominator
                min_error_idx = index
            elif Fraction(min_error[0], min_error[1]) > Fraction(numerator, denominator):
                min_error = numerator, denominator
                min_error_idx = index 
        print(error_rates)
        print('The least error rate owner is "{0}", it`s {1}'.format(data.columns[min_error_idx], Fraction(min_error[0], min_error[1])))
        for index, row in freq_tables[min_error_idx].iterrows():
            print("IF '{0}' == '{1}' THEN '{2}' = '{3}.' Confidence = {4}. Support = {5}".format(data.columns[min_error_idx], index, target_data.name, row.idxmax(), row.max()/row.sum(), row.max() ))
        write_rules(output_model_file,min_error_idx) 
    if args.condition == 'confidence':
        confidence_rates = []
        for table in freq_tables:
            confidence_rates.append([])
            for index, row in table.iterrows():
                total = row[:].sum()
                max_confidence = None
                for key, value in enumerate(table.columns):
                    var_temp = row[key] / total
                    if not max_confidence: max_confidence = var_temp
                    elif max_confidence < var_temp:
                        max_confidence = var_temp
                confidence_rates[-1].append(max_confidence)
        # choose the attribute-class that has the max mean confidence
        max_confidence = None
        max_confidence_idx = 0
        for index,innerArr in enumerate(confidence_rates):
            var_temp = (sum(innerArr))/ (len(innerArr))
            if not max_confidence:
                max_confidence = var_temp
            elif max_confidence < var_temp:
                max_confidence = var_temp
                max_confidence_idx = index
        print(confidence_rates)
        print('The max mean confidence rate owner is "{0}", it`s {1}'.format(data.columns[max_confidence_idx], max_confidence))
        for index, row in freq_tables[max_confidence_idx].iterrows():
            print("IF '{0}' == '{1}' THEN '{2}' = '{3}.' Confidence = {4}. Support = {5}".format(data.columns[max_confidence_idx], index, target_data.name, row.idxmax(), row.max()/row.sum(), row.max() ))
        write_rules(output_model_file, max_confidence_idx)
elif args.classification:
    # TRAINING MODE
    # %run oner.py -l ./lenses_fromLecture.tab ./result_model.txt --condition confidence | error_rate
    # %run oner.py -c ./result_model.txt lenses.tab result_of_classification.tab
    input_model_file = args.classification[0]
    input_data_file = args.classification[1]
    result_file = args.classification[2]
    #UNPACK OUR MODEL
    model = []
    with open(input_model_file, "r") as f:
        txt = f.readlines()
        for line in txt:
            words = line.rstrip().split(sep="::")
            model.append(words)
    attr_name = model[0][0]
    #that`s how we remove
    model[0:1] = []
    rules = model
    del model
    #PROCEED CLASSIFICATION
    data = pd.read_table(input_data_file, header=0, skiprows=(1,2))
    model_clmn_idx = list(data.columns).index(attr_name)
    for index, row in data.iterrows():
        for rule in rules:
            if rule[0] == row[model_clmn_idx]:
                data.iloc[index, -1] = rule[1]
    data.to_csv(result_file, index=False, sep='\t')
            
        
    
    
    
    
    
    