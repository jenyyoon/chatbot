# Google Gemini 챗봇 웹 애플리케이션

Google Gemini API를 사용하는 Streamlit 기반 챗봇 애플리케이션입니다.

## 🚀 시작하기

### 1. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. API 키 설정

`.env` 파일에 Google Gemini API 키를 설정하세요:

```
GOOGLE_API_KEY=your_api_key_here
```

### 3. 애플리케이션 실행

```bash
streamlit run chatbot.py
```

브라우저가 자동으로 열리며 챗봇을 사용할 수 있습니다.

## 📋 주요 기능

- 🤖 Google Gemini Pro 모델 사용
- 💬 실시간 대화 인터페이스
- 🕐 대화 타임스탬프 표시
- 🗑️ 대화 기록 초기화 기능
- 📱 반응형 웹 디자인

## 📁 파일 구조

```
앱프로그래밍/
├── chatbot.py          # 메인 챗봇 애플리케이션
├── .env                # API 키 (Git에 포함되지 않음)
├── .gitignore          # Git 제외 파일 목록
└── requirements.txt    # 필요한 패키지 목록
```

## ⚙️ 사용 방법

1. 입력창에 메시지를 입력합니다
2. Enter 키를 누르거나 '전송' 버튼을 클릭합니다
3. AI가 응답을 생성합니다
4. 사이드바에서 대화 기록을 지울 수 있습니다

## 🔒 보안

- `.env` 파일은 `.gitignore`에 포함되어 있어 Git에 올라가지 않습니다
- API 키를 절대 공유하거나 커밋하지 마세요

