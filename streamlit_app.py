import streamlit as st
from PIL import Image
import numpy as np
from colorspacious import cspace_convert

st.title("色弱シミュレーション比較アプリ")

# 色弱タイプ選択
sim_types = {
    "正常": None,
    "プロタノピア (赤弱)": "protanomaly",
    "デューテラノピア (緑弱)": "deuteranomaly",
    "トリタノピア (青弱)": "tritanomaly"
}
sim_choice = st.selectbox("シミュレーションタイプを選択", list(sim_types.keys()))

# 画像アップロード
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])

# サンプル画像のパス（ローカルに画像がある場合）
sample_image_path = "sample.jpg"

# アップロードされていない場合、サンプル画像を表示
if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="元画像", use_column_width=True)
else:
    # サンプル画像を表示
    try:
        img = Image.open(sample_image_path).convert("RGB")
        st.image(img, caption="サンプル画像", use_column_width=True)
    except FileNotFoundError:
        st.write("サンプル画像が見つかりませんでした。")

# シミュレーション処理
if uploaded_file or not uploaded_file:  # 画像がアップロードされている場合でもサンプル画像の場合でも
    if sim_choice != "正常":
        # PIL→numpy
        img_np = np.array(img) / 255.0

        # colorspaciousの色覚変換パラメータ
        cb_type = sim_types[sim_choice]
        # colorspaciousで色覚異常をシミュレート
        img_sim = cspace_convert(img_np, "sRGB1", f"sRGB1+CVD-{cb_type}")

        # 0-1にクリップしてuint8に戻す
        img_sim = np.clip(img_sim, 0, 1)
        img_sim = (img_sim * 255).astype(np.uint8)

        st.image(img_sim, caption=f"{sim_choice} シミュレーション", use_column_width=True)
    else:
        st.write("元画像を表示しています。")
