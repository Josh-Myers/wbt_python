"""
Rename files and copy into their own directory
one for wbt and another for wba
"""
import os
import shutil
import re

#put id as prefix on each file
path = "/Users/Joshua/Documents/Python_projects/wbt_neonate/newborn_m_files"

for path, sub_directories, files in os.walk(path):
    directory_name = os.path.split(path)[1]

    for file in files:
        extension = os.path.splitext(file)[1]
        old_name = os.path.splitext(file)[0]
        source = os.path.join(path, file)
        destination = os.path.join(path,  directory_name + old_name + extension)
        os.rename(source, destination)

 
# copy all the files in the subfolders to a single folder    
source_dir = "/Users/Joshua/Documents/Python_projects/wbt_neonate/newborn_m_files"
dest_dir = "/Users/Joshua/Documents/Python_projects/wbt_neonate/all_files"


for root, dirs, files in os.walk(source_dir):  
   for file in files:
      path_file = os.path.join(root,file)
      shutil.copy2(path_file,dest_dir) 


source_dir = "/Users/Joshua/Documents/Python_projects/wbt_neonate/all_files"
wba_dir = "/Users/Joshua/Documents/Python_projects/wbt_neonate/wba_files"
wbt_dir = "/Users/Joshua/Documents/Python_projects/wbt_neonate/wbt_files"

for root, dirs, files in os.walk(source_dir):  
   for file in files:
       path_file = os.path.join(root, file)
       if re.search('WBA', file):
           shutil.copy2(path_file, wba_dir) 
       elif re.search('WB3DT', file):
           shutil.copy2(path_file, wbt_dir) 


