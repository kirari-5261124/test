import streamlit as st
from PIL import Image
import numpy as np
from colorspacious import cspace_convert  # type: ignore

st.title("色弱シミュレーション比較アプリ")

sim_types = {
    "正常": None,
    "プロタノピア (赤弱)": "protanomaly",
    "デューテラノピア (緑弱)": "deuteranomaly",
    "トリタノピア (青弱)": "tritanomaly"
}
sim_choice = st.selectbox("シミュレーションタイプを選択", list(sim_types.keys()))

sample_image_path = "sample.jpg"

img = None
try:
    img = Image.open(sample_image_path).convert("RGB")
    st.image(img, caption="サンプル画像", use_column_width=True)
except FileNotFoundError:
    st.write("サンプル画像が見つかりませんでした。")

if img:
    if sim_choice != "正常":
        img_np = np.array(img) / 255.0
        cb_type = sim_types[sim_choice]

        img_sim = cspace_convert(
            img_np,
            start="sRGB1",
            end={
                "name": "sRGB1+CVD",
                "cvd_type": cb_type,
                "severity": 100  
            }
        )

        img_sim = np.clip(img_sim, 0, 1)
        img_sim = (img_sim * 255).astype(np.uint8)

        st.image(img_sim, caption=f"{sim_choice} シミュレーション", use_column_width=True)
    else:
        st.write("元画像を表示しています。")
