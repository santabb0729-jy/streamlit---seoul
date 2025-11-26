import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime

st.title('My First Streamlit App💞')

# 메인 탭 생성
main_tab, chat_tab = st.tabs(["📊 데이터 시각화", "💬 챗봇"])

# 데이터 시각화 탭
with main_tab:
    st.write("Here's our first attempt at using data to create a table:")
    st.write(pd.DataFrame({
        'first column' : [1, 2, 3, 4],
        'second column' : [10, 20, 30, 40]
    }))  

    st.write("Streamlit supports a wide range of data visualizations, including [Plotly, Altair, and Bokeh charts](https://docs.streamlit.io/develop/api-reference/charts). 📊 And with over 20 input widgets, you can easily make your data interactive!")

    all_users = ["Alice", "ELVIN👑", "JOIE✿","JIYOON"]
    with st.container(border=True):
        users = st.multiselect("Users", all_users, default=all_users)
        rolling_average = st.toggle("Rolling average")

    np.random.seed(42)
    data = pd.DataFrame(np.random.randn(20, len(users)), columns=users)
    if rolling_average:
        data = data.rolling(7).mean().dropna()

    tab1, tab2 = st.tabs(["Chart", "Dataframe"])
    tab1.line_chart(data, height=250)
    tab2.dataframe(data, height=250, use_container_width=True)

# 챗봇 탭
with chat_tab:
    st.header("💬 챗봇과 대화하기")
    
    # 채팅 기록 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # 환영 메시지 추가
        st.session_state.messages.append({
            "role": "assistant",
            "content": "안녕하세요! 저는 챗봇입니다. 무엇을 도와드릴까요? 😊"
        })
    
    # 챗봇 응답 함수
    def get_bot_response(user_message):
        user_message_lower = user_message.lower()
        
        # 인사말
        if any(word in user_message_lower for word in ["안녕", "하이", "hello", "hi", "반가워"]):
            responses = [
                "안녕하세요! 반갑습니다! 😊",
                "안녕하세요! 무엇을 도와드릴까요?",
                "하이! 오늘 하루는 어떠세요? 😄"
            ]
            return random.choice(responses)
        
        # 질문
        elif any(word in user_message_lower for word in ["이름", "누구", "who", "what"]):
            return "저는 Streamlit 챗봇입니다! 여러분의 친구가 되어드리겠습니다. 🤖"
        
        # 도움말
        elif any(word in user_message_lower for word in ["도움", "help", "도와", "어떻게"]):
            return "저는 여러분의 질문에 답변하고 대화를 나눌 수 있습니다. 자유롭게 말씀해주세요! 💬"
        
        # 감사 인사
        elif any(word in user_message_lower for word in ["고마워", "감사", "thank", "thanks"]):
            responses = [
                "천만에요! 언제든지 도와드릴게요! 😊",
                "별 말씀을요! 도움이 되어서 기쁩니다! 😄",
                "감사 인사 고마워요! 더 도와드릴게 있으면 말씀해주세요! 💕"
            ]
            return random.choice(responses)
        
        # 시간
        elif any(word in user_message_lower for word in ["시간", "time", "몇 시"]):
            current_time = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
            return f"현재 시간은 {current_time}입니다! ⏰"
        
        # 날씨 (간단한 응답)
        elif any(word in user_message_lower for word in ["날씨", "weather"]):
            return "죄송하지만 저는 실시간 날씨 정보를 제공할 수 없어요. 날씨 앱을 확인해주세요! ☀️"
        
        # 기본 응답
        else:
            responses = [
                "흥미로운 말이네요! 더 자세히 설명해주실 수 있나요? 🤔",
                "그렇군요! 다른 질문도 해주세요! 💭",
                "알겠습니다! 다른 도움이 필요하시면 언제든지 말씀해주세요! 😊",
                "좋은 질문이에요! 더 구체적으로 말씀해주시면 더 잘 도와드릴 수 있어요! 💡"
            ]
            return random.choice(responses)
    
    # 채팅 기록 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # 챗봇 응답 생성
        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
    
    # 채팅 기록 초기화 버튼
    if st.button("🗑️ 대화 기록 지우기"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "대화 기록이 초기화되었습니다. 새로운 대화를 시작해볼까요? 😊"
            }
        ]
        st.rerun()
