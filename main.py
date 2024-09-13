#%%
import polars as pl
import pickle
import numpy as np
from factors import *
import warnings
warnings.filterwarnings('ignore')

if __name__=="__main__":


    f=open('stock_df.pkl','rb')
    data=pickle.load(f)
    f.close()
    data=pl.DataFrame(data.reset_index())
    stock_df=data.with_columns((data['high']/data['low']-1).alias('fluct'))
    stock_df=stock_df.with_columns((pl.col('pctChg')/100).alias('returns'))
    stock_df=stock_df.with_columns((pl.col('pctChg').shift(-1).over('code')/100).alias('next_returns'))


    stock_df = return_skewness(stock_df)
    stock_df = return_kurtosis(stock_df)
    stock_df = top_25_volume_mom(stock_df)
    stock_df = bot_25_fluct_mom(stock_df)
    stock_df = top_20_volume_price_corr(stock_df)
    stock_df = volume_vol_div_return_mom(stock_df)
    stock_df = price_range_quantile(stock_df)

    from measures import *
    for col in ['skew','kurt','mom1','mom2','corr1','volume_vol_div_return_mom','factor1']:
        print(evaluate_factors(stock_df,col,'next_returns'))

    print('end')