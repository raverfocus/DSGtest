#%%
import polars as pl
import numpy as np
#收益率偏度（Skewness of Returns）
def return_skewness(stock_df: pl.DataFrame,window: int=30) -> pl.DataFrame:
    return stock_df.with_columns(pl.col('returns').skew().over('code').alias('skew'))
#收益率峰度（Kurtosis of Returns）
def return_kurtosis(stock_df: pl.DataFrame,window: int=30) -> pl.DataFrame:
    return stock_df.with_columns(pl.col('returns').kurtosis().over('code').alias('kurt'))

#过去30天内成交量最高的25天的动量
def top_25_volume_mom(stock_df: pl.DataFrame) -> pl.DataFrame:
    result = []
    #polars没有提供方便的groupby.apply的功能，所以复杂因子只能用for循环
    for _, group in stock_df.group_by('code'):
        temp_res=[np.nan]*30
        # 计算滚动窗口中的成交量最高的25天
        for i in range(30,len(group)):
            temp=group[i-30:i]
            temp=temp.with_columns(pl.col('volume').rank(method='average').alias('volume_rank'))
            res=temp.filter(pl.col('volume_rank')<=25)['returns'].sum()
            temp_res.append(res)
        result.append(group.with_columns(pl.Series('mom1',temp_res)))
    return pl.concat(result)

#过去30天内振幅最低的25天的动量
def bot_25_fluct_mom(stock_df: pl.DataFrame) -> pl.DataFrame:
    result = []
    #polars没有提供方便的groupby.apply的功能，所以复杂因子只能用for循环
    for _, group in stock_df.group_by('code'):
        temp_res=[np.nan]*30
        # 计算滚动窗口中的成交量最高的25天
        for i in range(30,len(group)):
            temp=group[i-30:i]
            temp=temp.with_columns(pl.col('fluct').rank(method='average').alias('fluct_rank'))
            res=temp.filter(pl.col('fluct_rank')>=5)['returns'].sum()
            temp_res.append(res)
        result.append(group.with_columns(pl.Series('mom2',temp_res)))
    return pl.concat(result)
#过去30天内成交最高的20天的价量相关性
def top_20_volume_price_corr(stock_df: pl.DataFrame) -> pl.DataFrame:
    result = []
    #polars没有提供方便的groupby.apply的功能，所以复杂因子只能用for循环
    for _, group in stock_df.group_by('code'):
        temp_res=[np.nan]*30
        # 计算滚动窗口中的成交量最高的25天
        for i in range(30,len(group)):
            temp=group[i-30:i]
            temp=temp.with_columns(pl.col('volume').rank(method='average').alias('volume_rank'))
            res=temp.filter(pl.col('volume_rank')<=20).select(pl.col('volume'),pl.col('close')).corr()[0,1]
            temp_res.append(res)
        result.append(group.with_columns(pl.Series('corr1',temp_res)))
    return pl.concat(result)

#量的波动率除以收益率再乘十日动量
def volume_vol_div_return_mom(stock_df: pl.DataFrame,window: int=10) -> pl.DataFrame:
    stock_df=stock_df.with_columns([
        pl.col('volume').rolling_std(window).over('code').alias('volume_vol'),
        (pl.col('close').pct_change()).rolling_mean(window).over('code').alias('momentum')])
    stock_df=stock_df.with_columns([(pl.col('volume_vol')/pl.col('momentum')).alias('volume_vol_div_return_mom')])
    return stock_df

#处于过去三天的价格区间分位数*过去20日平均振幅/过去3日平均振幅
def price_range_quantile(stock_df: pl.DataFrame) -> pl.DataFrame:
    stock_df=stock_df.with_columns(pl.col('high').rolling_max(3).over('code').alias('high_3d'),
        pl.col('low').rolling_min(3).over('code').alias('low_3d'))
    stock_df=stock_df.with_columns([((pl.col('close')-pl.col('low_3d'))/(pl.col('high_3d')-pl.col('low_3d'))).alias('price_range_quantile')])
    stock_df=stock_df.with_columns([pl.col('fluct').rolling_mean(20).over('code').alias('avg_fluct_20d')])
    stock_df=stock_df.with_columns([pl.col('fluct').rolling_mean(3).over('code').alias('avg_fluct_3d')])
    return stock_df.with_columns((pl.col('price_range_quantile')*pl.col('avg_fluct_20d')/pl.col('avg_fluct_3d')).alias('factor1'))
