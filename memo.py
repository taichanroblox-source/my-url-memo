import streamlit as st
import os
from collections import defaultdict

# 🔑 Streamlitの管理画面（Secrets）から安全にパスワードを読み込む
# ローカル環境で動かすとき（Secrets未設定時）は、一時的に右側のパスワードが使われます
PASSWORD = st.secrets.get("password", "taisukE2015")

st.title("📦 ボックス分けURL管理メモ")

# --- 🔐 ログインチェック機能 ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔒 パスワードを入力してください")
    input_pass = st.text_input("Password:", type="password") # type="password" で文字を伏せ字にします
    
    if st.button("ログイン"):
        if input_pass == PASSWORD:
            st.session_state.logged_in = True
            st.success("ログイン成功！")
            st.rerun()
        else:
            st.error("パスワードが違います！")
    
    # ログインしていない場合はここでプログラムを終了（これ以降の画面を見せない）
    st.stop()

# --- 🔓 ログイン成功後のみ以下の管理画面が表示される ---
st.sidebar.success("🔑 ログイン中")
if st.sidebar.button("ログアウト"):
    st.session_state.logged_in = False
    st.rerun()

MEMO_FILE = "my_memo.txt"

# 1. 既存のデータを読み込んで「ボックスごと」に分類する
box_data = defaultdict(list)

if "custom_boxes" not in st.session_state:
    st.session_state.custom_boxes = []

if os.path.exists(MEMO_FILE):
    with open(MEMO_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and "," in line:
                box_name, url = line.split(",", 1)
                box_data[box_name.strip()].append(url.strip())

# データの保存・更新用ヘルパー関数
def save_all_data(data_dict):
    with open(MEMO_FILE, "w", encoding="utf-8") as f:
        for box, urls in data_dict.items():
            for url in urls:
                f.write(f"{box},{url}\n")

# URLの一括追加処理を行うヘルパー関数
def add_urls_to_box(box_name, urls_text):
    if not urls_text.strip():
        st.warning("URLが入力されていません。")
        return
        
    raw_urls = urls_text.split()
    added_count = 0
    duplicate_count = 0
    invalid_urls = []
    
    for raw_url in raw_urls:
        url = raw_url.strip()
        if url:
            if not (url.startswith("http://") or url.startswith("https://")):
                invalid_urls.append(url)
                continue
                
            if url in box_data[box_name]:
                duplicate_count += 1
            else:
                box_data[box_name].append(url)
                added_count += 1
                
    save_all_data(box_data)
    
    if box_name in st.session_state.custom_boxes and added_count > 0:
        st.session_state.custom_boxes.remove(box_name)
    
    if added_count > 0:
        st.success(f"「{box_name}」に {added_count} 個のURLを追加しました！")
    if duplicate_count > 0:
        st.error(f"{duplicate_count} 個のURLはすでに「{box_name}」に入っていたためスキップしました。")
    if invalid_urls:
        for bad_url in invalid_urls:
            st.error(f"これはURLではありません：{bad_url}")

# 2. 【最上段】新規ボックス作成専用のエリア
st.subheader("📁 新しいボックスを作る")
new_box_name = st.text_input("新しいボックスの名前（例：プロキシ、動画など）:", key="new_box_input").strip()

if st.button("新しいボックスを開設する"):
    if new_box_name:
        if new_box_name in box_data or new_box_name in st.session_state.custom_boxes:
            st.warning(f"「{new_box_name}」はすでに存在します。")
        else:
            st.session_state.custom_boxes.append(new_box_name)
            st.success(f"ボックス「{new_box_name}」を作成しました！")
            st.rerun()
    else:
        st.warning("ボックス名を入力してください。")

st.divider()

# 3. ボックスごとにURLを表示 ＆ ボックス内直接入力 ＆ 削除処理
st.subheader("📦 現在のボックス一覧")

all_box_names = list(box_data.keys()) + st.session_state.custom_boxes
all_box_names = list(set(all_box_names))

if all_box_names:
    for box_name in all_box_names:
        urls = box_data[box_name]
        
        with st.expander(f"📁 {box_name} ({len(urls)}個のURL)", expanded=True):
            inline_input = st.text_area(
                f"「{box_name}」にURLを追加：", 
                key=f"input_inline_{box_name}",
                height=68,
                label_visibility="collapsed"
            )
            
            col_add, col_del = st.columns([0.7, 0.3])
            with col_add:
                if st.button(f"➕ この「{box_name}」ボックスに追加", key=f"btn_inline_add_{box_name}"):
                    add_urls_to_box(box_name, inline_input)
                    st.rerun()
            with col_del:
                if st.button(f"🚨 ボックスを丸ごと削除", key=f"del_box_{box_name}"):
                    if box_name in box_data:
                        del box_data[box_name]
                    if box_name in st.session_state.custom_boxes:
                        st.session_state.custom_boxes.remove(box_name)
                    save_all_data(box_data)
                    st.rerun()
            
            st.write("---")
            
            for i, url in enumerate(urls):
                col1, col2 = st.columns([0.85, 0.15])
                with col1:
                    st.markdown(f"- [{url}]({url})")
                with col2:
                    if st.button("🗑️ 削除", key=f"del_url_{box_name}_{i}"):
                        box_data[box_name].remove(url)
                        if not box_data[box_name]:
                            if box_name in box_data:
                                del box_data[box_name]
                        save_all_data(box_data)
                        st.rerun()
else:
    st.info("まだボックスがありません。一番上のフォームから作成してください。")
