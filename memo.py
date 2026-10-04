import streamlit as st

st.set_page_config(page_title="📦 ボックス分けURL管理メモ", layout="wide")
st.title("📦 ボックス分けURL管理メモ")

# データの初期化（最強リスト＋新お宝URLも最初から入れておいたよ！）
if "kv_storage" not in st.session_state:
    st.session_state.kv_storage = {
        "urls_動画": [
            "https://google.com",
            "https://hospitaldelninodif.gob.mx",
            "https://google.com",
            "https://google.com",
            "https://workers.dev",
            "https://railway.appmi"
        ],
        "urls_プロキシ": [
            "https://kos-kosan.tk",  # 👈 最高な新プロキシをここに追加！
            "https://smartproxy.kr", "https://workers.devmi", "https://workers.devmi",
            "https://workers.devmi", "https://learnnexus.xyzmi", "https://oldmillschool.orgmi",
            "https://jsdelivr.net", "https://pilotrights.com",
            "https://amazonaws.com", "https://amazonaws.com",
            "https://googleapis.com", "https://berugy.humi",
            "https://shela.numi", "https://com.armi", "https://googleapis.com",
            "https://co.ukmi", "https://sugamo-kotobuki.commi", "https://pmilbd.commi",
            "https://sevecom.commi", "https://olivrr.commi", "https://thundernova.ca",
            "https://plating.ru", "https://rolotec.ro", "https://moolah.asiami",
            "https://scoffin.orgmi", "https://onrender.commi", "https://onrender.commi"
        ],
        "urls_ダウンローダー": [
            "https://turboscribe.ai",
            "https://kol.id",
            "https://acethinker.jp"
        ],
        "urls_ゲーム＆仮想OS": [
            "https://historyspot.net",
            "https://dailytoolz.com",
            "https://duckmath.com",
            "https://viatasks.commi"
        ],
        "box_names": ["動画", "プロキシ", "ダウンローダー", "ゲーム＆仮想OS"]
    }

db = st.session_state.kv_storage

# --- 📁 新しいボックスの作成 ---
st.subheader("📁 新しいボックスを作る")
new_box_name = st.text_input("ボックスの名前:", key="new_box_input").strip()

if st.button("新しいボックスを開設する"):
    if new_box_name and new_box_name not in db["box_names"]:
        db["box_names"].append(new_box_name)
        db[f"urls_{new_box_name}"] = []
        st.success(f"ボックス「{new_box_name}」を作ったよ！")
        st.rerun()

st.divider()

# --- 📦 ボックスごとにURLを表示 ---
st.subheader("📦 現在のボックス一覧")
for b_name in db["box_names"]:
    urls = db.get(f"urls_{b_name}", [])
    
    # ✨ 修正ポイント：st.expanderの代わりに、状態を記憶できるst.toggleを使用！
    # value=True にしてるから、最初は全部開いた状態でスタートするよ
    is_open = st.toggle(f"📁 {b_name} ({len(urls)}個のURL)", value=True, key=f"toggle_{b_name}")
    
    if is_open:
        # ボックスの中身を少し見やすく囲うためのコンテナ
        with st.container(border=True):
            inline_input = st.text_area(f"「{b_name}」にURLを追加：", key=f"input_{b_name}", height=68, label_visibility="collapsed")
            
            col_add, col_del = st.columns([0.8, 0.2])
            with col_add:
                if st.button(f"➕ 「{b_name}」に追加", key=f"add_{b_name}"):
                    if inline_input.strip():
                        for raw_url in inline_input.split():
                            url = raw_url.strip()
                            if url and url not in urls:
                                urls.append(url)
                        db[f"urls_{b_name}"] = urls
                        st.rerun()
            with col_del:
                if st.button(f"🚨 ボックス削除", key=f"del_box_{b_name}"):
                    db["box_names"].remove(b_name)
                    if f"urls_{b_name}" in db:
                        del db[f"urls_{b_name}"]
                    st.rerun()
            
            st.write("")
            for i, url in enumerate(urls):
                col_url, col_btn = st.columns([0.95, 0.05])
                with col_url:
                    if url.endswith("mi"):
                        st.markdown(f"- ⚠️未検証: [{url}]({url})")
                    else:
                        st.markdown(f"- [{url}]({url})")
                with col_btn:
                    if st.button("🗑️", key=f"del_url_{b_name}_{i}"):
                        urls.remove(url)
                        db[f"urls_{b_name}"] = urls
                        st.rerun()
    st.write("") # ボックスごとのすき間あけ
