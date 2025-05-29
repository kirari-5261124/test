import streamlit as st
from PIL import Image
import numpy as np
import colorspacious as cs
import os

# 色弱タイプの定義
COLOR_VISION_TYPES = {
    "正常色覚 (Normal Vision)": None,
    "プロトノピア（赤）": {"name": "sRGB1", "cvd_type": "protan", "severity": 100},
    "デューテラノピア（緑）": {"name": "sRGB1", "cvd_type": "deutan", "severity": 100},
    "トリタノピア（青）": {"name": "sRGB1", "cvd_type": "tritan", "severity": 100},
}

# StreamlitのUI
st.set_page_config(page_title="色弱シミュレーター", layout="centered")
st.title("🧠 色弱シミュレーションアプリ")

# サンプル画像の読み込み
sample_path = "sample.jpg"
if os.path.exists(sample_path):
    sample_image = Image.open(sample_path).convert("RGB")
    st.sidebar.image(sample_image, caption="📷 サンプル画像", use_column_width=True)
else:
    st.sidebar.warning("sample.jpg が見つかりません。")

# ファイルアップロード or サンプル画像使用
uploaded_file = st.file_uploader("画像をアップロードするか、サンプルを使ってください", type=["png", "jpg", "jpeg"])
use_sample = st.checkbox("📎 サンプル画像を使う", value=uploaded_file is None)

# 色覚タイプの選択
vision_type = st.selectbox("シミュレーションする色覚タイプを選択", list(COLOR_VISION_TYPES.keys()))

# 対象画像を取得
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
elif use_sample and os.path.exists(sample_path):
    image = sample_image
else:
    image = None

if image:
    st.subheader("🖼️ 元の画像")
    st.image(image, use_column_width=True)

    if COLOR_VISION_TYPES[vision_type] is not None:
        # NumPy配列に変換（0〜1）
        img_array = np.array(image) / 255.0
        simulated = cs.cvd_simulate(img_array, COLOR_VISION_TYPES[vision_type])

        # PIL画像に変換
        simulated_img = Image.fromarray((simulated * 255).astype("uint8"))

        st.subheader(f"🎨 {vision_type} のシミュレーション結果")
        st.image(simulated_img, use_column_width=True)
    else:
        st.info("正常色覚が選択されています。シミュレーションは行われません。")
else:
    st.warning("画像が選択されていません。アップロードまたはサンプルを選んでください。")
