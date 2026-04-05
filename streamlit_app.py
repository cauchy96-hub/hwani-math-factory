import streamlit as st
import google.generativeai as genai
from PIL import Image as PILImage
import io

# 1. 페이지 설정 (가장 위에 와야 함)
st.set_page_config(page_title="화니쌤의 AI 수학 공장", page_icon="🏭")

# 2. API 키 설정
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# 3. 사이드바에서 비밀번호 입력 받기
st.sidebar.title("🔒 관리자 인증")
user_password = st.sidebar.text_input("비밀번호를 입력하세요", type="password")

# --- 비밀번호 체크 시작 ---
if user_password == "0911": 
    st.markdown('<h1 style="text-align: center;">🏭 화니쌤의 AI 수학 공장</h1>', unsafe_allow_html=True)
    st.write("우리 학생들을 위한 맞춤 문제 생성기입니다.")
    
    # 모델 설정 (최신 버전인 2.0-flash 권장, 2.5는 아직 지원 여부 확인 필요)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 4. 파일 업로드
    uploaded_file = st.file_uploader("📸 분석할 문제 사진을 올려주세요", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        img = PILImage.open(io.BytesIO(image_bytes))
        
        st.image(img, caption="업로드된 문제", use_container_width=True)
        
        if st.button("🔍 화니쌤, 문제 분석 시작!"):
            with st.spinner("화니쌤이 꼼꼼하게 분석 중... 잠시만 기다려!"):
                prompt = """당신은 대한민국 최고의 수학 교사 '화니쌤'입니다. 
                이미지를 분석하여 다음 4단계를 수행하세요. 
                [규칙] 1. 텍스트 중복 금지. 2. 모든 수식은 반드시 LaTeX($...$ 또는 $$...$$)를 사용하세요.
                
                ### 1단계: 핵심 개념 요약
                ### 2단계: 쌍둥이 유형 문제 (비슷한 숫자 변형)
                ### 3단계: 변형 유형 문제 (심화/응용)
                ### 4단계: 상세 풀이 및 정답"""
                
                try:
                    # 이미지와 프롬프트를 함께 전달
                    response = model.generate_content([prompt, img])
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"아이구, 에러가 났네: {e}")

    st.markdown("---")
    st.caption("화니쌤의 AI 수학 공장 v1.1 | 제작: 제이미")

# 비밀번호가 틀렸을 때 보여줄 화면
else:
    st.title("접근 제한 🚫")
    st.info("비밀번호를 입력해야 화니쌤의 AI 수학 공장이 가동됩니다.")
    st.stop()