import random
import streamlit as st
import time
menu = ["Toss The Coin", "Roll The Dice"]

choice = st.sidebar.selectbox("Menu",menu)
if choice == "Toss The Coin":
    st.markdown(
        "<h3 style='font-family:Verdana; color:#4dd0e1; font-size:px;'>🪙 TOSS THE COIN</b> </h3>",
        unsafe_allow_html=True)

    if st.button("Toss"):
        placeholder = st.empty()
        for i in range(10):
            result = random.choice(["Heads", "Tails"])
            placeholder.markdown(f'## 🪙 {result}') 
            time.sleep(0.1)

        st.success(f'Final Result: 🪙 {result}')
        countdown = st.empty()
        for i in range(5, 0, -1):
            countdown.warning(f'Restarting in {i} seconds')
            time.sleep(1)
        countdown.empty()
        st.rerun()

if choice == "Roll The Dice":
    st.markdown(
            "<h3 style='font-family:Verdana; color:#4dd0e1; font-size:px;'>🎲 Roll The Dice</b> </h3>",
            unsafe_allow_html=True)
    if st.button("Roll"):
        placeholder = st.empty()
        for i in range(10):
            result = random.randint(1, 6)
            placeholder.markdown(f'## 🎲 {result}')
            time.sleep(0.1)
        st.success(f'Final Result: 🎲 {result}')
        countdown = st.empty()
        for i in range(5, 0, -1):
            countdown.warning(f'Restarting in {i} seconds')
            time.sleep(1)
        countdown.empty()
        st.rerun()