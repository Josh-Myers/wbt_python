#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Join with labels and munge
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
import matplotlib.pyplot as plt
import seaborn as sns  #; sns.set()

# load dfs
abs = pd.read_pickle('wba_abs_df.pkl')
mag = pd.read_pickle('wba_mag_df.pkl')
pha = pd.read_pickle('wba_pha_df.pkl')
peak = pd.read_pickle('wbt_peak_df.pkl')
amb = pd.read_pickle('wbt_amb_df.pkl')

labels = pd.read_excel('Newborn.xlsx', sheet_name=0)
labels = labels[['urn.tth', 'ear', 'cat.qual.dpoae']].copy(deep=True)

labels['ear'].replace(['L'], 'Left', inplace=True)
labels['ear'].replace(['R'], 'Right', inplace=True)
labels['urn.tth'] = labels['urn.tth'].astype(str)
labels['id_ear'] = labels['urn.tth'] + '_' + labels['ear']

#labels['label'] = pd.Categorical(labels['cat.qual.dpoae'])
#labels.drop(['cat.qual.dpoae'], inplace=True, axis=1)
labels.columns = ['id', 'ear', 'label', 'id_ear']
#labels['label'].cat.categories

labels['label'].replace(['DP pass'], 'pass', inplace=True)
labels['label'].replace(['DP refer'], 'refer', inplace=True)
labels['label'].replace(['Tymp refer'], 'refer', inplace=True)
labels['label'].replace(['tymp refer'], 'refer', inplace=True)
labels['label'].replace(['CNT'], np.nan, inplace=True)
labels['label'].replace(['DNT'], np.nan, inplace=True)

abs_df = pd.merge(labels, abs, on='id_ear', how='left')
mag_df = pd.merge(labels, mag, on='id_ear', how='left')
pha_df = pd.merge(labels, pha, on='id_ear', how='left')
peak_df = pd.merge(labels, peak, on='id_ear', how='left')
amb_df = pd.merge(labels, amb, on='id_ear', how='left')

abs_df.dropna(axis=0, how='any', inplace=True)
mag_df.dropna(axis=0, how='any', inplace=True)
pha_df.dropna(axis=0, how='any', inplace=True)
peak_df.dropna(axis=0, how='any', inplace=True)
amb_df.dropna(axis=0, how='any', inplace=True)

abs_df.sort_values(by=['id_ear'], inplace=True)
mag_df.sort_values(by=['id_ear'], inplace=True)
pha_df.sort_values(by=['id_ear'], inplace=True)
peak_df.sort_values(by=['id_ear'], inplace=True)
amb_df.sort_values(by=['id_ear'], inplace=True)

# filter out some of the most egregious outliers (abs less than -1 and mag >100)
abs_df = abs_df[abs_df['297.30'] > -1]
mag_df = mag_df[(mag_df['385.55'] < 500) & (mag_df['1887.75'] < 500) & (mag_df['8000.00'] < 500) & (mag_df['4756.83'] < 500) & (mag_df['7127.19'] < 500)]

keys = list(amb_df.id_ear.values)
abs_df = abs_df[pd.Series(list(abs_df.id_ear), index=abs_df.index).isin(keys)]

keys = list(abs_df.id_ear.values)
amb_df = amb_df[pd.Series(list(amb_df.id_ear), index=amb_df.index).isin(keys)]
peak_df = peak_df[pd.Series(list(peak_df.id_ear), index=peak_df.index).isin(keys)]
mag_df = mag_df[pd.Series(list(mag_df.id_ear), index=mag_df.index).isin(keys)]
pha_df = pha_df[pd.Series(list(pha_df.id_ear), index=pha_df.index).isin(keys)]

keys = list(mag_df.id_ear.values)
abs_df = abs_df[pd.Series(list(abs_df.id_ear), index=abs_df.index).isin(keys)]
amb_df = amb_df[pd.Series(list(amb_df.id_ear), index=amb_df.index).isin(keys)]
peak_df = peak_df[pd.Series(list(peak_df.id_ear), index=peak_df.index).isin(keys)]
pha_df = pha_df[pd.Series(list(pha_df.id_ear), index=pha_df.index).isin(keys)]

