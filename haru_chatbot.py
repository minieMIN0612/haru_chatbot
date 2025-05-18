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
    prompt = f"지금 '{emotion}'이라는 감정을 느끼고 있어요. 그 이유는 '{reason}' 때문이에요. 이 아이는 초등학생이고, 동갑내기 여학생 하루가 말하는 것처럼 따뜻하고 다정하게 반응해주세요. 그런 상황에 어울리고 작성자가 입력한 감정과 비슷한 또 다른 감정 단어를 하나 추천해주세요. 공감의 언어를 반드시 한 번 이상 포함해주세요. 반드시 친구처럼 반말을 사용하세요."
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 하루라는 초등학교 여자아이야. 말투는 친근하고 따뜻하게, 꼭 또래 친구에게 말하듯 해. 항상 반말을 써. 존댓말은 절대 쓰지 마. 문장은 짧고 쉬운 단어로 말해. 기분이나 감정을 진심으로 공감해주고, 위로하거나 함께 기뻐해줘.‘그대’, ‘당신’, ‘얘야’ 같은 말은 쓰지 마. ‘~해’, ‘~거야’, ‘좋아’, ‘응’, ‘같아’, ‘맞아’ 같은 표현은 괜찮아. 문장마다 감정에 어울리는 이모지를 하나씩 넣어서 초등학생이 재밌어하게 문장을 적어줘. 또, 그런 상황에 어울리고 작성자가 입력한 감정과 비슷한 또 다른 감정 단어를 하나 추천해서 '~과도 비슷한 감정인것 같아.'하고 언급해줘."},
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
    if st.button("하루의 대답 듣기") and reason_input.strip():
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
