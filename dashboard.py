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
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('google_api_key')
g_map = googlemaps.Client(key = API_KEY)

# 한글 폰트 경로 설정
plt.rcParams['font.family'] ='Malgun Gothic'

with st.sidebar:
  selected = option_menu(
    menu_title = "Main Menu",
    options = ["Home","Dashboard","About"],
    icons = ["house","book","envelope"],
    menu_icon = "cast",
    default_index = 0,

  )
st.title("신재생에너지 대시보드")

# 데이터 가져오기
@st.cache_data
def get_transaction_data():
    df = pd.read_excel('dataset/한국전력거래소_신재생에너지 전력거래량_20211201.xlsx')
    # df
    col1, col2 = st.columns(2)
    with col1:
        # 데이터 정제
        selected_columns = ['기간', '(신에너지)연료전지','(신에너지)석탄가스화']
        df_selected = df[selected_columns]
        df_selected[:5]
    # 데이터 분석
    with col2:
        # 데이터 개수 확인
        lounge_count = df.shape[0]
        st.metric(label="데이터 갯수", value="{} 개".format(lounge_count))
        
@st.cache_data
def get_daily_dongseo_data():
    dongseo = pd.read_excel('dataset/한국동서발전(주)_신재생설비 발전량_20230731.xlsx')

    return dongseo

@st.cache_data
def get_daily_west_data():
    west = pd.read_excel('dataset/한국서부발전_신재생에너지발전량.xlsx')

    return west

@st.cache_data
def get_daily_middle_data():
    middle = pd.read_excel('dataset/한국중부발전_신재생발전량.xlsx')
    
    return middle

def get_address_re(df):
    # 정규표현식 패턴
    pattern = r'(보령|서울|서천|여수|인천|제주|세종)'
    
    # 지정된 칼럼에 대해 정규표현식 적용하여 주소 추출
    df['주소'] = df['발전기명'].str.extract(pattern)
    
    return df

def get_locaation(address):
    loaction = g_map.geocode(address, language='ko')
    latitude = loaction[0]["geometry"]["location"]["lat"]
    longitude = loaction[0]["geometry"]["location"]["lng"]
    return [latitude, longitude]



df_dongseo = get_daily_dongseo_data()
df_west = get_daily_west_data()
df_middle = get_daily_middle_data()


df_west_location = df_west['주소지'].drop_duplicates()
df_west_location

df_middle_location = get_address_re(df_middle)
df_middle_location = df_middle['주소'].drop_duplicates()
df_middle_location

df_dongseo_location = df_dongseo['위치'].drop_duplicates()
df_dongseo_location

get_transaction_data()       


    
loactions = [get_locaation(address) for address in df_dongseo_location]
loactions

def get_map():
    default_map = folium.Map(location=[36.194012, 127.5019596], zoom_start=7, scrollWheelZoom=True )
    
    
# get_daily_data()
# # 위치별 라운지 개수 확인
# lounge_count_by_location = df['구분'].value_counts()
# lounge_count_by_location
# # 그래프 그리기

# # Streamlit 애플리케이션 구현
# st.bar_chart(lounge_count_by_location,
#              height=400,
#              width=600,
#              use_container_width=False)
