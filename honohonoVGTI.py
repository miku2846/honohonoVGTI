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

# セッション変数
if 'step' not in st.session_state:
    st.session_state.step = 0
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


# 質問を1問ずつ表示
if st.session_state.step < len(questions):
    q, y, n = questions[st.session_state.step]
    st.write(q)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい", key=f"yes_{st.session_state.step}"):
            st.session_state.VGTI += y
            st.session_state.step += 1
    with col2:
        if st.button("いいえ", key=f"no_{st.session_state.step}"):
            st.session_state.VGTI += n
            st.session_state.step += 1


# 結果表示
elif st.session_state.step == len(questions):
    VGTI = st.session_state.VGTI
    st.header(f"あなたのVGTIタイプは: {VGTI} 🌱")

    if VGTI in wao:
        st.success('ベジレベル★★★★　1日3食食べていて素晴らしい！周りの人にも野菜摂取を勧めてみましょう！')
    elif VGTI in ooo:
        st.info('ベジレベル★★★　食事への意識が高いですね!これからも毎日の野菜摂取を続けましょう！')
    elif VGTI in iine:
        st.warning('ベジレベル★★　3食の意識・野菜摂取の意識向上を目指しましょう！')
    elif VGTI in eee:
        st.error('ベジレベル★　危険度MAX！！まずは１日３食規則正しい生活から！トマトケチャップや野菜ジュースなど手軽に摂れる野菜を取り入れてみましょう！')
    else:
        st.error("ERROR: 不正な診断コードです")

    if VGTI in image_VGTI:
        st.image(image_VGTI[VGTI], width=300, caption=f"{VGTI}のイメージ")


