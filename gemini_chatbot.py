import streamlit as st
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="Gemini 챗봇",
    page_icon="🤖",
    layout="centered"
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
    st.info("💡 .env 파일에 GOOGLE_API_KEY=your_api_key 형식으로 API 키를 설정해주세요.")
    st.stop()

# 헤더
st.title("🤖 Google Gemini 챗봇")
st.markdown("---")

# 사이드바
with st.sidebar:
    st.header("⚙️ 설정")
    st.markdown("**모델**: Gemini 2.5 Flash")
    
    if st.button("🗑️ 대화 기록 지우기", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 사용 방법")
    st.markdown("1. 하단 입력창에 메시지 입력")
    st.markdown("2. Enter 키 또는 전송 버튼 클릭")
    st.markdown("3. AI 응답 대기")

# 대화 기록 표시
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    
    with st.chat_message(role):
        st.markdown(content)
        if "timestamp" in message:
            st.caption(f"🕐 {message['timestamp']}")

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # 사용자 메시지 추가 및 표시
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": current_time
    })
    
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
                    role_key = "user" if msg["role"] == "user" else "model"
                    contents.append({
                        "role": role_key,
                        "parts": [{"text": msg["content"]}]
                    })
                
                # 현재 사용자 메시지 추가
                contents.append({
                    "role": "user",
                    "parts": [{"text": prompt}]
                })
                
                # API 요청
                api_url = f"{GEMINI_API_URL}?key={api_key}"
                request_data = {
                    "contents": contents,
                    "generationConfig": {
                        "temperature": 0.7,
                        "topP": 0.8,
                        "topK": 40,
                        "maxOutputTokens": 2048,
                    }
                }
                
                response = requests.post(
                    api_url,
                    headers={"Content-Type": "application/json"},
                    json=request_data,
                    timeout=30
                )
                
                response.raise_for_status()
                response_json = response.json()
                
                # 응답 추출
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
                
                # AI 응답 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": current_time
                })
                
            except requests.exceptions.RequestException as e:
                error_msg = f"❌ API 요청 오류: {str(e)}"
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_detail = e.response.json()
                        error_msg += f"\n상세: {error_detail}"
                    except:
                        error_msg += f"\n상세: {e.response.text if hasattr(e.response, 'text') else ''}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": current_time
                })
            except Exception as e:
                error_msg = f"❌ 오류 발생: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": current_time
                })

# 하단 정보
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: gray; font-size: 0.8em;">Powered by Google Gemini AI | Streamlit</div>',
    unsafe_allow_html=True
)

