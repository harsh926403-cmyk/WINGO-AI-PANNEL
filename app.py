 import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter

st.set_page_config(page_title="Wingo AI Panel", layout="wide")

def classify_num(n):
    size = "Big" if n >= 5 else "Small"
    if n in [1, 3, 7, 9]:
        col = "Green"
    elif n in [2, 4, 6, 8]:
        col = "Red"
    elif n == 0:
        col = "Red+Violet"
    else:
        col = "Green+Violet"
    return size, col

if "history" not in st.session_state:
    data = []
    base_p = 20261010001
    np.random.seed(42)
    for i, n in enumerate(np.random.randint(0, 10, size=30)):
        s, c = classify_num(int(n))
        data.append({"Period": str(base_p + i), "Number": int(n), "Size": s, "Color": c})
    st.session_state.history = data

st.title("⚡ Wingo AI Advanced Panel")

# Sidebar Controls
st.sidebar.header("🕹️ Controls")
with st.sidebar.form("add_form", clear_on_submit=True):
    p_in = st.text_input("Period Number", value=str(int(st.session_state.history[-1]["Period"]) + 1))
    n_in = st.number_input("Result Number (0-9)", min_value=0, max_value=9, value=0)
    if st.form_submit_button("➕ Add Result"):
        s, c = classify_num(int(n_in))
        st.session_state.history.append({"Period": str(p_in), "Number": int(n_in), "Size": s, "Color": c})
        st.rerun()

if st.sidebar.button("🎲 Simulate +5 Rounds"):
    last_p = int(st.session_state.history[-1]["Period"])
    for i in range(1, 6):
        rn = int(np.random.randint(0, 10))
        s, c = classify_num(rn)
        st.session_state.history.append({"Period": str(last_p + i), "Number": rn, "Size": s, "Color": c})
    st.rerun()

df = pd.DataFrame(st.session_state.history)
last_rec = df.iloc[-1]
recent_15 = df.tail(15)

# Size Prediction & Streak
sizes = df["Size"].tolist()
b_count = sizes[-10:].count("Big")
s_count = 10 - b_count
pred_size = "Small" if b_count > s_count else "Big"
size_conf = max(b_count, s_count) * 10

current_streak_type = sizes[-1]
streak_count = 0
for s in reversed(sizes):
    if s == current_streak_type:
        streak_count += 1
    else:
        break

# Number Prediction
num_counts = Counter(recent_15["Number"].tolist())
hot_nums = [num for num, _ in num_counts.most_common(3)]
candidate_nums = [n for n in range(5, 10)] if pred_size == "Big" else [n for n in range(0, 5)]

primary_pred_num = next((n for n in hot_nums if n in candidate_nums), candidate_nums[0])
secondary_pred_num = next((n for n in candidate_nums if n != primary_pred_num), candidate_nums[1])

# UI Boxes
col1, col2 = st.columns(2)
with col1:
    st.subheader("🎯 Size Prediction")
    st.info(f"### Next Size: **{pred_size}**\n**Confidence:** `{size_conf}%`\n\n**Current Streak:** `{streak_count}x {current_streak_type}`")

with col2:
    st.subheader("🔢 Number Prediction")
    st.success(f"### Best Numbers: **{primary_pred_num}** & **{secondary_pred_num}**\n**Target Category:** `{pred_size}`\n\n**Top Hot Number:** `{hot_nums[0] if hot_nums else 'N/A'}`")

st.write("---")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Last Period", last_rec["Period"])
m2.metric("Last Number", f"{last_rec['Number']} ({last_rec['Size']})")
m3.metric("Last Color", last_rec["Color"])
m4.metric("Big Ratio", f"{(df['Size']=='Big').mean()*100:.1f}%")

st.write("---")
st.subheader("📊 Number Frequency Distribution")
st.bar_chart(df["Number"].value_counts().sort_index())

st.subheader("📜 Recent History")
st.dataframe(df.tail(10).iloc[::-1], use_container_width=True, hide_index=True)
