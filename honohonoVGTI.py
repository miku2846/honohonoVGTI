import streamlit as st

# --- 絵文字アニメーション用のCSS ---
st.markdown(
    """
    <style>
    .emoji {
        display: inline-block; /* インライン要素をブロック要素のように扱いつつ、テキストの流れを維持 */
    }

    .wiggle {
        animation: wiggle 0.5s infinite alternate; /* wiggleアニメーションを0.5秒間隔で無限に繰り返す */
    }

    @keyframes wiggle {
        0% { transform: rotate(-5deg); }   /* 開始時: -5度回転 */
        100% { transform: rotate(5deg); }  /* 終了時: 5度回転 */
    }
    </style>
    """,
    unsafe_allow_html=True, # HTMLタグを安全でないものとして許可（<style>タグを使うため必須）
)

# --- アニメーションする絵文字を含むタイトル ---
st.markdown(
    f'<h1 style="display: flex; align-items: center; justify-content: center;">'
    f'<span class="emoji wiggle">🍅</span> '
    f'VGTI 診断 '
    f'<span class="emoji wiggle">🍆</span>'
    f'</h1>',
    unsafe_allow_html=True, # HTMLタグを安全でないものとして許可
)

# 質問と選択肢・結果の対応（[質問文, 選択肢リスト, 選択肢ごとのタイプ文字])
questions = [
    ('普段の生活リズムについて教えてください。',
     ['1日3食きちんと食べている', '1日1食or2食になってしまう...(食事の時間が不規則になりがち)'],
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
    st.session_state.answers = {} # 各質問の状態を保持するための辞書を初期化

step = st.session_state.step

if step < len(questions):
    q, options, codes = questions[step]
    st.subheader(f"Q{step + 1}. {q}")
        
    # ここを変更！「選択してください」のダミー選択肢を削除
    # display_options = ["選択してください"] + options は不要に

    # ユーザーが以前に選択した回答があれば、それを初期値にする
    # なければ、st.radio のデフォルト挙動（リストの最初の要素が選択される）になる
    default_index = 0
    if f"q{step}" in st.session_state.answers:
        try:
            # 以前の選択肢のインデックスを直接使う
            default_index = options.index(st.session_state.answers[f"q{step}"])
        except ValueError:
            default_index = 0

    # ここを変更！display_options ではなく options を直接渡す
    choice = st.radio("選択してください", options, index=default_index, key=f"q{step}_radio")

   
    if st.button("次へ ▶"): # ここを変更！条件分岐をシンプルに
        # アスタリスクを除いた元の選択肢のテキストを使ってインデックスを取得
        original_choice_text = choice.replace(" *", "")
        selected_index_in_original_options = options.index(original_choice_text) # ここはそのまま
        st.session_state.VGTI += codes[selected_index_in_original_options]
        st.session_state.step += 1
        st.session_state.answers[f"q{step}"] = original_choice_text
        st.rerun()

# 結果表示（省略。変更なし）
else:
    VGTI = st.session_state.VGTI
    st.header(f"あなたのVGTIタイプは: {VGTI} 🌱")

    wao = {'RHFL', 'RHFD', 'RHBL', 'REFL'}
    ooo = {'REFD', 'IHFL', 'REBL', 'RHBD'}
    iine = {'IEFL', 'IHBL', 'REBD', 'IHFD'}
    eee = {'IEBL', 'IEBD', 'IEFD', 'IHBD'}

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

    st.markdown("""
        <style>
        div.stButton > button {
            display: block;
            margin-left: auto;
            margin-right: 0;
            width: fit-content;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("もう一度ベジる🥦>>>"):
        st.session_state.step = 0
        st.session_state.VGTI = ""
        st.session_state.answers = {}
        st.rerun()

