import os
os.chdir('/Users/Miya/Desktop/Master-Thesis')
import pandas as pd                                                                                
import numpy as np
from collections import namedtuple
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
df = pd.read_excel('mydata.xlsx',sheet_name = 'Sheet1') 
growth_company = pd.read_excel('mydata.xlsx',sheet_name = 'Growth') 
mature_company = pd.read_excel('mydata.xlsx',sheet_name = 'Mature')
decline_company = pd.read_excel('mydata.xlsx',sheet_name = 'Decline')
shakeout_company = pd.read_excel('mydata.xlsx',sheet_name = 'ShakeOut')
introduction_company = pd.read_excel('mydata.xlsx',sheet_name = 'Introduction')
# assign the column ‘date’ to format ‘date’
df['date'] = pd.to_datetime(df['date'])
shakeout_company['date'] = pd.to_datetime(shakeout_company['date'])
growth_company['date'] = pd.to_datetime(growth_company['date'])
mature_company['date'] = pd.to_datetime(mature_company['date'])
introduction_company['date'] = pd.to_datetime(introduction_company['date'])
decline_company['date'] = pd.to_datetime(decline_company['date'])




#create a function to select the date block according to the month needed, and also according to the stage
def get_data_block(start_date,length):
    end_date = relativedelta(months=+length) + start_date
    mask = (df['date']>= start_date )&(df['date']<= end_date)
    list1 = df.loc[mask]
    return list1

def get_ShakeOut_block(start_date,length):
    end_date = relativedelta(months=+length) + start_date
    mask = (shakeout_company['date']>= start_date )&(shakeout_company['date']<= end_date)
    list1 = shakeout_company.loc[mask]
    return list1

def get_Growth_block(start_date,length):
    end_date = relativedelta(months=+length) + start_date
    mask = (growth_company['date']>= start_date )&(growth_company['date']<= end_date)
    list1 = growth_company.loc[mask]
    return list1

def get_Mature_block(start_date,length):
    end_date = relativedelta(months=+length) + start_date
    mask = (mature_company['date']>= start_date )&(mature_company['date']<= end_date)
    list1 = mature_company.loc[mask]
    return list1

def get_Introduction_block(start_date,length):
    end_date = relativedelta(months=+length) + start_date
    mask = (introduction_company['date']>= start_date )&(introduction_company['date']<= end_date)
    list1 = introduction_company.loc[mask]
    return list1


def get_Decline_block(start_date,length):
    end_date = relativedelta(months=+length) + start_date
    mask = (decline_company['date']>= start_date )&(decline_company['date']<= end_date)
    list1 = decline_company.loc[mask]
    return list1

# create function to select the 10% winners in a set of companies during a specific period
def momentum_company_MV(listi):
    returns = namedtuple('returns',('company','returns','MV'))
    allreturns = []
#get the list of companies in formation period
    a = list(set(listi['company']))
#calculate the returns for each company in the formation period
    for i in range(len(a)):
        b = a[i]
        list_indi = listi.loc[listi['company'] == b]
        list_indi = list_indi.sort_values('date')
#get the index (g) for the last item of the company list
        g = len(list_indi)-1
        c = list_indi.iloc[g,:]
        d = c['price']
# e is the beginning item of the list
        e = list_indi.iloc[0,:]
        f = e['price']
        h = c['MV']
#calculate the months between the periods, be careful, need to add 12 if in the next year
        if c[0].year > e[0].year:
            j = c[0].month - e[0].month + 12
        else:
            j = c[0].month - e[0].month
#calculate the total return for that period
        total_return = d/f - 1.0 
#calculate the annualized return
        if j == 0:
            annualized_return = total_return
        else:
            annualized_return = (total_return +1.0)**(12/j)-1.0
        allreturns.append(returns(b,annualized_return,h))
# sort the annualied return ascendingly, so the winners are at the bottum of the list
    allreturns = sorted(allreturns,key=lambda x: x[1])
#calculate how many companies are among the best 10%
    n = int(len(allreturns) * 0.1)
#if there are less than 10 companies, then select the best company, special case is that, when there is only one company in the whole formation period, the only company is selected
    if n == 0:
        selected = allreturns[-1:]
    else:
        selected = allreturns[-n:]
    #selected_company =[row[0] for row in selected]
    #return selected_company, including company name, annualized return, and also latest MV for this company
    return selected



#get the return of selected momentum companies in the holding period
def momentum_return_MV_weighted_full(company_list,data_block,holding_period):
    allreturns = []
    MVS = []
# a is the company name for all selected company
    a = [row[0] for row in company_list]
#o is the MV for selected company
    o = [row[2] for row in company_list]
