import os
import json
import random
import streamlit as st

QUESTION_FILE = "questions.json"
SAVE_FILE = "save.json"

# クイズデータの読み込み
with open(QUESTION_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

# セーブデータ読み込み関数
def load_save_data():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "used_flags": [False] * len(questions),
            "score": 0,
            "q_index": 0
        }

# 正解数の初期化
if "totalscore" not in st.session_state:
    if os.path.exists("save.json"):
        with open("save.json", "r") as f:
            data = json.load(f)
            st.session_state.totalscore = data.get("totalscore", 0)
    else:
        st.session_state.totalscore = 0


# セーブデータ保存関数
def save_progress():
    save_data = {
        "used_flags": [q.get("used", False) for q in questions],
        "score": st.session_state.score,
        "q_index": st.session_state.q_index,
        "totalscore": st.session_state.totalscore
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)

# セッション状態の初期化
save_data = load_save_data()
for i, flag in enumerate(save_data["used_flags"]):
    questions[i]["used"] = flag

if "mode" not in st.session_state:
    st.session_state.mode = None
if "q_index" not in st.session_state:
    st.session_state.q_index = save_data["q_index"]
if "score" not in st.session_state:
    st.session_state.score = save_data["score"]
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = []

# モード選択画面
if st.session_state.mode is None:
    st.title("🐍 Python Quest（基礎編）")
    st.subheader("モードを選んでください")
    if st.button("1. 全問を順に解く"):
        st.session_state.selected_questions = questions
        st.session_state.mode = "sequential"
        st.session_state.score_counted = False  # 成績表示のためのフラグ

    if st.button("2. ランダム出題（問題数を選ぶ）"):
        st.session_state.mode = "choose_random"
        st.session_state.score_counted = False
        st.rerun()

    # 成績表示ボタン
    if st.button("📊 成績を見る"):
        # セーブデータの読み込み
        try:
            with open("save.json", "r", encoding="utf-8") as f:
                save_data = json.load(f)
            used_flags = save_data.get("used_flags", [])
        except FileNotFoundError:
            used_flags = []

        correct_indices = [i for i, flag in enumerate(used_flags) if flag]

        if not correct_indices:
            st.info("まだ問題を解いていません。")
        else:
            st.success(f"これまでに {len(correct_indices)} /50 問解いています！")
            st.success(f"これまでの正解数: {st.session_state.totalscore} 問")
            # 解いた問題の表示（questions.jsonから取得）
            try:
                with open("questions.json", "r", encoding="utf-8") as f:
                    all_questions = json.load(f)

                st.markdown("### ✅ 解いた問題一覧")
                for i in correct_indices:
                    if i < len(all_questions):
                        q = all_questions[i]
                        st.markdown(f"- **{i + 1}. {q['question']}**")
            except FileNotFoundError:
                st.error("⚠️ 問題データ (questions.json) が見つかりませんでした。")

    if st.button("❌ 進捗をリセット"):
        for q in questions:
            q["used"] = False
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "used_flags": [False] * len(questions),
                "score": 0,
                "q_index": 0
            }, f, ensure_ascii=False, indent=2)
        st.session_state.totalscore = 0
        save_progress()  # ←リセット後の保存
        st.success("成績をリセットしました！")
        st.rerun()

# ランダムモード設定
elif st.session_state.mode == "choose_random":
    st.subheader("何問解きますか？")
    num = st.radio("選んでください", [10, 20, 30, 40, 50])
    if st.button("スタート"):
        unused = [q for q in questions if not q.get("used", False)]
        selected = random.sample(unused, min(num, len(unused)))
        for q in selected:
            q["used"] = True
        st.session_state.selected_questions = selected
        st.session_state.mode = "random"
        st.session_state.q_index = 0
        st.session_state.score = 0
        save_progress()
        st.rerun()

# クイズ進行
elif st.session_state.mode in ["sequential", "random"]:
    current_questions = st.session_state.selected_questions

    # クイズ終了時
    if st.session_state.q_index >= len(current_questions):
        st.balloons()
        st.write(f"🏁 終了！スコア: {st.session_state.score}/{len(current_questions)}")
        # 成績表に累計正解数を加算
        if not st.session_state.get("score_counted", False):
            st.session_state.totalscore += st.session_state.score
            st.session_state.score_counted = True  # 二重加算防止
        if st.button("最初からやり直す"):
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.mode = None
            st.session_state.selected_questions = []
            save_progress()
            st.rerun()

    # 出題中
    else:
        q = current_questions[st.session_state.q_index]
        st.title("🐍 Python 基礎クイズ")
        st.write(f"### 問題 {st.session_state.q_index + 1}: {q['question']}")
        selected = st.radio("選択肢を選んでください", q["choices"], key=st.session_state.q_index)

        if st.button("回答") and not st.session_state.answered:
            st.session_state.answered = True
            correct = q["choices"].index(selected) == q["answer_index"]
            if correct:
                st.success("正解！ 🎉")
                st.session_state.score += 1
            else:
                st.error("不正解 😢")
            st.info(f"💡 解説: {q['explanation']}")

            # 成績の保存
            save_progress()

        if st.session_state.answered:
            if st.button("次の問題へ"):
                st.session_state.q_index += 1
                st.session_state.answered = False
                save_progress()
                st.rerun()

