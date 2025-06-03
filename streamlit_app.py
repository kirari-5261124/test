import streamlit as st
from PIL import Image
import numpy as np
import os
import io
import base64

# 色弱シミュレーション関数
def simulate_color_blindness(image, type):
    img = np.array(image)
    if type == 'Deuteranopia':
        img[:, :, 0] = img[:, :, 1] = img[:, :, 2] = 0  # 仮の変換処理
    elif type == 'Protanopia':
        img[:, :, 1] = img[:, :, 2] = 0  # 仮の変換処理
    elif type == 'Tritanopia':
        img[:, :, 0] = img[:, :, 1] = 0  # 仮の変換処理
    return Image.fromarray(img)

# 画像を保存する関数
def save_image(image, filename):
    # 保存先ディレクトリ
    save_dir = 'saved_images'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 画像を保存
    image.save(os.path.join(save_dir, filename))

# 画像をBase64エンコードしてダウンロードリンクを作成
def get_image_download_link(image, filename):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a href="data:file/png;base64,{img_str}" download="{filename}">画像をダウンロード</a>'

# アプリケーションのUI
def app():
    st.title("色弱シミュレーション比較アプリ")

    # 画像アップロード
    uploaded_file = st.file_uploader("画像をアップロード", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption='アップロードした画像', use_column_width=True)

            # 色弱タイプ選択
            color_blind_type = st.selectbox(
                "色弱のタイプを選択",
                ["なし", "Deuteranopia", "Protanopia", "Tritanopia"]
            )

            if color_blind_type != "なし":
                # シミュレーション実行
                simulated_image = simulate_color_blindness(image, color_blind_type)
                st.image(simulated_image, caption=f'{color_blind_type}シミュレーション後', use_column_width=True)

                # 保存ボタン
                save_button = st.button(f"{color_blind_type} シミュレーション画像を保存")
                if save_button:
                    filename = f"{color_blind_type}_{uploaded_file.name}"
                    save_image(simulated_image, filename)
                    st.success(f"{color_blind_type}画像が保存されました: {filename}")

                    # ダウンロードリンクを表示
                    download_link = get_image_download_link(simulated_image, filename)
                    st.markdown(download_link, unsafe_allow_html=True)

            else:
                st.warning("色弱タイプを選択してください")

        except Exception as e:
            st.error(f"画像の処理中にエラーが発生しました: {str(e)}")
    else:
        st.info("画像をアップロードしてください。")

    # 保存された画像を表示
    st.subheader("保存された画像一覧")
    saved_images = os.listdir('saved_images')
    if saved_images:
        for image_file in saved_images:
            st.image(f'saved_images/{image_file}', caption=image_file, use_column_width=True)

            # 画像選択ボタン
            select_button = st.button(f"{image_file}を選択")
            if select_button:
                selected_image = Image.open(f'saved_images/{image_file}')
                st.image(selected_image, caption=f"選択された画像: {image_file}", use_column_width=True)

if __name__ == "__main__":
    app()
