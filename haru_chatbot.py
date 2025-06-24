import streamlit as st
import openai

# 페이지 설정
st.set_page_config(page_title="하루와 마음 나누기", page_icon="👩🏻")
st.title("👩🏻 하루에게 말을 걸어봐!")
st.write("오늘 어땠어? 지금의 기분을 함께 나눠보자!")

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
    prompt = f"지금 '{emotion}'이라는 감정을 느끼고 있어. 그 이유는 '{reason}' 때문이야. 하루는 초등학교 여학생이야. 또래 친구에게 말하듯 따뜻하고 다정하게 반응해줘. 문장은 쉽고 짧게. 항상 반말을 써. 공감의 말 한 마디를 꼭 넣어줘. 그리고 입력된 감정이 모호하거나 일상적인 표현(예: 힘들어, 그냥 그래, 몰라)일 경우, 더 구체적인 감정 단어로 바꿔서 설명해주고, 비슷한 감정 단어 하나도 추가로 추천해줘."

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 하루라는 초등학교 여학생이야. 문장은 쉽고 짧게, 감정에 공감하는 따뜻한 말투로 대화해. 항상 반말을 사용해. 존댓말, '당신', '그대', '얘야' 같은 말은 절대 쓰지 마. 입력된 감정이 모호하거나 일상적인 표현일 경우, 그 감정을 '지치다', '속상하다', '외롭다', '불안하다'처럼 구체적인 감정 단어로 바꿔서 설명하고, 비슷한 감정 하나도 추천해줘."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )
    return response.choices[0].message.content

# 단계별 인터페이스 구성
if st.session_state.emotion_stage == "ask_emotion":
    emotion_input = st.text_input("👩🏻 하루: 지금 기분이 어때? (예: 기쁨, 슬픔, 짜증, 불안 등)", key="emotion_input")
    if st.button("다음") and emotion_input.strip():
        st.session_state.emotion = emotion_input.strip()
        st.session_state.emotion_stage = "ask_reason"
        st.rerun()

elif st.session_state.emotion_stage == "ask_reason":
    st.write(f"👩🏻 하루: 왜 '{st.session_state.emotion}' 같은 기분이 드는 것 같아?")
    reason_input = st.text_input("여기에 이유를 적어줘:", key="reason_input")
    if st.button("하루의 대답 듣기") and reason_input.strip():
        st.session_state.reason = reason_input.strip()
        with st.spinner("하루가 생각 중이에요..."):
            st.session_state.response = get_gpt_response(
                st.session_state.emotion, st.session_state.reason
            )
        st.session_state.emotion_stage = "show_response"
        st.rerun()

elif st.session_state.emotion_stage == "show_response":
    st.success("👩🏻 하루의 대답:")
    st.write(st.session_state.response)
    if st.button("↩️ 다시 시작하기"):
        for key in ["emotion_stage", "emotion", "reason", "response"]:
            st.session_state.pop(key, None)
        st.rerun()
