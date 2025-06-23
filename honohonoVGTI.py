import streamlit as st
import gspread
from datetime import datetime
import json
import pytz

# --- 絵文字アニメーション用のCSS ---
st.markdown(
    """
    <style>
    .emoji {
        display: inline-block;
    }

    .wiggle {
        animation: wiggle 0.5s infinite alternate;
    }

    @keyframes wiggle {
        0% { transform: rotate(-5deg); }
        100% { transform: rotate(5deg); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- アニメーションする絵文字を含むタイトル ---
st.markdown(
    f'<h1 style="display: flex; align-items: center; justify-content: center;">'
    f'<span class="emoji wiggle">🍅</span> '
    f'VGTI 診断 '
    f'<span class="emoji wiggle">🍆</span>'
    f'</h1>',
    unsafe_allow_html=True,
)

# --- Google Sheets 接続設定 ---
GOOGLE_SHEET_ID = "1t6--DOwsN4Te47Yv6QqsZDWRLGfY4S7UVi78BAD5JHI" 

@st.cache_resource
def get_gspread_client():
    try:
        credentials_dict = st.secrets["gsheets_service_account"]
        gc = gspread.service_account_from_dict(credentials_dict)
        return gc
    except Exception as e:
        st.error(f"Google Sheetsの認証に失敗しました。認証情報をご確認ください: {e}")
        st.stop()

gc = get_gspread_client()

try:
    spreadsheet = gc.open_by_key(GOOGLE_SHEET_ID)
except gspread.exceptions.SpreadsheetNotFound:
    st.error(f"指定されたIDのGoogleスプレッドシートが見つかりません。IDを確認してください: {GOOGLE_SHEET_ID}")
    st.stop()
except Exception as e:
    st.error(f"スプレッドシートへのアクセス中にエラーが発生しました。権限やIDを確認してください: {e}")
    st.stop()

# --- スプレッドシートのデータをキャッシュして読み込む関数 ---
# 1時間(3600秒)ごとにキャッシュをクリア
@st.cache_data(ttl=3600)
def get_all_spreadsheet_data(_worksheet_obj): # 引数名を_で始める
    """スプレッドシートの全データをキャッシュして取得する関数"""
    return _worksheet_obj.get_all_values()

# 質問と選択肢・結果の対応
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
    st.session_state.answers_list = []
    st.session_state.result_logged = False 

# 質問の表示と回答の収集
if st.session_state.step < len(questions):
    q_data = questions[st.session_state.step]
    q_text, options, codes = q_data[0], q_data[1], q_data[2]
    
    st.subheader(f"Q{st.session_state.step + 1}. {q_text}")
        
    default_index = 0
    if st.session_state.step < len(st.session_state.answers_list):
        try:
            default_index = options.index(st.session_state.answers_list[st.session_state.step])
        except ValueError:
            default_index = 0

    choice = st.radio("選択してください", options, index=default_index, key=f"q{st.session_state.step}_radio")

    if st.button("次へ ▶"): 
        selected_index = options.index(choice)
        st.session_state.VGTI += codes[selected_index]

        if st.session_state.step < len(st.session_state.answers_list):
            st.session_state.answers_list[st.session_state.step] = choice
        else:
            st.session_state.answers_list.append(choice)

        st.session_state.step += 1
        st.rerun()

# 結果表示
else:
    final_VGTI = st.session_state.VGTI
    st.header(f"あなたのVGTIタイプは: {final_VGTI} 🌱")

    wao = {'RHFL', 'RHFD', 'RHBL', 'REFL'}
    ooo = {'REFD', 'IHFL', 'REBL', 'RHBD'}
    iine = {'IEFL', 'IHBL', 'REBD', 'IHFD'}
    eee = {'IEBL', 'IEBD', 'IEFD', 'IHBD'}

    result_message = ""
    if final_VGTI in wao:
        result_message = 'ベジレベル★★★★\n1日3食食べていて素晴らしい！周りの人にも野菜摂取を勧めましょう！'
        st.success(result_message)
    elif final_VGTI in ooo:
        result_message = 'ベジレベル★★★\n食事への意識が高いですね!これからも毎日の野菜摂取を続けましょう！'
        st.info(result_message)
    elif final_VGTI in iine:
        result_message = 'ベジレベル★★\n3食の意識・野菜摂取の意識向上を目指しましょう！'
        st.warning(result_message)
    elif final_VGTI in eee:
        result_message = 'ベジレベル★\n危険度MAX！！まずは１日３食規則正しい生活から！'
        st.error(result_message)
    else:
        result_message = "ERROR: 不正な診断コードです"
        st.error(result_message)

    # --- Google Sheetsへの結果書き込み処理 ---
    if not st.session_state.result_logged:
        try:
            tokyo = pytz.timezone("Asia/Tokyo")
            now_tokyo = datetime.now(tokyo)
            # テスト用に日付を強制的に進める場合は、以下の行をコメントアウト解除
            # from datetime import timedelta # これもファイルの先頭に移動済み
            # now_tokyo = now_tokyo + timedelta(days=1) 
            
            current_date_str = now_tokyo.strftime("%Y-%m-%d") 

            # シート名を日付にする
            sheet_name = current_date_str 

            # シートを取得、存在しない場合は新規作成
            try:
                worksheet = spreadsheet.worksheet(sheet_name)
                # 新しいシートが作成された際にキャッシュをクリアする
                get_all_spreadsheet_data.clear() 
            except gspread.exceptions.WorksheetNotFound:
                # シートが存在しない場合は新規作成
                # ヘッダー行なしでデータ用2列のシートを確保 (VGTIタイプ, 人数)
                worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=2) 
                # ヘッダー行を追加 (日付列は不要になったので削除)
                worksheet.append_row(["VGTIタイプ", "人数"]) # ★ここを修正★
                # 新しく作成されたシートのデータもキャッシュから取得し直す
                get_all_spreadsheet_data.clear() 

            # スプレッドシートの全データをキャッシュから取得
            all_records = get_all_spreadsheet_data(worksheet)
            
            # ヘッダー行を除いた実際のデータ
            data_rows = all_records[1:] if len(all_records) > 1 else []
            
            # 既存のデータと一致する行を探す
            found_row_index = -1
            current_count = 0 
            
            for i, row in enumerate(data_rows):
                # ★ここを修正★ row[0]がVGTIタイプになった
                # VGTIタイプがあることを確認 (以前のrow[1]がrow[0]になる)
                if len(row) > 0 and row[0] == final_VGTI: # 以前はrow[1] == final_VGTI
                    found_row_index = i + 2 # スプレッドシートの行番号 (ヘッダー行1 + 0始まりインデックス)
                    # 既存の人数カウントを取得 (C列、インデックスは2 → 新しいシートではB列、インデックスは1)
                    try:
                        current_count = int(row[1]) # ★ここを修正★ 以前はrow[2]
                    except (ValueError, IndexError):
                        current_count = 0 
                    break
            
            new_count = current_count + 1

            # 書き込むデータ (ヘッダー: VGTIタイプ, 人数)
            data_to_write = [
                final_VGTI, # ★ここを修正★ 日付はシート名にあるので削除
                new_count 
            ]

            if found_row_index != -1:
                # 既存の行を更新 (C列の人数だけ更新 → 新しいシートではB列)
                worksheet.update_cell(found_row_index, 2, new_count) # ★ここを修正★ 列番号(2はB列)
            else:
                # 新しい行を追加
                worksheet.append_row(data_to_write)

            st.session_state.result_logged = True
            
        except Exception as e:
            st.warning(f"結果の記録に失敗しました。認証情報、スプレッドシートID、共有設定を確認してください。エラー: {e}")
    # --- Google Sheetsへの結果書き込み処理 終わり ---


    # --- 画像表示とボタンのCSS ---
    image_VGTI = {
        'RHFL': 'RHFL.png', 'RHFD': 'RHFD.png', 'RHBL': 'RHBL.png', 'REFL': 'REFL.png',
        'REFD': 'REFD.png', 'IHFL': 'IHFL.png', 'REBL': 'REBL.png', 'RHBD': 'RHBD.png',
        'IEFL': 'IEFL.png', 'IHBL': 'IHBL.png', 'REBD': 'REBD.png', 'IHFD': 'IHFD.png',
        'IEBL': 'IEBL.png', 'IEBD': 'IEBD.png', 'IEFD': 'IEFD.png', 'IHBD': 'IHBD.png'
    }

    if final_VGTI in image_VGTI:
        st.markdown(f"""<div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/miku2846/honohonoVGTI/main/{image_VGTI[final_VGTI]}" width="300" />
        <p>{final_VGTI}のイメージ</p></div>""", unsafe_allow_html=True)

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
        st.session_state.answers_list = []
        st.session_state.result_logged = False
        # キャッシュをクリアする
        get_all_spreadsheet_data.clear() 
        st.rerun()