# prepare for market value weighted portfolio
    s = sum(o)
    for i in range(len(company_list)):
        b = a[i]
        t = o[i]
#calculate return in holding period
        list_indi = data_block.loc[data_block['company']==b]
        list_indi = list_indi.sort_values('date')
        g = len(list_indi)-1
        if g == -1:
            real_return1 = 0
        else:
            c = list_indi.iloc[g,:]
            d = c['price']
            e = list_indi.iloc[0,:]
            f = e['price']
            if c[0].year > e[0].year:
                h = c[0].month - e[0].month +12
            else:
                h = c[0].month - e[0].month
            total_return = d/f - 1.0 
#if h==0, it means there is only data for one month, the total return is zero
            if h == 0:
                annualized_return = total_return
            else:
                annualized_return = (total_return +1.0)**(12/h)-1.0
            real_return1 = (annualized_return + 1)**(holding_period/12) -1
#calculate the market value weighted return
        real_return = real_return1 * t / s
#calculate the weighted market value of the investment
        q = t*t/s
#get the weighted market value for this portfolio, which is used as a factor in later analysis
        MVS.append(q)
        allreturns.append(real_return)
#return the market value weighted return, the number of companies in the portfolio, and the adjusted market value
    return sum(allreturns),len(company_list),sum(MVS)



## plot returns
def plot_returns(returns):
    x = [row[0] for row in returns] 
    y = [row[1] for row in returns]
    plt.bar(x,y, align = 'center', alpha = 0.8, width = 0.4) 
    plt.xticks(x, fontsize =8, rotation = 50)
    plt.show() 

## slightly changed from get_year_return function, logic is the same, but for different object(list.iloc vs list)
def get_annual_return(original_return_list, holding_period):
    returns = namedtuple('returns',('year','returns'))
    annual_return = []
    m = int(12/holding_period)
    n = int(len(original_return_list)/m)
    if m == 4:
        for i in range(n):
            a = original_return_list.iloc[i*m][1]
            b = original_return_list.iloc[i*m +1][1]
            c = original_return_list.iloc[i*m +2][1]
            d = original_return_list.iloc[i*m +3][1]
            e = (a +1) * (b +1) * (c +1) *(d+1)-1
            f = original_return_list.iloc[i*m][0].year
            annual_return.append(returns(f,e))
    elif m == 2:
        for i in range(n):
            a = original_return_list.iloc[i*m][1]
            b = original_return_list.iloc[i*m +1][1]
            e = (a +1) * (b +1) -1
            f = original_return_list.iloc[i*m][0].year
            annual_return.append(returns(f,e))
    elif m == 1:
        for i in range(n):
            a = original_return_list.iloc[i*m][1]
            e = a
            f = original_return_list.iloc[i*m][0].year
            annual_return.append(returns(f,e))
    else:
        a = original_return_list.iloc[i*m][1]
        e = a
        f = str(original_return_list.iloc[i*m][0].year) + '.'+str(original_return_list.iloc[i*m][0].month)
        annual_return.append(returns(f,e))
    return annual_return

    
#create a loop for all strategies and stages
formation_periods = [12,6]
holding_periods = [3,6,9,12]
return_list = []
return_all_stages = []
stages = ['Growth','Introduction','Mature','ShakeOut','Decline','All']
for x in formation_periods:
    for y in holding_periods:
        all_returns = []
        for z in stages:
            date1 = pd.Timestamp(1990,6,12)
            end_date = pd.Timestamp(2019,6,12)
            formation_period = x
            holding_period = y
            n = int(((end_date.year - date1.year) * 12 + end_date.month - date1.month - formation_period)/ holding_period)
            print (n)
            for i in range(n):
                if z == 'Growth':
                    list1 = get_Growth_block(date1,formation_period)
                elif z == 'Introduction':
                    list1 = get_Introduction_block(date1,formation_period)
                elif z == 'Mature':
                    list1 = get_Mature_block(date1,formation_period)
                elif z == 'ShakeOut':
                    list1 = get_ShakeOut_block(date1,formation_period)
                elif z == 'Decline':
                    list1 = get_Decline_block(date1,formation_period)
                elif z == 'All':
                    list1 = get_data_block(date1, formation_period)
                else:
                    pass
                companies = momentum_company_MV(list1)
                date2 = relativedelta(months=+ formation_period ) + date1
                list2 = get_data_block(date2,holding_period)
                return1 = momentum_return_MV_weighted_full(companies, list2,holding_period)
                date1 = date1 + relativedelta(months=+ holding_period )
                date3 = date2 + relativedelta(months=+ holding_period )
                returns = (date3,) + return1 + (z,) + (x,) + (y,)
                return_list.append(returns)
                
