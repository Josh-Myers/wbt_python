#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract ambient data
"""
import re
import os
import pandas as pd

f = open("test.m", "r")
id = '123'
wba = f.read()
vars = wba.split(';')

ear = vars[8]
abs = vars[10]
mag = vars[11]
pha = vars[12]

freq =vars[9]
freqs = freq[34:-1]
freqs = freqs.split(', ')

ear_r = re.compile(r'\bLeft\b | \bRight\b', flags=re.I | re.X)
ear = ear_r.findall(ear)
ear = str(ear).strip('[]').strip("''")
id_ear = id + "_" + str(ear)

abs = abs[33:].strip('[]')
abs = abs.split(', ')
abs.insert(0, id_ear)


mag = mag[44:].strip('[]')
mag = mag.split(', ')
mag.insert(0, id_ear)

pha = pha[46:].strip('[]')
pha = pha.split(', ')
pha.insert(0, id_ear)


wba_path = "/Users/Joshua/Documents/Python_projects/wbt_neonate/wba_files"

freqs.insert(0, 'id_ear')

wba_abs = []
wba_mag = []
wba_pha = []

for root, dirs, files in os.walk(wba_path):
    for file in files:
        id = file[0:6]
        f = open(os.path.join(wba_path, file), 'r')
        wba = f.read()
        vars = wba.split(';')
        
        ear = vars[8]
        abs = vars[10]
        mag = vars[11]
        pha = vars[12]
        
        ear_r = re.compile(r'\bLeft\b | \bRight\b', flags=re.I | re.X)
        ear = ear_r.findall(ear)
        ear = str(ear).strip('[]').strip("''")
        id_ear = id + "_" + str(ear)
        
        abs = abs[33:].strip('[]')
        abs = abs.split(', ')
        abs.insert(0, id_ear)
        
        mag = mag[44:].strip('[]')
        mag = mag.split(', ')
        mag.insert(0, id_ear)
        
        pha = pha[46:].strip('[]')
        pha = pha.split(', ')
        pha.insert(0, id_ear)
        
        try:   # there was one mag that was really long - sth wrong with it
            assert len(abs)==108 
            assert len(mag)== 108
            assert len(pha)==108
            
            wba_abs.append(abs)
            wba_mag.append(mag)
            wba_pha.append(pha)
            
        except AssertionError: 
            pass
    
wba_abs_df = pd.DataFrame(wba_abs, columns=freqs)
wba_mag_df = pd.DataFrame(wba_mag, columns=freqs)
wba_pha_df = pd.DataFrame(wba_pha, columns=freqs)

wba_abs_df = wba_abs_df.drop_duplicates(['id_ear'])
wba_mag_df = wba_mag_df.drop_duplicates(['id_ear'])
wba_pha_df = wba_pha_df.drop_duplicates(['id_ear'])

num_cols = wba_abs_df.columns
num_cols = num_cols[1:]

wba_abs_df[num_cols] = wba_abs_df[num_cols].apply(pd.to_numeric, errors='coerce', downcast='float')
wba_mag_df[num_cols] = wba_mag_df[num_cols].apply(pd.to_numeric, errors='coerce', downcast='float')
wba_pha_df[num_cols] = wba_pha_df[num_cols].apply(pd.to_numeric, errors='coerce', downcast = 'float')

wba_abs_df.to_pickle('wba_abs_df.pkl') 
wba_mag_df.to_pickle('wba_mag_df.pkl') 
wba_pha_df.to_pickle('wba_pha_df.pkl') 

# to load
#df = pd.read_pickle('wba_mag_df.pkl')



import matplotlib.pyplot as plt
row = wba_abs_df.iloc[0]
row = row[1:]
row.plot(kind='area')
plt.show()

row = wba_mag_df.iloc[0][1:]
row.plot(kind='area')
plt.show()

# pha need to add 5 or so to make them all positive
row = wba_pha_df.iloc[0][1:]
row = row + 20
ax.set_yscale('log')
row.plot(kind='area')
plt.show()




