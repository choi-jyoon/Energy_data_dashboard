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

st.set_page_config(layout="wide")

         
# 전력 거래량 데이터 가져오기
@st.cache_data
def get_transaction_data():
    df = pd.read_excel('dataset/한국전력거래소_신재생에너지 전력거래량_20211201.xlsx')
    return df
        

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
    # ax.set_facecolor('lightgray')
    # fig.patch.set_facecolor('lightgray') 
    ax.bar(yearly_mean['연도'], yearly_mean['연도별 평균'], color='skyblue')
    ax.set_title('연도별 평균 거래량 추이')
    ax.set_xlabel('연도')
    ax.set_ylabel('연도별 평균 거래량 (MWh)')
    plt.xticks(rotation=45)  # x축 레이블 회전
    plt.grid(axis='y')
    plt.tight_layout()
    st.pyplot(fig)

def draw_monthly_total_graph(month_mean):
    fig, ax = plt.subplots(figsize=(30, 6))
    # ax.set_facecolor('lightgray')  
    # fig.patch.set_facecolor('lightgray') 
    ax.plot(month_mean['기간'], month_mean['합계'], marker='o', linestyle='-', color='b')
    ax.set_title('월별 전체 전력 거래량 (단위: MWh)')
    ax.set_xlabel('기간')
    ax.set_ylabel('월별 전체 거래량')
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
  
  # # 레이블과 autopct의 글자 색 변경
  # for text in texts:
  #     text.set_color('white')
  # for autotext in autotexts:
  #     autotext.set_color('white')
      
  ax.axis('equal')
  plt.title('에너지원별 발전량 분포')
  st.pyplot(fig)

st.subheader('에너지원 종류별 파이 및 전체 전력 거래량 추이')
with st.container():
  col1, col2 = st.columns([1,2])
  with col1:
    energy_pie()
  with col2:
    draw_yearly_mean_graph(yearly_mean)
    
  draw_monthly_total_graph(month_mean)
  
df_energy_transaction['기간'] = pd.to_datetime(df_energy_transaction['기간'])
df_energy_transaction['연도']= df_energy_transaction['기간'].dt.year
df_year = {year: group for year, group in df_energy_transaction.groupby('연도')}

st.subheader('연도별 전체 거래량 자세히 들여보기')
  # 연도 선택을 위한 selectbox 생성
year = st.selectbox(
    "연도를 선택하세요.",
    options=[2017, 2018, 2019, 2020, 2021]
)

# 선택된 연도를 표시
st.write(f"선택된 연도: {year}")

def energy_amount(year):
  df_year[year] = df_year[year].iloc[:, :-1]
  values = df_year[year].mean()
  values_int = values.map(int)
  values_int

def year_energy(year):
  categories = df_energy_mean['에너지원']
  values = df_year[year].mean()
  values_int = values.map(int)
  fig, ax = plt.subplots(figsize=(10, 6))
  ax.bar(categories, values, color='skyblue')

  # 그래프에 값 표시
  for i, value in enumerate(values):
      ax.text(i, value, f'{value:.2f}', ha='center', va='bottom')

  # 그래프의 제목과 축 이름을 설정
  ax.set_title(f'에너지원별 발전량 ({year})')
  ax.set_xlabel('에너지원')
  ax.set_ylabel('발전량 (단위: MWh)')
  plt.xticks(rotation=45)

  # Streamlit을 통해 그래프 출력
  st.pyplot(fig)

st.write('\n'*5)
with st.container():
  col3, col4 = st.columns([0.4, 0.6])
  with col3:
    energy_amount(year)
  with col4:
    year_energy(year)