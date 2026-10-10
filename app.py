import streamlit as st
import pandas as pd
import numpy as np

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
    for i, n in enumerate(np.random.randint(0, 10, size=25)):
        s, c = classify_num(int(n))
        data.append({"Period": str(base_p + i), "Number": int(n), "Size": s, "Color": c})
    st.session_state.history = data

st.title("⚡ Wingo 1-Min AI Panel")

# Sidebar - Manual Entry
st.sidebar.header("Add Result")
with st.sidebar.form("add_form", clear_on_submit=True):
    p_in = st.text_input("Period", value=str(int(st.session_state.history[-1]["Period"]) + 1))
    n_in = st.number_input("Number (0-9)", min_value=0, max_value=9, value=0)
    if st.form_submit_button("Submit"):
        s, c = classify_num(int(n_in))
        st.session_state.history.append({"Period": str(p_in), "Number": int(n_in), "Size": s, "Color": c})
        st.rerun()

if st.sidebar.button("Simulate +5 Rounds"):
    last_p = int(st.session_state.history[-1]["Period"])
    for i in range(1, 6):
        rn = int(np.random.randint(0, 10))
        s, c = classify_num(rn)
        st.session_state.history.append({"Period": str(last_p + i), "Number": rn, "Size": s, "Color": c})
    st.rerun()

# Dashboard Data & Analytics
df = pd.DataFrame(st.session_state.history)
last_rec = df.iloc[-1]

sizes = df["Size"].tolist()
b_count = sizes[-10:].count("Big")
s_count = 10 - b_count
pred = "Small" if b_count > s_count else "Big"
conf = max(b_count, s_count) * 10

st.info(f"### Next Predicted: **{pred}** (Confidence: {conf}%)")

c1, c2, c3 = st.columns(3)
c1.metric("Last Period", last_rec["Period"])
c2.metric("Last Number", f"{last_rec['Number']} ({last_rec['Size']})")
c3.metric("Big Ratio", f"{(df['Size']=='Big').mean()*100:.1f}%")

st.write("---")

st.write("### Number Frequency Chart")
counts = df["Number"].value_counts().sort_index()
st.bar_chart(counts)

st.write("### Recent History")
st.dataframe(df.tail(10).iloc[::-1], use_container_width=True, hide_index=True)