amb_df['id'].nunique()
peak_df['id'].nunique()
abs_df['id'].nunique()
mag_df['id'].nunique()
pha_df['id'].nunique()

# check if there are any rows with all zeros - will need to remove (but there were none)
#num_cols = abs_df.columns
#num_cols = num_cols[4:]

#abs_df = abs_df.loc[(abs_df[num_cols] != 0).any(1)]
#mag_df = mag_df.loc[(mag_df[num_cols] != 0).any(1)]
#pha_df = pha_df.loc[(pha_df[num_cols] != 0).any(1)]
#peak_df = peak_df.loc[(peak_df[num_cols] != 0).any(1)]
#amb_df = amb_df.loc[(amb_df[num_cols] != 0).any(1)]

# distribution of variables
abs_dist = abs_df.describe()
mag_dist = mag_df.describe()
pha_dist = pha_df.describe()
peak_dist = peak_df.describe()
amb_dist = amb_df.describe()

# have a look at the most egregious outliers 
#abs_out = abs_df.sort_values(by=['226.00'])
#mag_out = mag_df.sort_values(by=['226.00'], ascending=False)
#pha_out = pha_df.sort_values(by=['226.00'], ascending=False)
#peak_out = peak_df.sort_values(by=['226.00'], ascending=True)
#amb_out = amb_df.sort_values(by=['226.00'], ascending=False)

# create train val test sets 0.6, 0.2, 0.2
train_inds, val_test_inds = next(GroupShuffleSplit(test_size=.4, n_splits=1, random_state = 7).split(abs_df, groups=abs_df['id_ear']))

abs_train = abs_df.iloc[train_inds]
mag_train = mag_df.iloc[train_inds]
pha_train = pha_df.iloc[train_inds]
peak_train = peak_df.iloc[train_inds]
amb_train = amb_df.iloc[train_inds]

abs_val_test = abs_df.iloc[val_test_inds]
mag_val_test = mag_df.iloc[val_test_inds]
pha_val_test = pha_df.iloc[val_test_inds]
peak_val_test = peak_df.iloc[val_test_inds]
amb_val_test = amb_df.iloc[val_test_inds]

val_inds, test_inds = next(GroupShuffleSplit(test_size=.5, n_splits=1, random_state = 7).split(abs_val_test, groups=abs_val_test['id_ear']))

abs_val = abs_val_test.iloc[val_inds]
mag_val = mag_val_test.iloc[val_inds]
pha_val = pha_val_test.iloc[val_inds]
peak_val = peak_val_test.iloc[val_inds]
amb_val = amb_val_test.iloc[val_inds]

abs_test = abs_val_test.iloc[test_inds]
mag_test = mag_val_test.iloc[test_inds]
pha_test = pha_val_test.iloc[test_inds]
peak_test = peak_val_test.iloc[test_inds]
amb_test = amb_val_test.iloc[test_inds]

print(abs_train.shape, abs_val.shape, abs_test.shape)
print(mag_train.shape, mag_val.shape, mag_test.shape)
print(pha_train.shape, pha_val.shape, pha_test.shape)
print(peak_train.shape, peak_val.shape, peak_test.shape)
print(amb_train.shape, amb_val.shape, amb_test.shape)

# stack them for plotting
abs_train_p = abs_train.copy(deep=True)
abs_train_p['sample'] = 'train'
mag_train_p = mag_train.copy(deep=True)
mag_train_p['sample'] = 'train'
pha_train_p = pha_train.copy(deep=True)
pha_train_p['sample'] = 'train'
peak_train_p = peak_train.copy(deep=True)
peak_train_p['sample'] = 'train'
amb_train_p = amb_train.copy(deep=True)
amb_train_p['sample'] = 'train'

abs_val_p = abs_val.copy(deep=True)
abs_val_p['sample'] = 'val'
mag_val_p = mag_val.copy(deep=True)
mag_val_p['sample'] = 'val'
pha_val_p = pha_val.copy(deep=True)
pha_val_p['sample'] = 'val'
peak_val_p = peak_val.copy(deep=True)
peak_val_p['sample'] = 'val'
amb_val_p = amb_val.copy(deep=True)
amb_val_p['sample'] = 'val'

