import streamlit as st
import google.generativeai as genai
from PIL import Image as PILImage  # 이름을 PILImage로 바꿔서 충돌 방지!
import io

# 1. 페이지 설정
st.set_page_config(page_title="화니쌤의 AI 수학 공장", page_icon="🏭")

st.markdown('<h1 style="text-align: center;">🏭 화니쌤의 AI 수학 공장</h1>', unsafe_allow_html=True)

# 2. API 키 설정 (오빠 키 그대로!)
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. 파일 업로드
uploaded_file = st.file_uploader("📸 분석할 문제 사진을 올려주세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 에러 방지를 위해 BytesIO로 확실하게 읽기
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
                # 제미나이에게 분석 요청
                response = model.generate_content([prompt, img])
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"아이구, 에러가 났네: {e}")

st.markdown("---")
st.caption("화니쌤의 AI 수학 공장 v1.1 | 제작: 제이미")