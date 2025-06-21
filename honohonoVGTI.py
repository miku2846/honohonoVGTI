import streamlit as st

# タイトル
st.title("🍅 VGTI 診断 🍆")

# 質問と対応するタイプ文字
questions = [
    ('1日3食ご飯を食べていますか？', 'R', 'I'),
    ('外食より家での食事のほうが多いですか？', 'H', 'E'),
    ('野菜を摂る時に何か障壁はありますか？', 'F', 'B'),
    ('野菜を意識して食べていますか？', 'L', 'D')
]

# セッション状態の初期化
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'VGTI' not in st.session_state:
    st.session_state.VGTI = ""

# 画像ファイルとVGTIタイプの対応
image_VGTI = {
    'RHFL': 'RHFL.png',
    'RHFD': 'RHFD.png',
    'RHBL': 'RHBL.png',
    'REFL': 'REFL.png',
    'REFD': 'REFD.png',
    'IHFL': 'IHFL.png',
    'REBL': 'REBL.png',
    'RHBD': 'RHBD.png',
    'IEFL': 'IEFL.png',
    'IHBL': 'IHBL.png',
    'REBD': 'REBD.png',
    'IHFD': 'IHFD.png',
    'IEBL': 'IEBL.png',
    'IEBD': 'IEBD.png',
    'IEFD': 'IEFD.png',
    'IHBD': 'IHBD.png'
}

# VGTI診断のランク分け
wao = {'RHFL', 'RHFD', 'RHBL', 'REFL'}
ooo = {'REFD', 'IHFL', 'REBL', 'RHBD'}
iine = {'IEFL', 'IHBL', 'REBD', 'IHFD'}
eee = {'IEBL', 'IEBD', 'IEFD', 'IHBD'}

# 質問表示と回答処理を関数にまとめる
def show_question():
    q, y, n = questions[st.session_state.step]
    st.write(q)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい", key=f"yes_{st.session_state.step}"):
            st.session_state.VGTI += y
            st.session_state.step += 1
            return True  # 早期リターンして再描画へ
    with col2:
        if st.button("いいえ", key=f"no_{st.session_state.step}"):
            st.session_state.VGTI += n
            st.session_state.step += 1
            return True
    return False

def show_result():
    VGTI = st.session_state.VGTI
    st.header(f"あなたのVGTIタイプは: {VGTI} 🌱")

    if VGTI in wao:
        st.success('ベジレベル★★★★\n1日3食食べていて素晴らしい！周りの人にも野菜摂取を勧めてみましょう！')
    elif VGTI in ooo:
        st.info('ベジレベル★★★\n食事への意識が高いですね!これからも毎日の野菜摂取を続けましょう！')
    elif VGTI in iine:
        st.warning('ベジレベル★★\n3食の意識・野菜摂取の意識向上を目指しましょう！')
    elif VGTI in eee:
        st.error('ベジレベル★\n危険度MAX！！まずは１日３食規則正しい生活から！トマトケチャップや野菜ジュースなど手軽に摂れる野菜を取り入れてみましょう！')
    else:
        st.error("ERROR: 不正な診断コードです")

    if VGTI in image_VGTI:
        st.markdown(
            f"""<div style="text-align: center;">
                <img src="https://raw.githubusercontent.com/miku2846/honohonoVGTI/main/{image_VGTI[VGTI]}" width="300" />
                <p>{VGTI}のイメージ</p>
            </div>""",
            unsafe_allow_html=True
        )
    
    # リトライボタンを右側に配置
    col1, col2, col3 = st.columns([3,1,1])
    with col3:
        if st.button("もう一度ベジる🥦>>>"):
            st.session_state.step = 0
            st.session_state.VGTI = ""
            return True
    return False

# メイン処理
if st.session_state.step < len(questions):
    if show_question():
        st.rerun()
else:
    if show_result():
        st.rerun()
