import os
import pandas as pd

path = '/path/to/folder/containing/all/files'
                      
all_files = []            
for root, dirs, files in os.walk(os.path.abspath(path)):
    for file in files:
        print(os.path.join(root, file)) 
        all_files.append(os.path.join(root, file))           
            
df = pd.DataFrame(all_files, columns =['path'])            
            
df.to_csv('metadata.csv', index = False)
