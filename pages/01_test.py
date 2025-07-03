import streamlit as st

st.title("🎨 色覚異常チェックテスト (サンプル画像付き)")

st.write("""
以下の画像に含まれる数字を選択肢から選んでください。
""")

# テストデータ: 画像URLと質問、選択肢、正解
tests = [
    {
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Ishihara_plate_12.svg/320px-Ishihara_plate_12.svg.png",
        "question": "この画像に見える数字は？",
        "options": ["12", "6", "なし", "8"],
        "answer": "12"
    },
    {
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Ishihara_plate_8.svg/320px-Ishihara_plate_8.svg.png",
        "question": "この画像に見える数字は？",
        "options": ["3", "8", "6", "見えない"],
        "answer": "8"
    },
    {
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Ishihara_plate_6.svg/320px-Ishihara_plate_6.svg.png",
        "question": "この画像に見える数字は？",
        "options": ["6", "5", "2", "見えない"],
        "answer": "6"
    }
]

score = 0
total = len(tests)

for i, test in enumerate(tests):
    st.subheader(f"テスト {i + 1}")
    st.image(test["image_url"], width=300)
    user_answer = st.radio(test["question"], test["options"], key=f"q{i}")
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
        st.warning("一部誤答があります。気になる場合は専門
