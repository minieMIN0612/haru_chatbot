import streamlit as st
import openai

# 페이지 설정
st.set_page_config(page_title="하루와 대화하기", page_icon="👧")

st.title("👧 하루와 대화를 나눠보아요!")
st.write("SEL 감정 대화 친구, 하루와 함께 지금의 기분을 나눠보아요!")

# ✅ secrets.toml에서 안전하게 API 키 불러오기
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 입력창: 감정과 이유
emotion = st.text_input("👧 하루: 지금 기분이 어때? (예: 기쁨, 슬픔, 짜증, 불안 등)")
reason = st.text_input(f"👧 하루: 왜 '{emotion}' 같은 기분이 드는 것 같아?" if emotion else "")

# 버튼 클릭 시 GPT 응답
if st.button("하루에게 말 걸기"):
    if not emotion or not reason:
        st.warning("기분과 이유를 모두 입력해주세요!")
    else:
        with st.spinner("하루가 생각 중이에요..."):
            prompt = f"지금 '{emotion}'이라는 감정을 느끼고 있어요. 그 이유는 '{reason}' 때문이에요. 이 아이는 초등학생이고, 동갑내기 여학생 하루가 말하는 것처럼 따뜻하고 다정하게 반응해주세요."

            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "하루라는 초등학교 여학생이야. 아이처럼 말해도 괜찮고 조금 서투르지만, SEL 감정 전문가처럼 따뜻하게 감정을 받아주고 위로하거나 함께 기뻐해줘."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8
                )

                message = response.choices[0].message.content
                st.success("👧 하루의 대답:")
                st.write(message)

            except Exception as e:
                st.error(f"오류가 발생했어요: {e}")
