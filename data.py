import pandas as pd
import baostock as bs
from joblib import Parallel,delayed
from tqdm import tqdm
import numpy as np
bs.login()

aval_stocks=bs.query_zz500_stocks('2024-01-01').get_data().code

def Get_data(date='2024-01-01',end_date='2024-06-10'):
    try:
        stock_df=pd.read_pickle('stock_df.pkl')
        return stock_df
    except:
        def collect_kline(code):
            bs.login()
            return bs.query_history_k_data_plus(code,'date,code,open,close,high,low,volume,turn,peTTM,pbMRQ,pctChg','2024-01-01','2024-06-10',adjustflag='1').get_data()#后复权
        res=Parallel(n_jobs=30)(delayed(collect_kline)(code) for code in tqdm(aval_stocks))
        total_df=pd.concat(res).replace("",np.nan)
        total_df.date=pd.to_datetime(total_df.date)
        total_df=total_df.set_index(['date','code']).sort_index().astype(float)
        total_df.to_pickle('stock_df.pkl')
        return total_df
    
