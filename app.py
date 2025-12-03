import streamlit as st
import json
import pandas as pd

# --- 1. 데이터 및 AI 시뮬레이션 함수 ---

# 11개 국왕의 정보와 가상 일기 (AI 생성 내용 시뮬레이션)
KING_DATA = {
    "태조": {
        "reign": "1392년 ~ 1398년",
        "feature": "나라의 문을 활짝 연 첫 번째 킹! 🚪",
        "achievements": ["조선 건국 (1392)", "한양 천도", "위화도 회군"],
        "diary_excerpt": "새로운 나라를 세우는 것은 참으로 힘들고 외로운 일이었다. 백성들이 편안한 세상을 꿈꾸며 이 길을 걸었다. ⛰️"
    },
    "태종": {
        "reign": "1400년 ~ 1418년",
        "feature": "강력한 힘으로 왕권을 꽉 잡은 킹! 💪",
        "achievements": ["육조 직계제 실시", "사병 혁파", "호패법 실시"],
        "diary_excerpt": "왕실의 권위를 세우기 위해 피를 묻힌 것은 숙명이었다. 강력한 군주만이 혼란을 잠재울 수 있다. 🛡️"
    },
    "세종": {
        "reign": "1418년 ~ 1450년",
        "feature": "백성을 사랑한 한글 창제 킹! ❤️",
        "achievements": ["훈민정음 창제", "측우기, 해시계 발명", "4군 6진 개척"],
        "diary_excerpt": "글자를 몰라 억울함을 호소하지 못하는 백성들을 위해 이 새로운 스물여덟 글자를 만든다. 이 글자가 온 백성의 빛이 되리라 믿는다. ☀️"
    },
    "세조": {
        "reign": "1455년 ~ 1468년",
        "feature": "강한 법으로 나라의 기강을 세운 킹! ⚔️",
        "achievements": ["계유정난 주도", "경국대전 편찬 시작", "군권 직접 장악"],
        "diary_excerpt": "흔들리는 왕실을 바로잡기 위해 내가 직접 나섰다. 경국대전을 시작하여 영원히 변치 않을 나라의 틀을 만들고 싶다. 🦅"
    },
    "성종": {
        "reign": "1469년 ~ 1494년",
        "feature": "조선의 통치 제도를 완성한 킹! 📝",
        "achievements": ["경국대전 완성 및 반포", "홍문관 설치", "유교적 통치 질서 확립"],
        "diary_excerpt": "선대왕들이 시작하신 경국대전을 마침내 완성했다. 이제 모든 신하와 백성이 지킬 바를 알게 되었으니, 아름다운 유교의 나라가 완성되었다. 📚"
    },
    "선조": {
        "reign": "1567년 ~ 1608년",
        "feature": "임진왜란의 시련을 겪은 킹! 🌊",
        "achievements": ["임진왜란 발발", "분조(分朝) 설치", "붕당 정치 시작"],
        "diary_excerpt": "왜적의 침입으로 피난길에 오르는 신세가 되었다니 통탄할 일이다. 백성들의 의병 활동에 감격했다. 아들 광해에게 짐을 나누어 수습을 맡기니 부디 잘 해내기를. 😥"
    },
    "인조": {
        "reign": "1623년 ~ 1649년",
        "feature": "인조반정으로 즉위했으나 정묘호란과 병자호란을 겪은 비운의 군주 💔",
        "achievements": ["인조반정", "친명배금 정책", "병자호란 발발 및 삼전도의 굴욕"],
        "diary_excerpt": "삼전도의 굴욕은 평생 잊지 못할 치욕이다. 나라를 지키지 못한 죄를 어찌 갚아야 할꼬. 후대 왕은 이 복수를 반드시 해내야 할 것이다. 😭"
    },
    "효종": {
        "reign": "1649년 ~ 1659년",
        "feature": "청나라 복수를 꿈꾼 북벌 킹! 🏹",
        "achievements": ["북벌 정책 추진", "군사력 강화 및 조총 부대 양성", "나선 정벌 지원"],
        "diary_excerpt": "청나라에 인질로 잡혀갔던 치욕을 잊지 않는다. 내가 힘을 기르는 것은 오직 북벌을 위해서다. 이 나라의 군사력을 최고로 만들겠다. 🐅"
    },
    "숙종": {
        "reign": "1674년 ~ 1720년",
        "feature": "신하들을 마음대로 움직인 환국 킹! 🔄",
        "achievements": ["환국 정치 (세력 교체)", "대동법 전국 확대", "백두산 정계비 건립"],
        "diary_excerpt": "신하들의 싸움이 끝이 없으니, 내가 직접 그들을 바꾸어 나라를 다스리겠다. 이 나라의 주인은 오직 왕이다! 내 뜻대로 정치를 펼치리라. 👑"
    },
    "영조": {
        "reign": "1724년 ~ 1776년",
        "feature": "가장 오래 재위하며 백성의 삶을 살핀 킹! ⚖️",
        "achievements": ["탕평책 실시", "균역법 실시", "속대전 편찬"],
        "diary_excerpt": "어느 편도 들지 않는 공평한 정치가 탕평이다. 백성들의 군포 부담을 줄여주는 균역법을 시행하니 마음이 놓인다. 만백성이 평안하게 살기를. 🕊️"
    },
    "정조": {
        "reign": "1776년 ~ 1800년",
        "feature": "개혁과 문화를 꽃피운 천재 킹! 💡",
        "achievements": ["규장각 설치", "장용영 설치", "수원 화성 건설 및 신해통공 실시"],
        "diary_excerpt": "나의 개혁 의지는 누구도 막을 수 없다! 규장각에서 인재를 키우고, 수원 화성을 지어 나의 꿈을 펼치겠다. 아버지의 뜻을 이어 만천명월주인옹(萬川明月主人翁)이 될 것이다. 🏯"
    }
}

