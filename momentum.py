import os
import pandas as pd                                                                                
import numpy as np
from collections import namedtuple
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from global_var import *
from func import *

## plot returns
def plot_returns(returns):
    x = [row[0] for row in returns] 
    y = [row[1] for row in returns]
    plt.bar(x,y, align = 'center', alpha = 0.8, width = 0.4) 
    plt.xticks(x, fontsize =8, rotation = 50)
    plt.show() 

if __name__ == '__main__':

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
                
