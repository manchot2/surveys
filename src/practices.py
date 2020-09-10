#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 19:49:02 2020

@author: manchot2
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
Data preparation section
"""

data = pd.read_csv('../files/Sexual practice by gender survey.csv')

#Columns with practices
colnames_append = list(data.iloc[0])

#Columns with "like" or "dislikes" & renaming the unnames columns
data.columns = data.columns.to_series().mask(lambda x: x.str.startswith('Unnamed')).ffill()
colnames = list(data.columns)

#useless lines, only for data exploration purposes
#data["What gender do you identify with"].isna().sum()
#data[data["What gender do you identify with"]=='Female'].shape[0]
#data[data["What gender do you identify with"]=='Male'].shape[0]

#renaming the gender column
data["gender"] = data["What gender do you identify with"]
data = data.drop(["What gender do you identify with"], axis = 1)
#print(pd.crosstab(index=data["gender"],columns="count"))

general_pop = data.shape[0]
f_pop = data[data.gender == 'Female'].shape[0]
m_pop = data[data.gender == 'Male'].shape[0]

### Split in three dataset
data_like = data.drop(["What are your favorite practice?", "What practice do you want to avoid?"], axis = 1)
data_love = data.drop(["Which practices do you like (whithout especially being you favorite)", "What practice do you want to avoid?"], axis = 1)
data_hate = data.drop(["Which practices do you like (whithout especially being you favorite)", "What are your favorite practice?"], axis = 1)

#renaming the columns 
new_name = []
for index, name in enumerate(data_like.columns):
    if name == 'Which practices do you like (whithout especially being you favorite)':
        new_name.append(data_like.iloc[0, index])
    else :
        new_name.append(name)
data_like.columns = new_name

new_name = []
for index, name in enumerate(data_love.columns):
    if name == "What are your favorite practice?":
        new_name.append(data_love.iloc[0, index])
    else :
        new_name.append(name)
data_love.columns = new_name

new_name = []
for index, name in enumerate(data_hate.columns):
    if name == "What practice do you want to avoid?":
        new_name.append(data_hate.iloc[0, index])
    else :
        new_name.append(name)
data_hate.columns = new_name

#data_love.to_csv("../files/love.csv")
#data_love.to_csv("../files/like.csv")
#data_love.to_csv("../files/hate.csv")

#uncomment to check if pop count are alright
#print(pd.crosstab(index=data_love["gender"],columns="count"))

### Creating the count dataset : Male and Females
#like dataset
columns = data_like.columns

#proportion by gender population in percents
general_likes = tuple((general_pop-data_like.isna().sum())/general_pop*100)
female_likes = tuple((f_pop-data_like[data_like.gender == 'Female'].isna().sum())/f_pop*100)
male_likes = tuple((m_pop-data_like[data_like.gender == 'Male'].isna().sum())/m_pop*100)


like_sum = pd.DataFrame.from_records([general_likes, female_likes, male_likes], 
               columns = columns)
diff = abs(like_sum.diff().iloc[2])
like_sum = like_sum.append(diff)
like_sum = like_sum.iloc[:, 9:]
like_sum.index = ['general', 'female', 'male', 'difference']

#hate dataset
#proportion by gender population in percents
general = tuple((general_pop-data_hate.isna().sum())/general_pop*100)
female = tuple((f_pop-data_hate[data_hate.gender == 'Female'].isna().sum())/f_pop*100)
male = tuple((m_pop-data_hate[data_hate.gender == 'Male'].isna().sum())/m_pop*100)

hate_sum = pd.DataFrame.from_records([general, female, male], 
               columns = columns)
diff = abs(hate_sum.diff().iloc[2])
hate_sum = hate_sum.append(diff)
hate_sum = hate_sum.iloc[:, 9:]
hate_sum.index = ['general', 'female', 'male', 'difference']


#love dataset
#proportion by gender population in percents
general = tuple((general_pop-data_love.isna().sum())/general_pop*100)
female = tuple((f_pop-data_love[data_love.gender == 'Female'].isna().sum())/f_pop*100)
male = tuple((m_pop-data_love[data_love.gender == 'Male'].isna().sum())/m_pop*100)


love_sum = pd.DataFrame.from_records([general, female, male], 
               columns = columns)
diff = abs(love_sum.diff().iloc[2])
love_sum = love_sum.append(diff)
love_sum = love_sum.iloc[:, 9:]
love_sum.index = ['general', 'female', 'male', 'difference']







"""
Exploratory part
"""

#First dataset : most favorite practices
print("The most favorite practices are  \n{}".format(love_sum.iloc[0].sort_values(ascending = False)[2:8]))






