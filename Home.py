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
from PIL import Image

# 한글 폰트 경로 설정
plt.rcParams['font.family'] ='Malgun Gothic'
# 메인 화면 넓게 쓰기

# st.pyplot() 오류 메시지 무시
st.set_option('deprecation.showPyplotGlobalUse', False)

 
# 프로젝트 이름
st.title("신재생에너지 대시보드")

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        #st.image("img3.jpg", width=300)
        if st.button("프로젝트 소개",type='primary'):
            st.switch_page("pages/About.py")
    with col2:
        #st.image("img1.jpeg", width=300)
        if st.button("전체 신재생에너지 발전량",type='primary'):
            st.switch_page("pages/TotalEnergy.py")
    with col3:
        #st.image('img2.jpg', width=300)
        if st.button("발전소 위치 및 시간대별 발전량",type='primary'):
            st.switch_page("pages/Regional.py")