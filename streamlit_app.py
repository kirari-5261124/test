import streamlit as st

st.set_page_config(page_title="パーソナルカラー診断", layout="centered")
st.title("🎨 パーソナルカラー簡易診断")

st.markdown("""
肌の色や髪の色、目の色、似合う色の傾向などから、あなたのパーソナルカラーを推測します。
""")

# 質問項目
skin_tone = st.selectbox("あなたの肌の色は？", ["明るくピンクがかっている", "明るく黄みがかっている", "オークル系", "暗めで黄みが強い"])
hair_color = st.selectbox("髪の色は？", ["黒に近い", "明るいブラウン", "赤みがある", "アッシュ系"])
eye_color = st.selectbox("目の色は？", ["黒・ダークブラウン", "明るい茶色", "グレーっぽい", "グリーンっぽい"])
favorite_colors = st.multiselect("どんな色の服を着ると褒められますか？", ["白", "パステルカラー", "ビビッドカラー", "アースカラー", "黒・ネイビー"])

if st.button("診断する"):
    # 簡易ルールベース診断
    if "パステルカラー" in favorite_colors or skin_tone == "明るくピンクがかっている":
        result = "スプリング または サマー"
        tone = "明るく柔らかい色が似合います 🌸"
    elif "アースカラー" in favorite_colors or skin_tone == "オークル系":
        result = "オータム"
        tone = "深みのある暖色が似合います 🍁"
    elif "ビビッドカラー" in favorite_colors or hair_color == "アッシュ系":
        result = "ウィンター"
        tone = "はっきりとしたコントラストの強い色が似合います ❄️"
    else:
        result = "中間タイプ（ニュートラル）"
        tone = "多くの色を着こなせます 🎨"

    st.subheader("🧾 診断結果")
    st.markdown(f"**推定タイプ：{result}**")
    st.info(tone)
