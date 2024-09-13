#%%
import time
from functools import wraps
import statsmodels.api as sm
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

# 定义timer装饰器
def timer(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start_time=time.time()  
        result=func(*args,**kwargs) 
        end_time=time.time()
        run_time=end_time-start_time
        print(f"Function '{func.__name__}' executed in {run_time:.4f} seconds")
        return result 
    return wrapper

def calc_factor_return(df:pl.DataFrame,factor_col:str,return_col:str) -> float:
    sorted_df=df.sort(by=factor_col,descending=True)  
    top_quantile=sorted_df[:int(len(sorted_df)*0.2)] 
    bot_quantile=sorted_df[int(len(sorted_df)*0.8):]
    return top_quantile[return_col].mean()-bot_quantile[return_col].mean()

def calculate_max_drawdown(returns:np.array) -> float:
    cumulative=np.cumsum(returns)  
    max_cumulative=np.maximum.accumulate(cumulative)
    drawdown=max_cumulative-cumulative
    max_drawdown=np.max(drawdown)
    return max_drawdown

# 因子换手率计算函数
def calculate_turnover_rate(stock_df:pl.DataFrame,factor_col:str,top_n=100) -> float:



    #为每个日期选择前top_n的股票作为持仓
    stock_df=stock_df.with_columns([
        pl.col(factor_col).rank().over("date").alias("rank")])
    stock_df=stock_df.with_columns([
        (pl.col("rank") < top_n).alias("in_portfolio")])

    #计算换手率：持仓组合的变化情况
    stock_df=stock_df.sort(by=["code","date"])
    stock_df=stock_df.with_columns([
        pl.col("in_portfolio").shift(1).over("code").alias("prev_in_portfolio")])

    #如果当前持仓状态和上一天不同，表示持仓发生了变动
    stock_df=stock_df.with_columns([
        (pl.col("in_portfolio") != pl.col("prev_in_portfolio")).alias("turnover_flag")])

    #计算每个调仓周期的换手率
    turnover_rate=stock_df.group_by("date").agg([pl.col("turnover_flag").mean().alias("daily_turnover")])["daily_turnover"].mean()

    return turnover_rate

#绘制单因子的累计收益率和每日的最大回撤
def plot_factor_performance(stock_df:pl.DataFrame,factor_name:str):
    stock_df=stock_df.with_columns([pl.col('return').cum_sum().alias('cumulative_return')])

    cumulative_return=stock_df.select(['date','cumulative_return']).to_pandas()
    cumulative_return.set_index('date',inplace=True)

    # 计算最大回撤
    cumulative_return['drawdown']=(1+cumulative_return['cumulative_return'])/(1+cumulative_return['cumulative_return'].cummax())-1
    cumulative_return['drawdown']=cumulative_return['drawdown'].clip(upper=0)

    fig, ax1 = plt.subplots(figsize=(12, 6))
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Cumulative Return', color=color)
    ax1.plot(cumulative_return.index, cumulative_return['cumulative_return'], color=color, label='Cumulative Return')
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Drawdown', color=color)
    ax2.fill_between(cumulative_return.index, cumulative_return['drawdown'], color=color, alpha=0.3, label='Drawdown')
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title(f'{factor_name} Performance')
    fig.tight_layout()

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.savefig(f'{factor_name} performance.png')
    plt.show()



def evaluate_factors(df:pl.DataFrame,factor_col:str,return_col:str,period:int=5) -> dict:
    ic_list=[]
    factor_return_list=[]

    df_rank=df.select(pl.col('date'),pl.col(factor_col).rank().over('date').alias('rank_f'),pl.col(return_col).rank().over('date').alias('rank_r')).drop_nulls()

    for d in df['date'].unique()[:-1]:
        ic_list.append(df_rank.filter(pl.col('date')==d).drop_nulls().corr()[2,1])
        factor_return_list.append(calc_factor_return(df.filter(pl.col('date')==d),factor_col,return_col))

    if np.nanmean(ic_list)<0:
        df=df.with_columns(pl.col(factor_col)*(-1))
        factor_return_list=[-x for x in factor_return_list]
        dire='neg'
    else:
        dire='pos'
    
    icir=np.round(np.nanmean(ic_list)/np.nanstd(ic_list),3)
    win_rate=np.round(np.sum(np.sign(factor_return_list))/2/len(factor_return_list)+0.5,3)
    turnover_rate=calculate_turnover_rate(df,factor_col)
    max_drawdown=calculate_max_drawdown(factor_return_list)

    plot_factor_performance(pl.DataFrame({'date':df['date'].unique()[:-1],'return':factor_return_list}),factor_col)

    return {
        "IC":np.round(np.nanmean(ic_list),3),
        "ICIR":icir,
        "Direction":dire,
        "Factor Long-Short Return":np.round(np.mean(factor_return_list),3),
        "Win Rate":win_rate,
        'Turnover Rate':turnover_rate,
        'Max Drawdown':max_drawdown,
    }