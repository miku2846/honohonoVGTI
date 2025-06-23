import streamlit as st

st.title("🍅 VGTI 診断 🍆")

# 質問と選択肢・結果の対応（[質問文, 選択肢リスト, 選択肢ごとのタイプ文字])
questions = [
    ('普段の生活リズムについて教えてください。',
     ['一日三食きちんと食べている', '食事の時間が不規則になりがち'],
     ['R', 'I']),
    ('食事のスタイルはどちらが多いですか？',
     ['家で作って食べる、または中食', '外食が多い'],
     ['H', 'E']),
    ('野菜を摂ることに障壁を感じますか？',
     ['特に障壁は感じない', '時間・手間・価格等がネックになっている'],
     ['F', 'B']),
    ('野菜を食べたいという気持ちは？',
     ['積極的に摂りたい', 'あまり意識していない'],
     ['L', 'D'])
]

# セッション初期化
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.VGTI = ""

step = st.session_state.step

if step < len(questions):
    q, options, codes = questions[step]
    st.subheader(f"Q{step + 1}. {q}")
    choice = st.radio("選択してください", options, key=f"q{step}")

    if st.button("次へ ▶"):
        selected_index = options.index(choice)
        st.session_state.VGTI += codes[selected_index]
        st.session_state.step += 1
        st.rerun()

# 結果表示
else:
    VGTI = st.session_state.VGTI
    st.header(f"あなたのVGTIタイプは: {VGTI} 🌱")

    # タイプ分け
    wao = {'RHFL', 'RHFD', 'RHBL', 'REFL'}
    ooo = {'REFD', 'IHFL', 'REBL', 'RHBD'}
    iine = {'IEFL', 'IHBL', 'REBD', 'IHFD'}
    eee = {'IEBL', 'IEBD', 'IEFD', 'IHBD'}

    # 結果表示
    if VGTI in wao:
        st.success('ベジレベル★★★★\n1日3食食べていて素晴らしい！周りの人にも野菜摂取を勧めてみましょう！')
    elif VGTI in ooo:
        st.info('ベジレベル★★★\n食事への意識が高いですね!これからも毎日の野菜摂取を続けましょう！')
    elif VGTI in iine:
        st.warning('ベジレベル★★\n3食の意識・野菜摂取の意識向上を目指しましょう！')
    elif VGTI in eee:
        st.error('ベジレベル★\n危険度MAX！！まずは１日３食規則正しい生活から！')
    else:
        st.error("ERROR: 不正な診断コードです")

    # 画像
    image_VGTI = {
        'RHFL': 'RHFL.png', 'RHFD': 'RHFD.png', 'RHBL': 'RHBL.png', 'REFL': 'REFL.png',
        'REFD': 'REFD.png', 'IHFL': 'IHFL.png', 'REBL': 'REBL.png', 'RHBD': 'RHBD.png',
        'IEFL': 'IEFL.png', 'IHBL': 'IHBL.png', 'REBD': 'REBD.png', 'IHFD': 'IHFD.png',
        'IEBL': 'IEBL.png', 'IEBD': 'IEBD.png', 'IEFD': 'IEFD.png', 'IHBD': 'IHBD.png'
    }

    if VGTI in image_VGTI:
        st.markdown(f"""<div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/miku2846/honohonoVGTI/main/{image_VGTI[VGTI]}" width="300" />
        <p>{VGTI}のイメージ</p></div>""", unsafe_allow_html=True)

    # 再診断ボタンを右寄せで表示
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        if st.button("もう一度ベジる🥦>>>"):
            st.session_state.step = 0
            st.session_state.VGTI = ""
            st.rerun()
