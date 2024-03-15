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



# 기본 지도 그리기
def get_map():
    default_map = folium.Map(location=[36.194012, 127.5019596], zoom_start=7, scrollWheelZoom=True )
    return default_map
    
# 지도에 마커 추가하기
def marker_map(m, lat, log, text,color):
    folium.Marker([lat, log], 
                  popup=folium.Popup(text, parse_html=True),
                    icon=folium.Icon(color=color)).add_to(m)
   

# 동서, 서부, 중부 데이터 프레임 저장
df_dongseo = get_daily_dongseo_data()
df_west = get_daily_west_data()
df_middle = get_daily_middle_data()

df_dongseo['주소'] = df_dongseo['위치']
# 주소지 중복 제거하기
df_dongseo_location = df_dongseo[['발전기명', '주소']].drop_duplicates()
df_dongseo_location

df_west['주소'] = df_west['주소지']
df_west_location = df_west[['발전기명', '주소']].drop_duplicates()
df_west_location

df_middle_location = get_address_re(df_middle)
df_middle_location = df_middle_location[['발전기명', '주소']].drop_duplicates()
df_middle_location



# '위도'와 '경도' 열을 데이터프레임에 추가합니다. 초기값은 None으로 설정할 수 있습니다.
df_dongseo_location['위도'] = None
df_dongseo_location['경도'] = None

for index, row in df_dongseo_location.iterrows():
    # get_location 함수를 사용하여 위도와 경도 정보를 얻습니다.
    loc_info = get_location(row.주소)
    if loc_info:
        # loc_info가 None이 아니면, 해당 인덱스의 '위도'와 '경도' 열을 업데이트합니다.
        df_dongseo_location.at[index, '위도'] = loc_info['latitude']
        df_dongseo_location.at[index, '경도'] = loc_info['longitude']
    else:
        # 선택적: 주소를 찾을 수 없는 경우, 로그를 남깁니다.
        st.write(f"{row.주소}에 대한 결과를 찾을 수 없습니다.")
        
for index, row in df_west_location.iterrows():
    # get_location 함수를 사용하여 위도와 경도 정보를 얻습니다.
    loc_info = get_location(row.주소)
    if loc_info:
        # loc_info가 None이 아니면, 해당 인덱스의 '위도'와 '경도' 열을 업데이트합니다.
        df_west_location.at[index, '위도'] = loc_info['latitude']
        df_west_location.at[index, '경도'] = loc_info['longitude']
    else:
        # 선택적: 주소를 찾을 수 없는 경우, 로그를 남깁니다.
        st.write(f"{row.주소}에 대한 결과를 찾을 수 없습니다.")

for index, row in df_middle_location.iterrows():
    # get_location 함수를 사용하여 위도와 경도 정보를 얻습니다.
    loc_info = get_location(row.주소)
    if loc_info:
        # loc_info가 None이 아니면, 해당 인덱스의 '위도'와 '경도' 열을 업데이트합니다.
        df_middle_location.at[index, '위도'] = loc_info['latitude']
        df_middle_location.at[index, '경도'] = loc_info['longitude']
    else:
        # 선택적: 주소를 찾을 수 없는 경우, 로그를 남깁니다.
        st.write(f"{row.주소}에 대한 결과를 찾을 수 없습니다.")

df_dongseo_location
df_west_location
df_middle_location

energy_map = get_map()

# df_dongseo_location 데이터프레임을 순회하면서 '위도', '경도', '발전기명' 정보를 이용해 마커를 추가하는 코드
for row in df_dongseo_location.itertuples():

    marker_map(energy_map, row.위도, row.경도, row.발전기명, color='red')

for row in df_west_location.itertuples():
    # 위도나 경도가 None이거나 NaN인 경우, 해당 행을 건너뜁니다.
    if pd.isna(row.위도) or pd.isna(row.경도):
        continue
    
    # 위도와 경도 값이 유효한 경우에만 마커를 추가합니다.
    marker_map(energy_map, row.위도, row.경도, row.발전기명, color='blue')
    
for row in df_middle_location.itertuples():
    marker_map(energy_map, row.위도, row.경도, row.발전기명, color='green')
    
st_map  = st_folium.st_folium(energy_map, width=600, height=700)

# # get_daily_data()
# # # 위치별 라운지 개수 확인
# # lounge_count_by_location = df['구분'].value_counts()
# # lounge_count_by_location
# # # 그래프 그리기

# # # Streamlit 애플리케이션 구현
# # st.bar_chart(lounge_count_by_location,
# #              height=400,
# #              width=600,
# #              use_container_width=False)
