import streamlit as st
import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="Gemini 챗봇",
    page_icon="🤖",
    layout="wide"
)

# .env 파일에서 API 키 불러오기
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

# Gemini API 엔드포인트
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []

# API 키 확인
if not api_key:
    st.error("⚠️ .env 파일에서 GOOGLE_API_KEY를 찾을 수 없습니다.")
    st.info("💡 .env 파일을 확인하고 API 키를 설정해주세요.")
    st.stop()

# 타이틀 및 설명
st.title("🤖 Google Gemini 챗봇")
st.markdown("---")
st.markdown("💬 Google Gemini AI와 대화해보세요!")

# 사이드바에 정보 표시
with st.sidebar:
    st.header("ℹ️ 정보")
    st.markdown("**모델**: Gemini 2.5 Flash")
    st.markdown("**API**: REST API 직접 호출")
    st.markdown("---")
    
    if st.button("🗑️ 대화 기록 지우기"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 사용 방법")
    st.markdown("1. 아래 입력창에 메시지를 입력하세요")
    st.markdown("2. Enter 키를 누르거나 '전송' 버튼을 클릭하세요")
    st.markdown("3. AI가 응답을 생성합니다")

# 대화 기록 표시
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        timestamp = message.get("timestamp", "")
        
        if role == "user":
            with st.chat_message("user"):
                st.markdown(content)
                if timestamp:
                    st.caption(f"🕐 {timestamp}")
        else:
            with st.chat_message("assistant"):
                st.markdown(content)
                if timestamp:
                    st.caption(f"🕐 {timestamp}")

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 추가
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": current_time
    })
    
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"🕐 {current_time}")
    
    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("💭 생각 중..."):
            try:
                # 대화 기록을 API 형식으로 변환
                contents = []
                for msg in st.session_state.messages[:-1]:  # 현재 메시지 제외
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append({
                        "role": role,
                        "parts": [{"text": msg["content"]}]
                    })
                
                # 현재 사용자 메시지 추가
                contents.append({
                    "role": "user",
                    "parts": [{"text": prompt}]
                })
                
                # API 요청 데이터 구성
                request_data = {
                    "contents": contents,
                    "generationConfig": {
                        "temperature": 0.7,
                        "topP": 0.8,
                        "topK": 40,
                        "maxOutputTokens": 2048,
                    }
                }
                
                # Gemini API REST 호출
                api_url = f"{GEMINI_API_URL}?key={api_key}"
                headers = {
                    "Content-Type": "application/json"
                }
                
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=request_data,
                    timeout=30
                )
                
                # 응답 확인
                response.raise_for_status()
                response_json = response.json()
                
                # 응답 텍스트 추출
                if "candidates" in response_json and len(response_json["candidates"]) > 0:
                    candidate = response_json["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        response_text = candidate["content"]["parts"][0]["text"]
                    else:
                        raise Exception("응답 형식이 올바르지 않습니다.")
                else:
                    raise Exception("응답에 candidates가 없습니다.")
                
                # 응답 표시
                st.markdown(response_text)
                st.caption(f"🕐 {current_time}")
                
                # AI 응답을 세션 상태에 추가
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": current_time
                })
                
            except requests.exceptions.RequestException as e:
                error_msg = f"❌ API 요청 오류: {str(e)}"
                if hasattr(e.response, 'text'):
                    error_msg += f"\n상세: {e.response.text}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": current_time
                })
            except Exception as e:
                error_msg = f"❌ 오류가 발생했습니다: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": current_time
                })

# 하단 정보
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <small>Powered by Google Gemini AI | Streamlit</small>
    </div>
    """,
    unsafe_allow_html=True
)

