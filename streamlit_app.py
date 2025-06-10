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
if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="元画像", use_column_width=True)

    # シミュレーション処理
    if sim_choice != "正常":
        # PIL→numpy
        img_np = np.array(img) / 255.0

        # colorspaciousの色覚変換パラメータ
        cb_type = sim_types[sim_choice]
        # colorspaciousで色覚異常をシミュレート
        # cspace_convertで一旦色空間変換して色弱シミュレーションを実施
        # colorspaciousの色覚変換名に合わせてください（例: 'sRGB1', 'sRGB1+CVD', etc）

        # ここでは例としてprotanomalyの色覚変換を実装
        # しかしcolorspaciousの実際の呼び出しは以下のようにする必要がある
        img_sim = cspace_convert(img_np, "sRGB1", f"sRGB1+CVD-{cb_type}")

        # 0-1にクリップしてuint8に戻す
        img_sim = np.clip(img_sim, 0, 1)
        img_sim = (img_sim * 255).astype(np.uint8)

        st.image(img_sim, caption=f"{sim_choice} シミュレーション", use_column_width=True)
    else:
        st.write("元画像を表示しています。")

else:
    st.write("画像をアップロードしてください。")