# 퀴즈 데이터 (7문제) - JSON 형식
QUIZ_DATA_JSON = """
{
  "questions": [
    {"questionNumber": 1, "type": "multiple_choice", "question": "조선 건국의 기초가 된 가장 결정적인 사건은 무엇인가요? (태조 관련)", "answerOptions": ["홍건적 토벌", "위화도 회군", "계유정난", "무인정사", "정묘호란"], "correctAnswer": "위화도 회군", "rationale": "위화도 회군은 이성계가 군사적 실권을 장악하고 정권 교체의 길을 연 결정적인 사건입니다."},
    {"questionNumber": 2, "type": "ox", "question": "세종대왕은 강수량을 측정하는 과학 기구인 혼천의를 발명하였다. (O/X)", "answerOptions": ["O", "X"], "correctAnswer": "X", "rationale": "강수량을 측정하는 기구는 측우기이며, 혼천의는 천체의 위치를 관측하는 기구입니다."},
    {"questionNumber": 3, "type": "multiple_choice", "question": "법전 '경국대전'의 편찬을 시작하였으나 아들 성종 대에 완성된 왕은 누구인가요?", "answerOptions": ["세조", "태종", "영조", "숙종", "효종"], "correctAnswer": "세조", "rationale": "세조가 경국대전 편찬을 시작하였고, 성종 대에 완성되었습니다."},
    {"questionNumber": 4, "type": "ox", "question": "임진왜란 당시 선조는 광해군에게 분조(分朝) 활동을 맡겨 전시 상황을 수습하려 노력했다. (O/X)", "answerOptions": ["O", "X"], "correctAnswer": "O", "rationale": "선조는 비록 피난을 갔지만, 광해군에게 분조 활동을 맡겨 전쟁 수행에 노력했습니다."},
    {"questionNumber": 5, "type": "multiple_choice", "question": "탕평책을 강력하게 추진하며 백성에게 군역 부담을 줄여준 '균역법'을 시행한 왕은 누구인가요?", "answerOptions": ["숙종", "인조", "영조", "효종", "정조"], "correctAnswer": "영조", "rationale": "영조는 탕평책과 함께 균역법을 실시하여 백성들의 군포 부담을 줄여주었습니다."},
    {"questionNumber": 6, "type": "ox", "question": "숙종 대에 발생한 '환국(換局)'은 왕권을 강화하는 수단으로 작용하였다. (O/X)", "answerOptions": ["O", "X"], "correctAnswer": "O", "rationale": "환국은 왕이 인사권을 이용하여 정권을 하루아침에 교체하는 방식으로, 숙종이 왕권을 강화하는 수단으로 활용했습니다."},
    {"questionNumber": 7, "type": "multiple_choice", "question": "병자호란 이후 청나라에 대한 복수심으로 '북벌(北伐)'을 추진한 왕은 누구인가요?", "answerOptions": ["선조", "세조", "효종", "인조", "정조"], "correctAnswer": "효종", "rationale": "효종은 병자호란 때 인질로 잡혀갔던 경험을 바탕으로 즉위 후 북벌을 추진했습니다."}
  ]
}
"""
QUIZ_DATA = json.loads(QUIZ_DATA_JSON)['questions']


