import random
import streamlit as st
import time

st.title("🪙 TOSS THE COIN ")

if st.button("Toss"):
    placeholder = st.empty()
    for i in range(10):
        result = random.choice(["Heads", "Tails"])
        placeholder.markdown(f'## 🪙 {result}') 
        time.sleep(0.1)

    st.success(f'Final Result: 🪙 {result}')