import streamlit as st
import openai

# 페이지 설정
st.set_page_config(page_title="하루와 대화하기", page_icon="👧")
st.title("👧 하루가 들어줄게요!")
st.write("SEL 감정 대화 친구, 하루와 함께 지금의 기분을 나눠보아요!")

# ✅ secrets에서 API 키 가져오기
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 세션 상태 초기화
if "emotion_stage" not in st.session_state:
    st.session_state.emotion_stage = "ask_emotion"
if "emotion" not in st.session_state:
    st.session_state.emotion = ""
if "reason" not in st.session_state:
    st.session_state.reason = ""
if "response" not in st.session_state:
    st.session_state.response = ""

# GPT 응답 생성 함수
def get_gpt_response(emotion, reason):
    prompt = f"지금 '{emotion}'이라는 감정을 느끼고 있어요. 그 이유는 '{reason}' 때문이에요. 이 아이는 초등학생이고, 동갑내기 여학생 하루가 말하는 것처럼 따뜻하고 다정하게 반응해주세요."
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "하루라는 초등학교 여학생이야. 아이처럼 말해도 괜찮고 조금 서투르지만, SEL 감정 전문가처럼 따뜻하게 감정을 받아주고 위로하거나 함께 기뻐해줘."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )
    return response.choices[0].message.content

# 단계별 인터페이스 구성
if st.session_state.emotion_stage == "ask_emotion":
    emotion_input = st.text_input("👧 하루: 지금 기분이 어때? (예: 기쁨, 슬픔, 짜증, 불안 등)", key="emotion_input")
    if st.button("다음") and emotion_input.strip():
        st.session_state.emotion = emotion_input.strip()
        st.session_state.emotion_stage = "ask_reason"
        st.rerun()

elif st.session_state.emotion_stage == "ask_reason":
    st.write(f"👧 하루: 왜 '{st.session_state.emotion}' 같은 기분이 드는 것 같아?")
    reason_input = st.text_input("여기에 이유를 적어줘:", key="reason_input")
    if st.button("하루에게 말 걸기") and reason_input.strip():
        st.session_state.reason = reason_input.strip()
        with st.spinner("하루가 생각 중이에요..."):
            st.session_state.response = get_gpt_response(
                st.session_state.emotion, st.session_state.reason
            )
        st.session_state.emotion_stage = "show_response"
        st.rerun()

elif st.session_state.emotion_stage == "show_response":
    st.success("👧 하루의 대답:")
    st.write(st.session_state.response)
    if st.button("↩️ 다시 시작하기"):
        for key in ["emotion_stage", "emotion", "reason", "response"]:
            st.session_state.pop(key, None)
        st.rerun()
