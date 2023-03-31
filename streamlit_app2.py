import preprocessing
import model_predict
#import user_crawer
# import db
import request_craw
import logging
import util_log
import streamlit as st
import pandas as pd

util_log.LoggerFactory.create_logger()#로그 작동

st.balloons()

st.title('나의 _:blue[롤 티어]_ 예측하기 :sunglasses:')

with st.form("my_form"):
   text_val = st.text_input('롤 닉네임을 입력하시오', ' ')

   # Every form must have a submit button.
   submitted = st.form_submit_button("submit")
   
tab1, tab2= st.tabs(["수치데이터", "나의 롤티어"])

# Submit버튼 클릭시 your.gg에서 크롤링 시작
if submitted:
   with tab1:
      st.write("your.gg에서", text_val, "데이터를 가져오는 중입니다.")
      
      # 크롤링 시작
      cwar = request_craw.craw()
      data = cwar.craw_data(text_val)
      try:
          current_season = data[26]
      
      # 크롤링 데이터 숫자형, 문자형 전처리 된 data
          tier_mean_data = preprocessing.tier_mean()
          db_mean_data = tier_mean_data.tier_metric(data)
          user_mean_data = tier_mean_data.tier_metric_df(data)
      
      
          col1, col2, col3, col4, col5 = st.columns(5)
          col6, col7, col8, col9, col10 = st.columns(5)
          col11, col12, col13, col14, col15 = st.columns(5)
          col16, col17, col18, col19, col20 = st.columns(5)
          col21, col22, col23, col24, col25 = st.columns(5)
        
          col1.metric(label="인분", value=db_mean_data.iloc[0,1], delta=round(user_mean_data.iloc[0,4]-db_mean_data.iloc[0,1],2))
          col2.metric(label="KDA", value=db_mean_data.iloc[0,2], delta=round(user_mean_data.iloc[0,5]-db_mean_data.iloc[0,2],2))
          col3.metric(label="라인전", value=db_mean_data.iloc[0,3], delta=round(user_mean_data.iloc[0,6]-db_mean_data.iloc[0,3],2))
          col4.metric(label="캐리력", value=db_mean_data.iloc[0,4], delta=user_mean_data.iloc[0,7], delta_color="off")
          col5.metric(label="팀운", value=db_mean_data.iloc[0,5], delta=user_mean_data.iloc[0,8], delta_color="off")
          col6.metric(label="분당 CS", value=db_mean_data.iloc[0,6], delta=round(user_mean_data.iloc[0,9]-db_mean_data.iloc[0,6],2))
          col7.metric(label="분당 골드", value=db_mean_data.iloc[0,7], delta=round(user_mean_data.iloc[0,10]-db_mean_data.iloc[0,7],2))
          col8.metric(label="15분 CS 차이", value=db_mean_data.iloc[0,8], delta=round(user_mean_data.iloc[0,11]-db_mean_data.iloc[0,8],2))
          col9.metric(label="15분 골드 차이", value=db_mean_data.iloc[0,9], delta=round(user_mean_data.iloc[0,12]-db_mean_data.iloc[0,9],2))
          col10.metric(label="15분 레벨 차이", value=db_mean_data.iloc[0,10], delta=round(user_mean_data.iloc[0,13]-db_mean_data.iloc[0,10],2))
          col11.metric(label="킬", value=db_mean_data.iloc[0,11], delta=round(user_mean_data.iloc[0,14]-db_mean_data.iloc[0,11],2))
          col12.metric(label="어시스트", value=db_mean_data.iloc[0,12], delta=round(user_mean_data.iloc[0,15]-db_mean_data.iloc[0,12],2))
          col13.metric(label="데스", value=db_mean_data.iloc[0,13], delta=round(db_mean_data.iloc[0,13]-user_mean_data.iloc[0,16],2), delta_color="inverse")
          col14.metric(label="솔로킬", value=db_mean_data.iloc[0,14], delta=round(user_mean_data.iloc[0,17]-db_mean_data.iloc[0,14],2))
          col15.metric(label="솔로킬 허용", value=db_mean_data.iloc[0,15], delta=round(db_mean_data.iloc[0,15]-user_mean_data.iloc[0,18],2), delta_color="inverse")
          col16.metric(label="분당 딜량", value=db_mean_data.iloc[0,16], delta=user_mean_data.iloc[0,19], delta_color="off")
          col17.metric(label="골드당 딜량", value=db_mean_data.iloc[0,17], delta=user_mean_data.iloc[0,20], delta_color="off")
          col18.metric(label="데스당 딜량", value=db_mean_data.iloc[0,18], delta=user_mean_data.iloc[0,21], delta_color="off")
          col19.metric(label="15분 킬 관여율", value=db_mean_data.iloc[0,19], delta=user_mean_data.iloc[0,22], delta_color="off")
          col20.metric(label="킬 관여율", value=db_mean_data.iloc[0,20], delta=user_mean_data.iloc[0,23], delta_color="off")
          col21.metric(label="시야 점수", value=db_mean_data.iloc[0,21], delta=round(user_mean_data.iloc[0,24]-db_mean_data.iloc[0,21],2))
          col22.metric(label="제어 와드", value=db_mean_data.iloc[0,22], delta=round(user_mean_data.iloc[0,25]-db_mean_data.iloc[0,22],2))
          util_log.LoggerFactory._LOGGER.info('User: {} 1번 Tab 정상진행'.format(text_val))
      except:
          st.error('This is an error -> 소환사명이 없습니다!', icon="🚨")
          util_log.LoggerFactory._LOGGER.info('User: {} 1번 Tab 비정상진행'.format(text_val))
          
   with tab2:
       try:
           data_pre = preprocessing.pre(data)
           pre_data = data_pre.data()
           model1 = model_predict.model()
      
           st.write("나의 롤티어 -> :trophy:",current_season,":trophy:")
           st.write("머신러닝 모델이 예측한 나의 롤티어 -> :trophy:",model1.tier(pre_data),":trophy:")
           util_log.LoggerFactory._LOGGER.info('User: {} 2번 Tab 정상진행'.format(text_val))
       except:
           st.error('This is an error -> 소환사명이 없습니다!', icon="🚨")
           util_log.LoggerFactory._LOGGER.info('User: {} 2번 Tab 비정상진행'.format(text_val))

