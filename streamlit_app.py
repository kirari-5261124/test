import streamlit as st
from PIL import Image
import numpy as np
from colorspacious import cspace_convert
from streamlit_image_comparison import image_comparison

# タイトル
st.title("色弱シミュレーション・ビフォーアフター比較アプリ")

# 色覚タイプと強度
sim_types = {
    "プロタノピア（赤が見えにくい）": "protanomaly",
    "デューテラノピア（緑が見えにくい）": "deuteranomaly",
    "トリタノピア（青が見えにくい）": "tritanomaly"
}
sim_choice = st.selectbox("シミュレーションタイプを選択", list(sim_types.keys()))
severity = st.slider("色覚異常の強さ（severity）", 0, 100, 50)

# サンプル画像読み込み
sample_image_path = "sample.jpg"
try:
    img = Image.open(sample_image_path).convert("RGB")
    img_np = np.array(img) / 255.0

    # 色弱シミュレーション画像生成
    cb_type = sim_types[sim_choice]
    img_sim = cspace_convert(
        img_np,
        start="sRGB1",
        end={
            "name": "sRGB1+CVD",
            "cvd_type": cb_type,
            "severity": severity
        }
    )
    img_sim = np.clip(img_sim, 0, 1)
    img_sim = (img_sim * 255).astype(np.uint8)
    img_sim_pil = Image.fromarray(img_sim)

    # 🔄 ビフォーアフター比較
    st.subheader("ビフォーアフター比較（スライダーで違いを確認）")
    image_comparison(
        img1=img,
        img2=img_sim_pil,
        label1="オリジナル",
        label2=f"{sim_choice} シミュレーション",
    )

except FileNotFoundError:
    st.error("サンプル画像（sample.jpg）が見つかりません。アプリと同じフォルダに配置してください。")
