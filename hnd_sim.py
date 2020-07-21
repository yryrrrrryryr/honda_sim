import random
import numpy as np
import pandas as pd

win_rate = []
msec_med = []
rank_mean = []

t_list     = []
rank_list  = []
colas_list = []
win_list   = []
wins_in_sec_list = []
colas = 0
win_prob_per_cola = 1./3   # コーラ1個当たりの当選確率

msec_per_hour = 3600*1000
t_e = 100*msec_per_hour      # シミュレーション終了時刻[ms]
attend_prob   =  5435./653.*900./3000./1000. # 1 ms ごとの参加者出現確率
cola_add_prob =   900./3000. # 1 s ごとのコーラ追加確率

for t in range(t_e):
  
  if((t%(1000*3600)==0)):
    print('hour=',t/(1000*3600))
  
  #毎秒.000ごとに
  if((t%1000)==0):
    
    #値のリセット?
    rank = 0
    wins = 0
    
    #コーラ追加の判断
    if(random.random()<=cola_add_prob):
      colas += 1
  
  #参加者の有無を判断
  if(random.random()<=attend_prob):
    #参加者がいる場合
    rank += 1

    win_prob = 1. - (1.-win_prob_per_cola)**colas
    #win_prob = 1./3. if colas>=1 else 0
    #勝敗の決定
    if(random.random()<=win_prob):
      win = 1
      wins += 1
      wins_in_sec = wins
      colas -= 1
    else:
      win = 0
      wins_in_sec = 0

    #リストへの追加
    t_list.append(t)
    rank_list.append(rank)
    colas_list.append(int(colas+win))
    win_list.append(win)
    wins_in_sec_list.append(wins_in_sec)
    
df = pd.DataFrame({'t':t_list,'rank':rank_list,'colas':colas_list,'win':win_list,'wins_in_sec':wins_in_sec_list})

#tをsecとmsecに分解
df['sec'] = df['t'].apply(lambda x: int(x/1000))
df['msec'] = df['t'].apply(lambda x: int(x%1000))

win_rate.append(df['win'].mean()*100.)
msec_med.append(df.query('win == 1')['msec'].median())
rank_mean.append(df.query('win == 1')['rank'].mean())


df_t = pd.DataFrame()
df_t['rank_max'] = df['sec'].value_counts()
df_t = df_t.reset_index()
df_t.rename(columns={'index':'sec'}, inplace=True)
df = pd.merge(df,df_t,on='sec',how='left')
df.to_csv('dataframe.csv')
print('win_rate :',np.mean(win_rate))
print('msec_med :',np.mean(msec_med))
print('rank_mean:',np.mean(rank_mean))


df_g = df.groupby('msec')['win'].mean().reset_index()
df_g.to_csv('win_rate.csv')

