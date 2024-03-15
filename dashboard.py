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


# 한글 폰트 경로 설정
plt.rcParams['font.family'] ='Malgun Gothic'
# 메인 화면 넓게 쓰기
st.set_page_config(layout="wide")
# st.pyplot() 오류 메시지 무시
st.set_option('deprecation.showPyplotGlobalUse', False)


# 사이드 바 구성
with st.sidebar:
  selected = option_menu(
    menu_title = "Main Menu",
    options = ["Home","Dashboard","About"],
    icons = ["house","book","envelope"],
    menu_icon = "cast",
    default_index = 0,

  )
  
# 프로젝트 이름
st.title("신재생에너지 대시보드")

# 전력 거래량 데이터 가져오기
@st.cache_data
def get_transaction_data():
    df = pd.read_excel('dataset/한국전력거래소_신재생에너지 전력거래량_20211201.xlsx')
    return df
        
# 동서발전 데이터 가져오기
@st.cache_data
def get_daily_dongseo_data():
    
    dongseo = pd.read_excel('dataset/한국동서발전(주)_신재생설비 발전량_20230731.xlsx')
    return dongseo

# 서부발전 데이터 가져오기
@st.cache_data
def get_daily_west_data():
    
    west = pd.read_excel('dataset/한국서부발전_신재생에너지발전량.xlsx')
    return west

# 중부발전 데이터 가져오기
@st.cache_data
def get_daily_middle_data():
    
    middle = pd.read_excel('dataset/한국중부발전_신재생발전량.xlsx')
    return middle


col1, col2, col3 = st.columns(3)
with col1:
  with st.container(height=300):
    if st.button("Home"):
        st.switch_page("your_app.py")
with col2:
  with st.container(height=300):
    if st.button("dashboard"):
        st.switch_page("generation.py")
with col3:
  with st.container(height=300):
    if st.button("dashboard2"):
        st.switch_page("transaction.py")
  

    