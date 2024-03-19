import pandas as pd
import matplotlib as mlt
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from streamlit_option_menu import option_menu
from geopy.geocoders import Nominatim
import streamlit_folium as st_folium
import folium
import googlemaps
import re
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('google_api_key')
g_map = googlemaps.Client(key = API_KEY)

st.set_page_config(layout="wide")
with st.sidebar:
    with st.container():
        if st.button("프로젝트 소개"):
            st.switch_page("pages/about.py")
        if st.button("발전소 위치 및 시간대별 발전량"):
            st.switch_page("pages/generation.py")
        if st.button("전체 신재생에너지 발전량"):
            st.switch_page("pages/transaction.py")
         
st.subheader("주요 발전소 위치 안내")
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

# 중부발전 발전기 위치 저장하기
def get_address_re(df):
    # 정규표현식 패턴
    pattern = r'(보령|서울|서천|여수|인천|제주|세종)'
    # 정규표현식 적용하여 주소 추출
    df['주소'] = df['발전기명'].str.extract(pattern)
    return df

# 주소에서 위도, 경도 추출하기 
def get_location(address):
    location = g_map.geocode(address, language='ko')
    # 결과가 비어 있는지 확인
    if not location:
        # st.write(f"{address}에 대한 결과를 찾을 수 없습니다.")
        return None

    latitude = location[0]["geometry"]["location"]["lat"]
    longitude = location[0]["geometry"]["location"]["lng"]
    return {'latitude':latitude, 'longitude':longitude}

def get_lat_lng(df):
    for index, row in df.iterrows():

        loc_info = get_location(row.주소)
        if loc_info:
            df.at[index, '위도'] = loc_info['latitude']
            df.at[index, '경도'] = loc_info['longitude']
        # else:
        #     st.write(f"{row.주소}에 대한 결과를 찾을 수 없습니다.")
    return df

# 기본 지도 그리기
def get_map():
    default_map = folium.Map(location=[36.194012, 127.5019596], zoom_start=7, scrollWheelZoom=True )
    return default_map
    
# 지도에 마커 추가하기
def marker_map(m, lat, log, text,color):
    folium.Marker([lat, log], popup=folium.Popup(text, parse_html=True, max_width = 300), icon=folium.Icon(color=color)).add_to(m)
   

# 동서, 서부, 중부 데이터 프레임 저장
df_dongseo = get_daily_dongseo_data()
df_west = get_daily_west_data()
df_middle = get_daily_middle_data()

# 주소지 중복 제거하기
df_dongseo['주소'] = df_dongseo['위치']
df_dongseo_location = df_dongseo[['발전기명', '주소']].drop_duplicates()


df_west['주소'] = df_west['주소지']
df_west_location = df_west[['발전기명', '주소']].drop_duplicates()


df_middle_location = get_address_re(df_middle)
df_middle_location = df_middle_location[['발전기명', '주소']].drop_duplicates()


# 위경도 얻기
df_dongseo_location = get_lat_lng(df_dongseo_location)
df_west_location = get_lat_lng(df_west_location)
df_middle_location = get_lat_lng(df_middle_location)

# 발전소 선택 위젯
loc = st.selectbox(
    "발전소를 선택하세요.",
    options=['전체보기', '서부발전', '동서발전', '중부발전']
)

# 지도 객체 생성
energy_map_loc = get_map()

# 지도에 마커 추가 함수
def add_markers(df, map_obj, color):
    for row in df.itertuples():
        if pd.isna(row.위도) or pd.isna(row.경도):
            continue
        marker_map(map_obj, row.위도, row.경도, row.발전기명, color=color)
        
        
def dongseo_mean():
    groupby_region = df_dongseo.groupby('발전기명')

    # Matplotlib을 이용해 그래프를 준비합니다.
    fig, ax = plt.subplots(figsize=(2,3))

    # 발전소별 평균 발전량을 저장할 리스트
    names = []
    averages = []

    for name, group in groupby_region:
        hours_data = group.iloc[:, 5:]  # '방전' 컬럼 이후의 모든 컬럼 선택
        average_production = hours_data.mean(axis=1).mean()  # 시간당 평균 발전량 계산
        names.append(name)
        averages.append(average_production)

    # 그래프 그리기
    ax.barh(names, averages, color = 'red')
    ax.set_ylabel('발전소 이름')
    ax.set_xlabel('시간당 평균 발전량 (kWh)')
    ax.set_title('발전소별 평균 발전량')
    plt.yticks(rotation=45, ha="right")

    # Streamlit을 이용해 그래프 표시
    st.pyplot(fig)
    
def west_mean_small():
    groupby_region = df_west.groupby('발전기명')

    # Matplotlib을 이용해 그래프를 준비합니다.
    fig, ax = plt.subplots(figsize=(4,6))

    threshold = 8000000
    names = []
    averages = []

    for name, group in groupby_region:
        if group['합계'].mean() < threshold and group['합계'].mean() > 2500000:
            average_production = group['합계'].mean()  # 시간당 평균 발전량 계산
            names.append(name)
            averages.append(average_production)

    # 그래프 그리기
    ax.barh(names, averages, color = 'skyblue')
    ax.set_ylabel('발전소 이름')
    ax.set_xlabel('시간당 평균 발전량 (kWh)')
    ax.set_title('발전소별 평균 발전량')
    
    # x축 눈금을 10개 단위로 조정합니다.
    ticks_positions = np.arange(0, len(names), 5)  # 10개 단위로 위치를 설정합니다.
    ticks_labels = names[::5]  # 10개 단위로 라벨을 설정합니다.
    plt.yticks(rotation=45, ha="right")

    # Streamlit을 이용해 그래프 표시
    st.pyplot(fig)
    