# --- 2. Streamlit 초기 설정 및 상태 관리 ---

st.set_page_config(
    page_title="🌈 AI 조선 왕조 도감 👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'quiz_started' not in st.session_state:
    st.session_state['quiz_started'] = False
if 'user_answers' not in st.session_state:
    st.session_state['user_answers'] = {f"q_{i}": None for i in range(len(QUIZ_DATA))} # 초기값을 None으로 설정
if 'quiz_submitted' not in st.session_state:
    st.session_state['quiz_submitted'] = False

# --- 3. UI 스타일링 및 함수 ---

def color_header(text, color):
    """지정된 색상으로 제목을 표시합니다."""
    st.markdown(f"## <span style='color:{color};'>{text}</span>", unsafe_allow_html=True)

def start_quiz():
    """퀴즈 시작 버튼을 눌렀을 때 상태 변경"""
    st.session_state['quiz_started'] = True
    st.session_state['quiz_submitted'] = False
    # 퀴즈 시작 시 답변 상태 초기화 (None)
    st.session_state['user_answers'] = {f"q_{i}": None for i in range(len(QUIZ_DATA))} 

def submit_quiz():
    """퀴즈 제출 버튼을 눌렀을 때 채점 및 상태 변경"""
    st.session_state['quiz_submitted'] = True

# --- 4. 도감 정보 표시 함수 (시각화 유지) ---

def display_king_info(king_name):
    """선택된 국왕의 정보와 가상 일기를 메인 화면에 표시합니다."""
    info = KING_DATA[king_name]
    
    st.header(f"🌟 **{king_name} 국왕의 역사 여행** 🌟")
    
    # 왕의 핵심 특징 카드
    st.markdown("---")
    st.info(f"**재위 기간:** {info['reign']} | **핵심 특징:** **{info['feature']}**")
    st.markdown("---")
    
    # 가상 일기/자서전
    color_header(f"📜 {king_name} 왕의 비밀 일기/자서전 (AI 생성)", "#FF69B4") # 핑크색 제목
    
    # 📝 일기장 모양 박스
    st.markdown(
        f"""
        <div style="background-color: #FFF0F5; padding: 20px; border-radius: 15px; border: 2px dashed #FF69B4;">
            <p style='font-size: 18px; line-height: 1.6; color: #333333;'>
                {info['diary_excerpt']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 주요 업적
    color_header("🏆 꼭 알아야 할 주요 업적", "#1E90FF") # 파란색 제목
    
    cols = st.columns(len(info['achievements']))
    for i, achievement in enumerate(info['achievements']):
        with cols[i % len(cols)]:
            st.success(f"✅ {achievement}")
        
    st.caption("ℹ️ 이 모든 정보는 AI 선생님이 정리한 학습 내용이랍니다! (CK+T)")


# --- 5. 퀴즈 UI 및 로직 (오류 수정 핵심) ---

def display_quiz():
    """퀴즈 질문들을 표시합니다."""
    color_header("🎉 조선 왕조 지식 점검 퀴즈! (7문제)", "#FF4500") # 주황색 제목
    st.caption("지금까지 배운 내용을 퀴즈로 확인해 보세요! 📝")
    
    # st.form 시작
    quiz_form = st.form(key='quiz_form')
    
    # 퀴즈 로직
    for i, q in enumerate(QUIZ_DATA):
        question_key = f"q_{i}"
        
        # 퀴즈 질문 스타일링
        quiz_form.markdown(f"#### ❓ <span style='color:#8A2BE2;'>{q['questionNumber']}번 문제:</span> **{q['question']}**", unsafe_allow_html=True)
        
        options = q['answerOptions']
        # 라디오 버튼에 초등학생 친화적인 아이콘 추가 및 인덱스 표시
        display_options = [f"{('O' if opt=='O' else 'X' if opt=='X' else str(j+1)+'.')} {opt}" for j, opt in enumerate(options)]
        
        # 이전 선택 인덱스 가져오기 (None 일 수 있음)
        default_index = st.session_state['user_answers'].get(question_key)
        
        # st.radio를 form 내부에서 사용
        user_choice_display = quiz_form.radio(
            "선택:",
            display_options,
            key=question_key,
            # None을 허용하지 않으므로, None일 경우 default로 0번 인덱스 선택
            index=default_index if default_index is not None else 0 
        )
        
        # 사용자의 선택 인덱스를 저장
        selected_index = display_options.index(user_choice_display)
        st.session_state['user_answers'][question_key] = selected_index
        
        # 실제 선택된 답변 텍스트 (채점용)
        user_choice = options[selected_index]

        # 제출 후 정답 및 해설 표시
        if st.session_state['quiz_submitted']:
            is_correct = (user_choice == q['correctAnswer'])
            if is_correct:
                quiz_form.success(f"🥳 **정답!** 잘 했어요! 👍 (정답: {q['correctAnswer']})")
            else:
                quiz_form.error(f"❌ **아쉬워요!** 정답은 **{q['correctAnswer']}** 입니다. ")
                with quiz_form.expander("👀 AI 해설 다시 보기"):
                    quiz_form.markdown(f"**해설:** {q['rationale']}")
        
        quiz_form.markdown("---")

    # st.form_submit_button 추가 (제출 버튼 누락 경고 해결)
    quiz_form.form_submit_button('✨ 퀴즈 제출 및 점수 확인!', on_click=submit_quiz, 
                                 disabled=st.session_state['quiz_submitted'])

# --- 6. 점수 계산 및 결과 표시 ---

def display_results():
    """퀴즈 결과를 계산하고 점수를 표시합니다."""
    
    if not st.session_state['quiz_submitted']:
        return

    score = 0
    total_questions = len(QUIZ_DATA)
    
    for i, q in enumerate(QUIZ_DATA):
        selected_index = st.session_state['user_answers'].get(f"q_{i}")
        
        if selected_index is not None:
            options = q['answerOptions']
            user_answer = options[selected_index]
            
            if user_answer == q['correctAnswer']:
                score += 1
    
    st.markdown("---")
    st.header("💯 나의 점수는?")
    
    if score == total_questions:
        st.balloons()
        st.success(f"**🎉🎉 만점입니다!** {total_questions}문제 중 **{score}점** 획득! 당신은 역사 왕! 👑")
    elif score >= total_questions * 0.7:
        st.info(f"**👍 합격입니다!** {total_questions}문제 중 **{score}점** 획득! 조금만 더 하면 만점이에요!")
    else:
        st.warning(f"**😢 재도전이 필요해요!** {total_questions}문제 중 **{score}점** 획득. 오답 해설과 국왕 정보를 다시 확인해보세요.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⏪ 처음으로 돌아가 다시 학습하기"):
        # 초기화 시 user_answers도 None으로 설정해야 오류 방지
        st.session_state['quiz_submitted'] = False
        st.session_state['quiz_started'] = False
        st.session_state['user_answers'] = {f"q_{i}": None for i in range(len(QUIZ_DATA))}
        st.experimental_rerun()


# --- 7. 메인 앱 로직 (흐름 제어) ---

# 사이드바 설정
st.sidebar.header("🗺️ 조선 왕조 도감 탐험 🧭")
king_options = list(KING_DATA.keys())
selected_king = st.sidebar.selectbox("정보를 탐색할 국왕을 선택하세요:", king_options)

st.sidebar.markdown("---")
st.sidebar.subheader("🌟 학습 목표")
st.sidebar.info("국왕의 업적을 **감정 이입(일기)**으로 이해하고, 퀴즈로 **사실 정보(정답)**를 검증해요!")

if st.session_state['quiz_started']:
    # 퀴즈 페이지
    display_quiz()
    display_results()
else:
    # 국왕 정보 페이지 (도감)
    display_king_info(selected_king)
    
    st.markdown("---")
    st.subheader("🚀 다음 단계는 퀴즈!")
    st.info("선택한 왕의 정보를 모두 확인했나요? 준비가 되었다면 퀴즈를 풀어봅시다!")
    
    # 퀴즈 시작 버튼
    st.button("✨ 업적 검증 퀴즈 시작하기!", on_click=start_quiz, type="primary")
