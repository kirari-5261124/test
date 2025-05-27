import streamlit as st
from PIL import Image
import numpy as np

# 色弱変換行列（簡易版）
def simulate_colorblind(img: Image.Image, mode='protanopia'):
    # RGB 画像を NumPy 配列に変換
    img_array = np.array(img).astype(float)

    # 色覚異常の変換行列（簡易）
    if mode == 'protanopia':  # 赤色盲
        matrix = np.array([[0.567, 0.433, 0],
                           [0.558, 0.442, 0],
                           [0,     0.242, 0.758]])
    elif mode == 'deuteranopia':  # 緑色盲
        matrix = np.array([[0.625, 0.375, 0],
                           [0.7,   0.3,   0],
                           [0,     0.3,   0.7]])
    elif mode == 'tritanopia':  # 青色盲
        matrix = np.array([[0.95, 0.05,  0],
                           [0,    0.433, 0.567],
                           [0,    0.475, 0.525]])
    else:
        return img

    # 各ピクセルに変換行列を適用
    transformed = np.dot(img_array[...,:3], matrix.T)
    transformed = np.clip(transformed, 0, 255).astype(np.uint8)

    # 新しい画像を返す
    return Image.fromarray(transformed)

# Streamlit UI
st.title("👁 色弱シミュレーションアプリ")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])
mode = st.selectbox("シミュレートする色覚異常タイプ", ["protanopia", "deuteranopia", "tritanopia"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.subheader("オリジナル画像")
    st.image(image, use_column_width=True)

    # シミュレーション結果
    simulated_img = simulate_colorblind(image, mode)
    st.subheader(f"{mode} のシミュレーション画像")
    st.image(simulated_img, use_column_width=True)
