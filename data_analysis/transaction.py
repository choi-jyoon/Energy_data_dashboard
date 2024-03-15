import pandas as pd
import matplotlib as mlt
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from streamlit_option_menu import option_menu
from geopy.geocoders import Nominatim
import streamlit_folium as st_folium
import folium
import googlemaps
import re
import numpy
from datetime import datetime

# 거래량 데이터 기간 포맷팅
df_energy_transaction = get_transaction_data()
df_energy_transaction['기간'] = df_energy_transaction['기간'].dt.strftime('%Y-%m')

# 에너지원별 거래량 평균
energy_transaction_mean = df_energy_transaction.mean(skipna=True)

df_energy_mean = energy_transaction_mean.reset_index()
df_energy_mean.columns = ['에너지원', '평균']

# 월별 전체 거래량 합계
month_mean = df_energy_transaction[['기간']]
month_mean['합계'] = df_energy_transaction.drop('기간', axis=1).sum(axis=1)

# 전체 거래량 연도별 추이 그래프
month_mean['연도'] = month_mean['기간'].str[:4]
yearly_mean = month_mean.groupby('연도')['합계'].mean().reset_index()
yearly_mean['연도별 평균'] = yearly_mean['합계'].round(0)
del yearly_mean['합계']  # 중복되는 '합계' 열을 삭제합니다.


def draw_yearly_mean_graph(yearly_mean):
    fig, ax = plt.subplots(figsize=(10, 3.25))
    ax.set_facecolor('lightgray')
    fig.patch.set_facecolor('lightgray') 
    ax.bar(yearly_mean['연도'], yearly_mean['연도별 평균'], color='skyblue')
    ax.set_title('연도별 평균 거래량 추이', color='white')
    ax.set_xlabel('연도', color ='white')
    ax.set_ylabel('연도별 평균 거래량 (MWh)', color='white')
    plt.xticks(rotation=45)  # x축 레이블 회전
    plt.grid(axis='y', color='gray')
    plt.tight_layout()
    st.pyplot(fig)

def draw_monthly_total_graph(month_mean):
    fig, ax = plt.subplots(figsize=(30, 6))
    ax.set_facecolor('lightgray')  
    fig.patch.set_facecolor('lightgray') 
    ax.plot(month_mean['기간'], month_mean['합계'], marker='o', linestyle='-', color='b')
    ax.set_title('월별 전체 전력 거래량 (단위: MWh)', color='white')
    ax.set_xlabel('기간', color='white')
    ax.set_ylabel('월별 전체 거래량', color='white')
    plt.grid(True)
    plt.xticks(rotation=45)  # x축 레이블 회전
    plt.tight_layout()
    st.pyplot(fig)
# 에너지원 파이 차트 

def energy_pie():
  fig, ax = plt.subplots(figsize=(10, 6))
  fig.patch.set_alpha(0)
  ax.patch.set_alpha(0)
  
  # 파이 차트 그리기
  wedges, texts, autotexts = ax.pie(df_energy_mean['평균'], labels=df_energy_mean['에너지원'],
                                    autopct='%1.1f%%', shadow=False, startangle=90)
  
  # 레이블과 autopct의 글자 색 변경
  for text in texts:
      text.set_color('white')
  for autotext in autotexts:
      autotext.set_color('white')
      
  ax.axis('equal')
  plt.title('에너지원별 발전량 분포', color='white')
  st.pyplot(fig)

with st.container():
  col1, col2 = st.columns([1,2])
  with col1:
    energy_pie()
  with col2:
    draw_yearly_mean_graph(yearly_mean)
    
  draw_monthly_total_graph(month_mean)