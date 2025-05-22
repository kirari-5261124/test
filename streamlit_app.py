import streamlit as st

st.title('世界の言葉')
st.write('こんにちは')
user_name = st.text_input('名前を入力してください')
st.header('あなたの名前は' + str(user_name) + 'です')
h = st.number_input('身長を入力してください(m)',value = 1.6)
w = st.number_input('体重を入力してください', value = 50)

bmi = w/(h**2)

dbmi = round(bmi,2)

st.header('あなたのBMIは' + str(dbmi) + 'です')
st.slider('年齢を選択してください' 0, 100)
fuits = st.selectbox('好きな果物を選んでください', ['リンゴ','バナナ','チェリー'])