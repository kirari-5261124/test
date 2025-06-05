import streamlit as st
from PIL import Image
import numpy as np

# 色弱シミュレーション関数
def simulate_cvd(img: Image.Image, mode: str) -> Image.Image:
    img_np = np.array(img).astype(float) / 255.0
    
    matrices = {
        'protan': np.array([[0.56667, 0.43333, 0.0],
                            [0.55833, 0.44167, 0.0],
                            [0.0, 0.24167, 0.75833]]),
        'deutan': np.array([[0.625, 0.375, 0.0],
                            [0.7, 0.3, 0.0],
                            [0.0, 0.3, 0.7]]),
        'tritan': np.array([[0.95, 0.05, 0.0],
                            [0.0, 0.43333, 0.56667],
                            [0.0, 0.475, 0.525]])
    }
    
    matrix = matrices.get(mode)
    if matrix is None:
        return img

    shape = img_np.shape
    img_reshaped = img_np.reshape(-1, 3)
    transformed = img_reshaped @ matrix.T
    transformed = np.clip(transformed, 0, 1)
    img_transformed = transformed.reshape(shape)
    img_out = (img_transformed * 255).astype(np.uint8)
    return Image.fromarray(img_out)

st.title("色弱シミュレーション比較アプリ")

st.markdown("""
アップロードは最大3枚まで可能です。アップロードがない場合はサンプル画像で比較します。
""")

uploaded_files = st.file_uploader(
    "画像をアップロードしてください (複数可、最大3枚)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# サンプル画像（Streamlit付属のものを利用）
from PIL import ImageDraw, ImageFont

def create_sample_image(text: str):
    img = Image.new("RGB", (300, 200), (255, 255, 255))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    w, h = d.textsize(text, font=font)
    d.text(((300-w)/2, (200-h)/2), text, fill=(0, 0, 0), font=font)
    return img

sample_images = [
    create_sample_image("Sample 1"),
    create_sample_image("Sample 2"),
    create_sample_image("Sample 3")
]

# アップロード画像があれば使い、なければサンプルを使用
if uploaded_files:
    if len(uploaded_files) > 3:
        st.warning("最大3枚までアップロード可能です。最初の3枚を使用します。")
        uploaded_files = uploaded_files[:3]
    images = [Image.open(f).convert("RGB") for f in uploaded_files]
else:
    st.info("アップロードがないためサンプル画像を表示します。")
    images = sample_images

modes = ['original', 'protan', 'deutan', 'tritan']
mode_names = {
    'original': 'オリジナル',
    'protan': 'プロタノピア（赤色盲）',
    'deutan': 'デュタノピア（緑色盲）',
    'tritan': 'トリタノピア（青色盲）'
}

for idx, img in enumerate(images):
    st.subheader(f"画像 {idx + 1}")
    cols = st.columns(len(modes))
    
    for i, mode in enumerate(modes):
        with cols[i]:
            st.markdown(f"**{mode_names[mode]}**")
            if mode == 'original':
                st.image(img, use_column_width=True)
            else:
                sim_img = simulate_cvd(img, mode)
                st.image(sim_img, use_column_width=True)
