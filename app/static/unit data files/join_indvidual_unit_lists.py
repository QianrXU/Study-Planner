import pandas as pd
import glob
import os

# download these files and place them all, including the .py script, in a directory 
# before you run the script.

path = os.getcwd()
files = glob.glob(os.path.join(path, "*.xlsx"))
  
# empty data frame for the new output excel file with the merged excel files
output = pd.DataFrame()

# loop over the list of csv files
for file in files:

    # print the filename
    print('File name:', file.split("\\")[-1])

    # read file
    x = pd.read_excel(file, skiprows=2)

    # appending data
    output = output.append(x, ignore_index=True)

merged = output.groupby("Code").first().reset_index()
merged.to_csv("Unit list.csv", index=False)