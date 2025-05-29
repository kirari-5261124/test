import streamlit as st
from PIL import Image
import numpy as np
import colorspacious as cs
import os

# 色弱タイプ定義
COLOR_VISION_SIMULATIONS = {
    "プロトノピア 🔴": {"cvd_type": "protan", "severity": 100},
    "デューテラノピア 🟢": {"cvd_type": "deutan", "severity": 100},
    "トリタノピア 🔵": {"cvd_type": "tritan", "severity": 100},
}

st.set_page_config(page_title="色弱シミュレーション比較", layout="wide")
st.title("👁 色弱シミュレーション比較アプリ（4分割ビュー）")

# サンプル画像（任意で差し替え可能）
sample_path = "sample.jpg"
if os.path.exists(sample_path):
    sample_image = Image.open(sample_path).convert("RGB")
else:
    sample_image = None

# UI構築
st.markdown("画像をアップロードするか、サンプル画像を使用してください。")
col1, col2 = st.columns([2, 1])
with col1:
    uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])
with col2:
    use_sample = st.checkbox("📎 サンプル画像を使う", value=(uploaded_file is None))

# 入力画像の決定
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
elif use_sample and sample_image:
    image = sample_image
else:
    image = None

# シミュレーション処理
if image:
    img_array = np.array(image) / 255.0

    # 変換後画像を保存
    sim_images = {}
    for label, params in COLOR_VISION_SIMULATIONS.items():
        simulated = cs.cvd_simulate(img_array, {
            "name": "sRGB1",
            "cvd_type": params["cvd_type"],
            "severity": params["severity"]
        })
        sim_img = Image.fromarray((simulated * 255).astype("uint8"))
        sim_images[label] = sim_img

    # 表示
    st.subheader("🖼️ 比較ビュー")
    col1, col2, col3, col4 = st.columns(4)

    col1.markdown("**🎨 オリジナル**")
    col1.image(image, use_column_width=True)

    for col, (label, sim_img) in zip([col2, col3, col4], sim_images.items()):
        col.markdown(f"**{label}**")
        col.image(sim_img, use_column_width=True)
else:
    st.warning("画像がありません。アップロードするか、サンプルを使ってください。")
