'''
Tools to be used during the operations
'''
from cgi import test
import plotly.graph_objects as go
import crypto_backend.data as datar
import pandas as pd

def time_series_generator(X, y):
    pass

# Memory saving function that can only be used with df
def reduce_mem_usage(df):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.
    """
    start_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))

    for col in df.columns:
        col_type = df[col].dtype.name

        if col_type not in ['object', 'category', 'datetime64[ns, UTC]', 'datetime64[ns]']:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)

    end_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))

    return df


# This train test generator's default assumes the following,
# approximately 2 years of data is input into the function
# It then makes 20 4-month-long train_test_split sets where the first 3 month is train and last month is test
# each set is 1 month further than the previous set . this can be changed by changing the step

def train_test_generator(X,test_sets=20,train_size=3*30*24*60,test_size=30*24*60,step = 30*24*60):
    X_train= []
    X_test=[]
    for i in range(test_sets):
        #start at the beginning of the set
        start= i*(step)
        #training set
        X_train.append(X.iloc[(start):(start+train_size)])
        #testing set
        X_test.append(X.iloc[(start+train_size):(start+train_size+test_size)])

    return X_train,X_test

#take in prediction take from facebook then graphs it together with previous data
def FB_grapher(fb_data,currency):
    data = datar.get_data(currency)
    odata = datar.organize_data(data)
    d_data = datar.daily_data(odata)
    fig1 = go.Figure(data=[go.Candlestick(x=d_data['time'],
                                        open=d_data['open'],
                                        high=d_data['high'],
                                        low=d_data['low'],
                                        close=d_data['close'],
                                        name = 'Historical Data'),
                go.Scatter(x=fb_data.ds.iloc[-14:],
                            y=fb_data.yhat.iloc[-14:],
                            mode='lines',
                            name = 'Prediction')
                ])
    return fig1


#take in prediction in the form returned fom sarimax_predict then graphs it together with previous data

def sarimax_grapher(sarimax_data,currency):
    data = datar.get_data(currency)
    odata = datar.organize_data(data)
    d_data = datar.daily_data(odata)
    pred_x = sarimax_data.pred.index
    fig2 = go.Figure(data=[go.Candlestick(x=d_data['time'],
                                        open=d_data['open'],
                                        high=d_data['high'],
                                        low=d_data['low'],
                                        close=d_data['close'],
                                        name = 'Historical Data'),
                go.Scatter(x=pred_x,
                            y=sarimax_data.pred.close,
                            mode='lines',
                            name = 'Prediction'),
                go.Scatter(
                        x=pred_x +pred_x[::-1], # x, then x reversed
                        y=sarimax_data.upper+sarimax_data.lower[::-1], # upper, then lower reversed
                        fill='toself',
                        fillcolor='rgba(0,100,80,0.2)',
                        line=dict(color='rgba(255,255,255,0)'),
                        hoverinfo="skip",
                        showlegend=False)
                ])
    return fig2


if __name__ == '__main__':
    # Test function here
    pass