abs_test_p = abs_test.copy(deep=True)
abs_test_p['sample'] = 'test'
mag_test_p = mag_test.copy(deep=True)
mag_test_p['sample'] = 'test'
pha_test_p = pha_test.copy(deep=True)
pha_test_p['sample'] = 'test'
peak_test_p = peak_test.copy(deep=True)
peak_test_p['sample'] = 'test'
amb_test_p = amb_test.copy(deep=True)
amb_test_p['sample'] = 'test'

abs_p = pd.concat([abs_train_p, abs_val_p, abs_test_p])
mag_p = pd.concat([mag_train_p, mag_val_p, mag_test_p])
pha_p = pd.concat([pha_train_p, pha_val_p, pha_test_p])
peak_p = pd.concat([peak_train_p, peak_val_p, peak_test_p])
amb_p = pd.concat([amb_train_p, amb_val_p, amb_test_p])

# plot median for each sampel by pass/refer
# get numeric frequency range
freqs = abs_df.columns[4:]
freq_num = freqs.astype(float)

abs_med = abs_p.groupby(['label', 'sample']).median()
abs_med = abs_med.reset_index(drop=True)
abs_med = abs_med.values
abs_med = pd.DataFrame(abs_med)
abs_med.columns = freqs
abs_med['label'] = ['pass', 'pass', 'pass', 'refer', 'refer', 'refer']
abs_med['sample'] = ['test', 'train', 'val', 'test', 'train', 'val']
abs_med = pd.melt(abs_med, id_vars=['label', 'sample'])
abs_med.columns = ['Label', 'Sample', 'Frequency', 'Absorbance']
abs_med['Frequency'] = abs_med['Frequency'].astype(float).astype(int)

mag_med = mag_p.groupby(['label', 'sample']).median()
mag_med = mag_med.reset_index(drop=True)
mag_med = mag_med.values
mag_med = pd.DataFrame(mag_med)
mag_med.columns = freqs
mag_med['label'] = ['pass', 'pass', 'pass', 'refer', 'refer', 'refer']
mag_med['sample'] = ['test', 'train', 'val', 'test', 'train', 'val']
mag_med = pd.melt(mag_med, id_vars=['label', 'sample'])
mag_med.columns = ['Label', 'Sample', 'Frequency', 'Admittance magnitude', ]
mag_med['Frequency'] = mag_med['Frequency'].astype(float).astype(int)

pha_med = pha_p.groupby(['label', 'sample']).median()
pha_med = pha_med.reset_index(drop=True)
pha_med = pha_med.values
pha_med = pd.DataFrame(pha_med)
pha_med.columns = freqs
pha_med['label'] = ['pass', 'pass', 'pass', 'refer', 'refer', 'refer']
pha_med['sample'] = ['test', 'train', 'val', 'test', 'train', 'val']
pha_med = pd.melt(pha_med, id_vars=['label', 'sample'])
pha_med.columns = ['Label', 'Sample', 'Frequency', 'Admittance phase', ]
pha_med['Frequency'] = pha_med['Frequency'].astype(float).astype(int)

peak_med = peak_p.groupby(['label', 'sample']).median()
peak_med = peak_med.reset_index(drop=True)
peak_med = peak_med.values
peak_med = pd.DataFrame(peak_med)
peak_med.columns = freqs
peak_med['label'] = ['pass', 'pass', 'pass', 'refer', 'refer', 'refer']
peak_med['sample'] = ['test', 'train', 'val', 'test', 'train', 'val']
peak_med = pd.melt(peak_med, id_vars=['label', 'sample'])
peak_med.columns = ['Label', 'Sample', 'Frequency', 'Peak Absorbance', ]
peak_med['Frequency'] = peak_med['Frequency'].astype(float).astype(int)

amb_med = amb_p.groupby(['label', 'sample']).median()
amb_med = amb_med.reset_index(drop=True)
amb_med = amb_med.values
amb_med = pd.DataFrame(amb_med)
amb_med.columns = freqs
amb_med['label'] = ['pass', 'pass', 'pass', 'refer', 'refer', 'refer']
amb_med['sample'] = ['test', 'train', 'val', 'test', 'train', 'val']
amb_med = pd.melt(amb_med, id_vars=['label', 'sample'])
amb_med.columns = ['Label', 'Sample', 'Frequency', 'Absorbance 0 daPa', ]
amb_med['Frequency'] = amb_med['Frequency'].astype(float).astype(int)

