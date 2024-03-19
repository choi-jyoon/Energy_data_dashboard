import streamlit as st

with st.sidebar:
    with st.container():
        if st.button("프로젝트 소개"):
            st.switch_page("pages/about.py")
        if st.button("발전소 위치 및 시간대별 발전량"):
            st.switch_page("pages/generation.py")
        if st.button("전체 신재생에너지 발전량"):
            st.switch_page("pages/transaction.py")
            
st.write('''
# Data_DashBoard

## 프로젝트 소개
### 신재생에너지 현황 대시보드 
- 배경 :
    - 전세계적으로 탄소중립 정책과 신재생에너지의 중요성이 대두되면서 국내에서도 ESG경영 트렌드에 맞춘 탄소 중립 실현 기업이 증가하고 있습니다
- 목적
    - 신재생에너지 전력거래량을 제공하고 발전소별 발전량과 이용량의 추이를 분석하여 신재생에너지 활용을 높이고자 합니다.
- 개요 :
    - 신재생에너지의 발전량과 이용량, 발전소의 위치 정보를 제공하는 데이터 대쉬보드를 구현하였습니다.
- 데이터 :
    - 신재생에너지 항목별 전력 거래량,
    - 한국서부발전 일간 발전량,
    - 한국중부발전 일간 발전량,
    - 한국동서발전 일간 발전량
- 기능
    - 지도에서 발전소 위치 정보 확인
    - 에너지원 별 전력 거래량 그래프
    - 발전소별 발전량 그래프
''')