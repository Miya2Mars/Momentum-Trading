import pandas as pd                                                                                
import datetime	

# prase data
df = pd.read_excel('mydata.xlsx', sheet_name = 'Sheet1') 
growth_company = pd.read_excel('mydata.xlsx', sheet_name = 'Growth') 
mature_company = pd.read_excel('mydata.xlsx', sheet_name = 'Mature')
decline_company = pd.read_excel('mydata.xlsx', sheet_name = 'Decline')
shakeout_company = pd.read_excel('mydata.xlsx', sheet_name = 'ShakeOut')
introduction_company = pd.read_excel('mydata.xlsx', sheet_name = 'Introduction')

# assign the column 'date' to format 'date'
df['date'] = pd.to_datetime(df['date'])
shakeout_company['date'] = pd.to_datetime(shakeout_company['date'])
growth_company['date'] = pd.to_datetime(growth_company['date'])
mature_company['date'] = pd.to_datetime(mature_company['date'])
introduction_company['date'] = pd.to_datetime(introduction_company['date'])
decline_company['date'] = pd.to_datetime(decline_company['date'])