# plot
f, ax = plt.subplots(figsize=(12, 7))
ax.set(xscale="log")
sns.lineplot(x="Frequency", y="Absorbance", hue='Label', style='Sample', data=abs_med)

f, ax = plt.subplots(figsize=(12, 7))
ax.set(xscale="log")
sns.lineplot(x="Frequency", y="Admittance magnitude", hue='Label', style='Sample', data=mag_med)

f, ax = plt.subplots(figsize=(12, 7))
ax.set(xscale="log")
sns.lineplot(x="Frequency", y="Admittance phase", hue='Label', style='Sample', data=pha_med)

f, ax = plt.subplots(figsize=(12, 7))
ax.set(xscale="log")
sns.lineplot(x="Frequency", y="Peak Absorbance", hue='Label', style='Sample', data=peak_med)

f, ax = plt.subplots(figsize=(12, 7))
ax.set(xscale="log")
sns.lineplot(x="Frequency", y="Absorbance 0 daPa", hue='Label', style='Sample', data=amb_med)

# make pngs - need to always set y axis range so all same scale
# absorbance < 0 = 0
# mag y axis = 0-5
# need to make pha positive +200 and set y-axis from 0 to 400
abs_png = abs_df.copy(deep=True)
mag_png = mag_df.copy(deep=True)
pha_png = pha_df.copy(deep=True)
peak_png = peak_df.copy(deep=True)
amb_png = amb_df.copy(deep=True)

# set <0 to 0 for absorbance variables
abs_png[freqs] =  abs_png[freqs].clip(lower=0)
peak_png[freqs] =  peak_png[freqs].clip(lower=0)
amb_png[freqs] =  amb_png[freqs].clip(lower=0)

# make phase non-negative
pha_png[freqs] = pha_png[freqs] + 200

# abs
for i in range(abs_png.shape[0]): # or range(0, len(abs_png))
    data = abs_png.iloc[i]
    id = data[3]
    wai = data[4:]
    plt.figure()
    plt.xlim(226, 8000)
    plt.ylim(0, 1)
    wai.plot(kind='area', color='black')
    plt.axis('off')
    plt.savefig('images/abs/' + id, bbox_inches='tight', pad_inches=0)
    plt.clf()
  
# mag    
for i in range(mag_png.shape[0]):
    data = mag_png.iloc[i]
    id = data[3]
    wai = data[4:]
    plt.figure()
    plt.xlim(226, 8000)
    plt.ylim(0, 7)
    wai.plot(kind='area', color='black')
    plt.axis('off')
    plt.savefig('images/mag/' + id, bbox_inches='tight', pad_inches=0)
    plt.clf()
    
# pha   
for i in range(pha_png.shape[0]):
    data = pha_png.iloc[i]
    id = data[3]
    wai = data[4:]
    plt.figure()
    plt.xlim(226, 8000)
    plt.ylim(0, 300)
    wai.plot(kind='area', color='black')
    plt.axis('off')
    plt.savefig('images/pha/' + id, bbox_inches='tight', pad_inches=0)
    plt.clf()
   
# peak 
for i in range(peak_png.shape[0]):
    data = peak_png.iloc[i]
    id = data[3]
    wai = data[4:]
    plt.figure()
    plt.xlim(226, 8000)
    plt.ylim(0, 1)
    wai.plot(kind='area', color='black')
    plt.axis('off')
    plt.savefig('images/peak/' + id, bbox_inches='tight', pad_inches=0)
    plt.clf()

# amb 
for i in range(amb_png.shape[0]):
    data = amb_png.iloc[i]
    id = data[3]
    wai = data[4:]
    plt.figure()
    plt.xlim(226, 8000)
    plt.ylim(0, 1)
    wai.plot(kind='area', color='black')
    plt.axis('off')
    plt.savefig('images/amb/' + id, bbox_inches='tight', pad_inches=0)
    plt.clf()
    