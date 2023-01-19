import datetime as dt
import pandas_datareader.data as web
import matplotlib.pyplot as plt
plt.style.use('dark_background')

# implementing the moving average crossover strategy

# choosing time frames
ma_1=30
ma_2=80

start=dt.datetime.now()-dt.timedelta(days=365*3)
end=dt.datetime.now()

data = web.DataReader(name="TSLA", data_source="stooq", start=start, end=end)

data[f'SMA_{ma_1}']=data['Close'].rolling(window=ma_1).mean()
data[f'SMA_{ma_2}']=data['Close'].rolling(window=ma_2).mean()

# first columns will be obvisouly NaN
# delete first ma_2 rows since ma_2>ma_1
data=data.iloc[ma_2:]
print(data)


buy_signals=[]
sell_signals=[]
trigger=0

for x in range(len(data)):    
    if data[[f'SMA_{ma_1}']].iloc[x].values <= data[[f'SMA_{ma_2}']].iloc[x].values and trigger!=1:
        buy_signals.append(data['Close'].iloc[x])
        sell_signals.append(float('nan'))
        trigger=1 
    elif data[[f'SMA_{ma_1}']].iloc[x].values >= data[[f'SMA_{ma_2}']].iloc[x].values and trigger!=-1:
        sell_signals.append(data['Close'].iloc[x])
        buy_signals.append(float('nan'))
        trigger=-1
    else:
        buy_signals.append(float('nan'))
        sell_signals.append(float('nan'))
data['Buy Signals']=buy_signals
data['Sell Signals']=sell_signals

print(data)

plt.figure(figsize=(12,6))
plt.plot(data['Close'], label='share price', alpha=0.6, color='lightgray')
plt.plot(data[f'SMA_{ma_1}'], label=f'MA {ma_1}' ,color='orange', linestyle='--')
plt.plot(data[f'SMA_{ma_2}'], label=f'MA {ma_2}' ,color='blue',  linestyle='--')
plt.scatter(data.index, data['Buy Signals'], label='Buy', marker='^', color='green', lw=1)
plt.scatter(data.index, data['Sell Signals'], label='Sell', marker='^', color='red', lw=1)
plt.legend(loc='upper left')
plt.savefig('figure.jpg')
plt.show()