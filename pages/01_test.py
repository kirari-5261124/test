import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageDraw
import io

# ページ設定
st.set_page_config(
    page_title="色覚異常判断テスト",
    page_icon="👁️",
    layout="wide"
)

# セッション状態の初期化
if 'current_test' not in st.session_state:
    st.session_state.current_test = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'test_completed' not in st.session_state:
    st.session_state.test_completed = False

def create_ishihara_pattern(number, size=400, dot_size_range=(8, 20)):
    """石原式色覚検査風のパターンを生成"""
    # 色の定義
    colors = {
        'red': [(255, 100, 100), (255, 150, 150), (200, 80, 80), (180, 60, 60)],
        'green': [(100, 255, 100), (150, 255, 150), (80, 200, 80), (60, 180, 60)],
        'background': [(200, 200, 150), (180, 180, 130), (220, 220, 170), (160, 160, 110)]
    }
    
    # 数字のパターン定義
    number_patterns = {
        8: [
            [0, 1, 1, 1, 0],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [0, 1, 1, 1, 0]
        ],
        3: [
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0]
        ],
        5: [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0]
        ],
        2: [
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 1, 1, 1, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1]
        ]
    }
    
    # 画像作成
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 背景ドットを描画
    for _ in range(2000):
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        dot_size = random.randint(*dot_size_range)
        color = random.choice(colors['background'])
        draw.ellipse([x-dot_size//2, y-dot_size//2, x+dot_size//2, y+dot_size//2], fill=color)
    
    # 数字パターンを描画
    if number in number_patterns:
        pattern = number_patterns[number]
        center_x, center_y = size // 2, size // 2
        cell_size = size // 8
        
        for i, row in enumerate(pattern):
            for j, cell in enumerate(row):
                if cell == 1:
                    # 数字部分のドット
                    for _ in range(50):
                        offset_x = random.randint(-cell_size//2, cell_size//2)
                        offset_y = random.randint(-cell_size//2, cell_size//2)
                        x = center_x + (j - 2) * cell_size + offset_x
                        y = center_y + (i - 2) * cell_size + offset_y
                        
                        if 0 <= x < size and 0 <= y < size:
                            dot_size = random.randint(*dot_size_range)
                            color = random.choice(colors['red'])
                            draw.ellipse([x-dot_size//2, y-dot_size//2, x+dot_size//2, y+dot_size//2], fill=color)
    
    return img

def create_line_test():
    """線の判別テスト画像を生成"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 背景色
    ax.set_facecolor('#f0f0f0')
    
    # 複数の線を描画
    x = np.linspace(0, 10, 100)
    
    # 正常者には見える線（赤と緑のコントラスト）
    y1 = np.sin(x) + 2
    ax.plot(x, y1, color='#ff4444', linewidth=3, label='線A')
    
    # 色覚異常者には見えにくい線
    y2 = np.cos(x) + 4
    ax.plot(x, y2, color='#44ff44', linewidth=3, label='線B')
    
    # 誰でも見える線
    y3 = np.sin(x + 1) + 6
    ax.plot(x, y3, color='#4444ff', linewidth=3, label='線C')
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_title('どの線が見えますか？', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # 日本語フォント設定
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
    # 画像をバイト配列に変換
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    buf.seek(0)
    plt.close()
    
    return Image.open(buf)

# テストデータ
test_data = [
    {
        'type': 'number',
        'number': 8,
        'question': '画像の中に見える数字を答えてください',
        'correct_answer': '8',
        'options': ['6', '8', '9', '見えない']
    },
    {
        'type': 'number',
        'number': 3,
        'question': '画像の中に見える数字を答えてください',
        'correct_answer': '3',
        'options': ['2', '3', '5', '見えない']
    },
    {
        'type': 'number',
        'number': 5,
        'question': '画像の中に見える数字を答えてください',
        'correct_answer': '5',
        'options': ['2', '3', '5', '見えない']
    },
    {
        'type': 'line',
        'question': '画像の中で見える線を全て選んでください（複数選択可）',
        'correct_answer': ['線A', '線B', '線C'],
        'options': ['線A', '線B', '線C']
    }
]

# メインアプリ
def main():
    st.title("色覚異常判断テスト ver.1")
    st.write("このテストは色覚の特性を確認するためのものです。医学的診断ではありません。")
    
    # サイドバーで進行状況表示
    st.sidebar.title("テスト進行状況")
    st.sidebar.progress((st.session_state.current_test) / len(test_data))
    st.sidebar.write(f"問題 {st.session_state.current_test + 1} / {len(test_data)}")
    
    if not st.session_state.test_completed:
        # 現在のテスト問題
        if st.session_state.current_test < len(test_data):
            current_question = test_data[st.session_state.current_test]
            
            st.subheader(f"問題 {st.session_state.current_test + 1}")
            st.write(current_question['question'])
            
            # 画像生成と表示
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if current_question['type'] == 'number':
                    # 数字テスト画像を生成
                    img = create_ishihara_pattern(current_question['number'])
                    st.image(img, caption=f"テスト画像 {st.session_state.current_test + 1}", width=400)
                elif current_question['type'] == 'line':
                    # 線テスト画像を生成
                    img = create_line_test()
                    st.image(img, caption="線の判別テスト", width=600)
            
            with col2:
                st.write("### 回答選択")
                
                # 回答選択
                if current_question['type'] == 'line':
                    # 複数選択
                    selected_options = []
                    for option in current_question['options']:
                        if st.checkbox(option, key=f"option_{option}"):
                            selected_options.append(option)
                    user_answer = selected_options
                else:
                    # 単一選択
                    user_answer = st.radio(
                        "回答を選択してください:",
                        current_question['options'],
                        key=f"answer_{st.session_state.current_test}"
                    )
                
                # 次へボタン
                if st.button("次へ", type="primary"):
                    st.session_state.answers.append({
                        'question': st.session_state.current_test + 1,
                        'answer': user_answer,
                        'correct': current_question['correct_answer']
                    })
                    st.session_state.current_test += 1
                    st.rerun()
        
        # テスト完了チェック
        if st.session_state.current_test >= len(test_data):
            st.session_state.test_completed = True
            st.rerun()
    
    else:
        # 結果表示
        st.success("🎉 テスト完了！")
        st.subheader("結果")
        
        correct_count = 0
        total_count = len(st.session_state.answers)
        
        for i, answer in enumerate(st.session_state.answers):
            with st.expander(f"問題 {answer['question']} の結果"):
                st.write(f"**あなたの回答**: {answer['answer']}")
                st.write(f"**正解**: {answer['correct']}")
                
                if answer['answer'] == answer['correct']:
                    st.success("✅ 正解")
                    correct_count += 1
                else:
                    st.error("❌ 不正解")
        
        # 総合結果
        st.subheader("総合結果")
        score = (correct_count / total_count) * 100
        st.metric("正答率", f"{score:.1f}%", f"{correct_count}/{total_count}")
        
        # 結果の解釈
        if score >= 75:
            st.success("🟢 正常色覚の可能性が高いです")
        elif score >= 50:
            st.warning("🟡 軽度の色覚特性がある可能性があります")
        else:
            st.error("🔴 色覚特性がある可能性があります")
        
        st.info("**注意**: このテストは簡易的なものです。正確な診断には眼科医の検査を受けることをお勧めします。")
        
        # リセットボタン
        if st.button("テストをやり直す", type="secondary"):
            st.session_state.current_test = 0
            st.session_state.answers = []
            st.session_state.test_completed = False
            st.rerun()

if __name__ == "__main__":
    main()