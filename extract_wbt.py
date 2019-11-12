import re
import os
import pandas as pd

# first need to rename each file with id
# then put all in one folder (one folder for amb and one for wbt)
# then for loop to convert each - object name will be id + earside

f = open("test2.m", "r")
id = '123'
wbt = f.read()
vars = wbt.split(';')

ear = vars[8]
peak = vars[56]
amb = vars[57]
abs_tymp = vars[50]

freq =vars[10]
freqs = freq[36:-1]
freqs = freqs.split(', ')

pres = vars[9]
press = pres[41:-1]
press = press.split(', ')
press = press[:10]

ear_r = re.compile(r'\bLeft\b | \bRight\b', flags=re.I | re.X)
ear = ear_r.findall(ear)
ear = str(ear).strip('[]').strip("''")
id_ear = id + "_" + str(ear)

peak = peak[39:].strip('[]')
peak = peak.split(',')
#type(peak)
peak.insert(0, id_ear)

#peak = [float(i) for i in peak]
#peak = np.asarray(peak)

amb = amb[42:].strip('[]')
amb = amb.split(',')
#amb = [float(i) for i in amb]
#amb = np.asarray(amb)

#abs_tymp = abs_tymp[46:].strip('[]')
#abs_tymp = abs_tymp.split(',')
#abs_tymp = abs_tymp[:10]
#abs_tymp = [float(i) for i in abs_tymp]
#abs_tymp = np.asarray(abs_tymp)


# do a function for wba and another for wbt

# for file in files:
# id = filename[0:5]
# extract variables
# name of each var is id + earside + var_type (eg amb)
# return a list will all the vars
# so for wbt it will be list of 3 amb, peak, abs_tymp
# save each variable into a list wbt_peak[] all the peak arrays

# will need to remove duplicates also (some retest)
wbt_path = "/Users/Joshua/Documents/Python_projects/wbt_neonate/wbt_files"

freqs.insert(0, 'id_ear')
press.insert(0, 'id_ear')

wbt_peak = []
wbt_amb = []
#wbt_abs_tymp = pd.DataFrame(columns=press)

for root, dirs, files in os.walk(wbt_path):
    for file in files:
        id = file[0:6]
        f = open(os.path.join(wbt_path, file), 'r')
        wbt = f.read()
        vars = wbt.split(';')
        ear = vars[8].strip('[]')
        peak = vars[56]
        amb = vars[57]
        #abs_tymp = vars[50]
        
        ear_r = re.compile(r'\bLeft\b | \bRight\b', flags=re.I | re.X)
        ear = ear_r.findall(ear)
        ear = str(ear).strip('[]').strip("''")
        
        peak = peak[39:].strip('[]')
        peak = peak.split(',')
        
        #peak = [float(i) for i in peak]
        #peak = np.asarray(peak)
        
        amb = amb[42:].strip('[]')
        amb = amb.split(',')
        #amb = [float(i) for i in amb]
        #amb = np.asarray(amb)
        
        #abs_tymp = abs_tymp[46:].strip('[]')
        #abs_tymp = abs_tymp.split(',')
        #abs_tymp = abs_tymp[:10]
        #abs_tymp = [float(i) for i in abs_tymp]
        #abs_tymp = np.asarray(abs_tymp)
        
        id_ear = id + "_" + str(ear)
        
        peak.insert(0, id_ear)
        amb.insert(0, id_ear)
        #abs_tymp.insert(0, id_ear)
        
        wbt_peak.append(peak)
        wbt_amb.append(amb)
        
        #abs_tymp_df = pd.DataFrame([abs_tymp], columns=press)
        #wbt_abs_tymp = wbt_abs_tymp.append(abs_tymp_df)
        
wbt_peak_df = pd.DataFrame(wbt_peak, columns=freqs)
wbt_amb_df = pd.DataFrame(wbt_amb, columns=freqs)
    
wbt_peak_df = wbt_peak_df.drop_duplicates(['id_ear'])
wbt_amb_df = wbt_amb_df.drop_duplicates(['id_ear'])

num_cols = wbt_peak_df.columns
num_cols = num_cols[1:]

wbt_peak_df[num_cols] = wbt_peak_df[num_cols].apply(pd.to_numeric, errors='coerce', downcast='float')
wbt_amb_df[num_cols] = wbt_amb_df[num_cols].apply(pd.to_numeric, errors='coerce', downcast='float')

wbt_peak_df.to_pickle('wbt_peak_df.pkl') 
wbt_amb_df.to_pickle('wbt_amb_df.pkl') 
        

