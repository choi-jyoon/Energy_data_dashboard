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
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('google_api_key')
g_map = googlemaps.Client(key = API_KEY)

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


energy_map = get_map()

# df_dongseo_location 데이터프레임을 순회하면서 '위도', '경도', '발전기명' 정보를 이용해 마커를 추가하는 코드
for row in df_dongseo_location.itertuples():

    marker_map(energy_map, row.위도, row.경도, row.발전기명, color='red')

for row in df_west_location.itertuples():
    # 위도나 경도가 None이거나 NaN인 경우, 해당 행을 건너뜁니다.
    if pd.isna(row.위도) or pd.isna(row.경도):
        continue
    marker_map(energy_map, row.위도, row.경도, row.발전기명, color='blue')
    
for row in df_middle_location.itertuples():
    marker_map(energy_map, row.위도, row.경도, row.발전기명, color='green')
    
st_map  = st_folium.st_folium(energy_map, width=600, height=700)