import pandas as pd

#note that it is important for all files to have only two row above the header
MT = pd.read_excel('Unit list 12520 Master of Translation Studies.xlsx', skiprows=2) #skip first two row of excel file
MIT = pd.read_excel('Unit list 62510 Master of Information Technology.xlsx', skiprows=2) 
MPE = pd.read_excel('Unit list 62550 Master of Professional Engineering.xlsx', skiprows=2)

unitlists_joined = pd.concat([MT, MIT, MPE], ignore_index=True)
unitlists_duplicates_merged = unitlists_joined.groupby("Code").first().reset_index()

unitlists_duplicates_merged.to_csv('Unit list.csv')