def west_mean():
    groupby_region = df_west.groupby('발전기명')

    # Matplotlib을 이용해 그래프를 준비합니다.
    fig, ax = plt.subplots(figsize=(4,6))

    threshold = 8000000
    names = []
    averages = []

    for name, group in groupby_region:
        if group['합계'].mean() > threshold:
            average_production = group['합계'].mean()  # 시간당 평균 발전량 계산
            names.append(name)
            averages.append(average_production)

    # 그래프 그리기
    ax.barh(names, averages, color = 'skyblue')
    ax.set_ylabel('발전소 이름')
    ax.set_xlabel('시간당 평균 발전량 (kWh)')
    ax.set_title('발전소별 평균 발전량')
    
    # x축 눈금을 10개 단위로 조정합니다.
    ticks_positions = np.arange(0, len(names), 5)  # 10개 단위로 위치를 설정합니다.
    ticks_labels = names[::5]  # 10개 단위로 라벨을 설정합니다.
    plt.yticks(rotation=45, ha="right")

    # Streamlit을 이용해 그래프 표시
    st.pyplot(fig)
    
def middle_mean():
    groupby_region = df_middle.groupby('발전기명')

    # Matplotlib을 이용해 그래프를 준비합니다.
    fig, ax = plt.subplots(figsize=(4,6))

    threshold = 10000000
    names = []
    averages = []

    for name, group in groupby_region:
        hours_data = group.iloc[:, 5:]  # '방전' 컬럼 이후의 모든 컬럼 선택
        if hours_data.mean(axis=1).mean() > threshold:
            average_production = hours_data.mean(axis=1).mean()  # 시간당 평균 발전량 계산
            names.append(name)
            averages.append(average_production)

    # 그래프 그리기 - 여기서 x, y축을 바꿉니다.
    ax.barh(names, averages, color = 'green')
    ax.set_ylabel('발전소 이름')
    ax.set_xlabel('시간당 평균 발전량 (kWh)')
    ax.set_title('발전소별 평균 발전량')
    plt.yticks(rotation=45, ha="right")

    # Streamlit을 이용해 그래프 표시
    st.pyplot(fig)

   
def middle_mean_small():
    groupby_region = df_middle.groupby('발전기명')

    # Matplotlib을 이용해 그래프를 준비합니다.
    fig, ax = plt.subplots(figsize=(4,6))

    threshold = 10000000
    names = []
    averages = []

    for name, group in groupby_region:
        hours_data = group.iloc[:, 5:]  # '방전' 컬럼 이후의 모든 컬럼 선택
        if hours_data.mean(axis=1).mean() < threshold:
            average_production = hours_data.mean(axis=1).mean()  # 시간당 평균 발전량 계산
            names.append(name)
            averages.append(average_production)

    # 그래프 그리기 - 여기서 x, y축을 바꿉니다.
    ax.barh(names, averages, color = 'green')
    ax.set_ylabel('발전소 이름')
    ax.set_xlabel('시간당 평균 발전량 (kWh)')
    ax.set_title('발전소별 평균 발전량')
    plt.yticks(rotation=45, ha="right")

    # Streamlit을 이용해 그래프 표시
    st.pyplot(fig)
    
# 사용자 선택에 따른 마커 추가
if loc == '서부발전':
    add_markers(df_west_location, energy_map_loc, 'blue')
    with st.container():
        col1, col2 = st.columns([1, 1])  # 1:1 비율로 컬럼을 나눕니다.
        with col1:
            west_mean_small()
        with col2:
            west_mean()
elif loc == '동서발전':
    # add_markers(df_dongseo_location, energy_map_loc, 'red')
    with st.container():
        col1, col2 = st.columns([1, 1])  # 1:1 비율로 컬럼을 나눕니다.
        with col1:
            dongseo_mean()
        with col2:
            add_markers(df_dongseo_location, energy_map_loc, 'red')
elif loc == '중부발전':
    add_markers(df_middle_location, energy_map_loc, 'green')
    with st.container():
        col1, col2 = st.columns([1, 1])  # 1:1 비율로 컬럼을 나눕니다.
        with col1:
            middle_mean_small()
        with col2:
            middle_mean()
else:  # '전체보기' 선택 시
    with st.container():
        col1, col2 = st.columns([1, 1])  # 1:1 비율로 컬럼을 나눕니다.
        with col1:
            add_markers(df_dongseo_location, energy_map_loc, 'red')
            add_markers(df_west_location, energy_map_loc, 'blue')
            add_markers(df_middle_location, energy_map_loc, 'green')
        with col2:
            # 여기서는 모든 발전소의 평균을 보여주는 함수를 호출할 수 있습니다.
            # 예를 들어, 전체 발전소 평균을 보여주는 함수가 있다면 여기에 넣을 수 있어요.
            pass


# 지도를 Streamlit에 표시
st_folium.st_folium(energy_map_loc, width=600, height=700)
    
# 발전소 이름을 유니크하게 가져옵니다.
unique_plants = df_dongseo['발전기명'].unique()
df_dongseo.drop('일자', axis=1)

# Streamlit에서 발전소를 선택할 수 있도록 드롭다운 메뉴를 생성합니다.
selected_plant = st.selectbox('발전소를 선택하세요:', unique_plants)

# 선택된 발전소에 대한 데이터만 필터링합니다.
filtered_data = df_dongseo[df_dongseo['발전기명'] == selected_plant]

filtered_data
