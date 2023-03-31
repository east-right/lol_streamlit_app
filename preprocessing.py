import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from pickle import load
import re
import json

# 데이터 전처리 코드
class pre:
    def __init__(self, data):
        #딕셔너리 파일 불러오기
        with open('pre_label.json', 'r') as f: #ver2 에선 pre_label.json
            self.dic = json.load(f)
            
        # colum은 전체 컬럼
        self.colum =['user_id','last_season_tier','main_position','num_games','servings','kda','line_war','carry_power',
                     'team_luck','per_minute_cs','per_minute_gold','dif_15min_cs','dif_15min_gold','dif_15min_level',
                     'total_kill','assist','death','solo_kill','allow_solo_kill','per_minute_deal','gold_deal','per_death_deal',
                     'kill_engage_15min','kill_engage','vision_score','control_ward','current_season_tier']
        
        # col은 숫자형 컬럼들
        self.col =['last_season_tier','num_games','servings','kda','line_war','carry_power','team_luck','per_minute_cs',
                   'per_minute_gold','dif_15min_cs','dif_15min_gold','dif_15min_level','total_kill','assist','death',
                   'solo_kill','allow_solo_kill','per_minute_deal','gold_deal','per_death_deal',
                   'kill_engage_15min','kill_engage','vision_score','control_ward']
        
        self.df =  pd.DataFrame(columns = self.colum)
        self.df.loc[0] = data
        
        #티어 라벨링
        def tier_label(d):
            tier = self.dic['tier_label'][re.sub('[^a-zA-z]','',d)]
            try:
                num = 5 - int(re.sub('\D','', d))
            except ValueError:
                num = 0
            value = tier + num
            return value
        
        #티어 관련은 함수 사용 나머지는 딕셔너리 매칭   
        self.df['last_season_tier'] = tier_label(self.df['last_season_tier'][0])
        self.df['current_season_tier'] = tier_label(self.df['current_season_tier'][0])
        self.df['carry_power'] = self.dic['stat_rank'][self.df['carry_power'][0]]
        self.df['gold_deal'] = self.dic['stat_rank'][self.df['gold_deal'][0]]
        self.df['per_death_deal'] = self.dic['stat_rank'][self.df['per_death_deal'][0]]
        self.df['per_minute_deal'] = self.dic['stat_rank'][self.df['per_minute_deal'][0]]
        self.df['team_luck'] = self.dic['team_luck'][self.df['team_luck'][0]]
        self.df['main_position'] = self.df['main_position'].astype('category')
        
        # 기존 scaler 모델 불러오기
        scaler = load(open('standardscaler1.pkl','rb'))
        self.df[self.col] = scaler.transform(self.df[self.col])
        
    def data(self):
        return self.df
    
class tier_mean:
    def __init__ (self):
        self.tier_mean_col = pd.read_csv('preprocessing1.csv',index_col=0).reset_index()
        self.tier_mean_col.iloc[:,1:4] = self.tier_mean_col.iloc[:,1:4].round(2)
        self.tier_mean_col.iloc[:,6:16] = self.tier_mean_col.iloc[:,6:16].round(2)
        self.tier_mean_col.iloc[:,21:23] = self.tier_mean_col.iloc[:,21:23].round(2)
        
    # user_data는 사용자의 티어 데이터, tier_mean은 티어별 평균 데이터들이 저장된 데이터프레임
    def tier_metric(self, user_data):
        # 들어온 데이터 전처리
        user_data[26] = user_data[26].split(' ')[0].lower()
        tier_graph = self.tier_mean_col[self.tier_mean_col['index'] == user_data[26]]
        
        return tier_graph
    
    # 데이터프레임 변환
    def tier_metric_df(self, user_data):
        user_data = pd.DataFrame([user_data])

        return user_data


