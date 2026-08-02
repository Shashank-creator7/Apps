import random
import streamlit as st
import time
menu = ["Toss The Coin", "Roll The Dice",  "About"]

choice = st.sidebar.selectbox("Menu",menu)
if choice == "Toss The Coin":
    st.markdown(
        "<h3 style='font-family:Verdana; color:#4dd0e1; font-size:px;'>🪙 TOSS THE COIN</b> </h3>",
        unsafe_allow_html=True)

    userchoice = st.radio("Choose your side:", ["Heads", "Tails"])
    if st.button("Toss"):
        placeholder = st.empty()
        for i in range(10):
            result = random.choice(["Heads", "Tails"])
            # placeholder.markdown(f'## 🪙 {result}') 
            if userchoice == result:
                placeholder.success(f'## 🪙 {result} - You Win!')
            else:
                placeholder.error(f'## 🪙 {result} - Opponent Wins!')
            time.sleep(0.1)
            

        # st.info(f'Final Result: 🪙 {result}')
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
# if choice == "Rock Paper Scissors":
#     st.markdown(
#         "<h3 style='font-family:Verdana; color:#4dd0e1; font-size:px;'>✊ Rock Paper Scissors</b> </h3>",
#         unsafe_allow_html=True)
#     user_choice = st.radio("Choose your move:", ["Rock", "Paper", "Scissors"])
#     if st.button("Play"):
#         computer_choice = random.choice(["Rock", "Paper", "Scissors"])
#         st.write(f"Computer chose: {computer_choice}")
#         if user_choice == computer_choice:
#             st.warning("It's a tie!")
#         elif (user_choice == "Rock" and computer_choice == "Scissors") or \
#              (user_choice == "Paper" and computer_choice == "Rock") or \
#              (user_choice == "Scissors" and computer_choice == "Paper"):
#             st.success("You win!")
#         else:
#             st.error("You lose!")
if choice == "About":
    st.markdown(
        "<h3 style='font-family:Verdana; color:#4dd0e1; font-size:px;'>About</b> </h3>",
        unsafe_allow_html=True)
    st.write("This is a simple app to toss a coin or roll a dice. It is built using Streamlit and Python." \
    "You can choose your side for the coin toss or roll the dice and see the result. Enjoy!" \
    "\n\nMade with ❤️ by [Shashank Sul ](https://github.com/Shashank-creator7).")