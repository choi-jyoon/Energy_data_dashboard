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
from pages import about, generation, transaction

# 한글 폰트 경로 설정
plt.rcParams['font.family'] ='Malgun Gothic'
# 메인 화면 넓게 쓰기
st.set_page_config(layout="wide")
# st.pyplot() 오류 메시지 무시
st.set_option('deprecation.showPyplotGlobalUse', False)

 
# 프로젝트 이름
st.title("신재생에너지 대시보드")


# 사이드바에 동일한 버튼 구성
with st.sidebar:
    with st.container():
        if st.button("프로젝트 소개"):
            st.switch_page("pages/about.py")
        if st.button("발전소 위치 및 시간대별 발전량"):
            st.switch_page("pages/generation.py")
        if st.button("전체 신재생에너지 발전량"):
            st.switch_page("pages/transaction.py")