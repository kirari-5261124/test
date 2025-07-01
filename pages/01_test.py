import streamlit as st

st.title("ユニバーサルデザイン")
import streamlit as st
import random

# 色覚ユニバーサルデザインに配慮したカラーパレット
color_palette = {
    'red': '#D65F5F',
    'green': '#5F8D5F',
    'blue': '#5F5F8D',
    'orange': '#D78F3B',
    'purple': '#9B5F9B'
}

# 問題を生成する関数
def generate_question():
    # ランダムに色のペアを選択
    color1, color2 = random.sample(list(color_palette.values()), 2)
    # 問題を表示
    question = f"この2色のうち、異なる色を選んでください："
    st.write(question)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div style="background-color:{color1};height:100px;width:100px;"></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="background-color:{color2};height:100px;width:100px;"></div>', unsafe_allow_html=True)
    return color1, color2

# ユーザーの選択肢を取得する関数
def user_answer(correct_color, color1, color2):
    selected = st.radio("選択肢", options=[color1, color2])
    if selected == correct_color:
        st.success("正解です！")
    else:
        st.error("不正解です。もう一度挑戦してください！")

def main():
    st.title("カラーユニバーサルデザイン視覚テスト")
    st.write("色の識別テストです。異なる色を見つけて選んでください。")

    # 問題を生成
    color1, color2 = generate_question()
    correct_color = color1  # 正解色を色1とする

    # ユーザーの回答を確認
    user_answer(correct_color, color1, color2)

if __name__ == "__main__":
    main()
