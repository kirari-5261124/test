import streamlit as st
from PIL import Image

st.title("🎨 色覚異常チェックテスト")
st.write("""
以下の画像に含まれる数字が見えますか？
見えた数字を選択肢から選んでください。
""")

# 色覚異常テスト用の画像と回答
tests = [
    {
        "image": "ishihara_12.png",
        "question": "この画像に見える数字は？",
        "options": ["12", "6", "なし", "8"],
        "answer": "12"
    },
    {
        "image": "ishihara_8.png",
        "question": "この画像に見える数字は？",
        "options": ["3", "8", "6", "見えない"],
        "answer": "8"
    },
    {
        "image": "ishihara_6.png",
        "question": "この画像に見える数字は？",
        "options": ["6", "5", "2", "見えない"],
        "answer": "6"
    }
]

score = 0
total = len(tests)

for i, test in enumerate(tests):
    st.subheader(f"テスト {i + 1}")
    # 画像表示
    image = Image.open(test["image"])
    st.image(image, width=300)
    
    # ユーザー回答取得
    user_answer = st.radio(test["question"], test["options"], key=f"q{i}")
    
    # 答え合わせ（ボタン押下後に判定するので、一旦結果保存）
    tests[i]["user_answer"] = user_answer

if st.button("結果を表示"):
    for test in tests:
        if test["user_answer"] == test["answer"]:
            score += 1
    st.success(f"正解数: {score} / {total}")
    if score == total:
        st.info("色覚異常の兆候は見られません。")
    elif score == 0:
        st.warning("色覚異常の可能性があります。専門医の診断をおすすめします。")
    else:
        st.warning("一部誤答があります。気になる場合は専門医へ。")

st.caption("※このテストは簡易的なチェック用です。正式な診断は専門機関で行ってください。")
