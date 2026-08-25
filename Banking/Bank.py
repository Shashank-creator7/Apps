# Import requrired libraries--------
import streamlit as st
import numpy as np
import pandas as pd
import csv
import time
import datetime
# ------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state['logged_in'] = False

menu = ["Login", "Signup", "Forgot Password", "About"]
# Login system for banking application
choice = st.sidebar.selectbox("User Menu", menu )

if choice == 'Login':
    if not st.session_state["logged_in"]:
        st.subheader("Login")
        username = st.text_input("Username", key = "login_username")
        password = st.text_input("Password", type="password", key = "login_password")

        st.button("Login", key = "login_button")

        found = False
        with open("baccounts.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"] == username and row["Password"] == password:
                    found = True
                    break

            if found:
                st.session_state["logged_in"] = True
                st.success("Login successfully !")
                countdown = st.empty()
                for i in range(3, 0, -1):
                    countdown.info(f'Logging in {i} seconds')
                    time.sleep(1)
                countdown.empty()
                st.rerun()
        
                st.session_state["username"] = ""
                st.session_state["password"] = ""
                st.rerun()
            else:
                if username and password:
                    st.error("Invalid Credintial")
                    st.write("If you forgot your password, go to Forgot Password option")

elif choice == ("Forgot Password"):
    if not st.session_state["logged_in"]:
        st.subheader("Security Questions")
        username = st.text_input("Username :")
        sq1 = st.text_input("Who is your favourite teacher :")
        sq2 = st.text_input("What is your favourite subject :")
        if st.button("Submit"):

            found = False
            with open("accounts.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Username"] == username:
                        found = True
                        break
            if found:
                if sq1 in row["SQ1"] and sq2 in row["SQ2"]:
                    st.success(f"Correct answers. Your password is - {row['Password']}")
                    
                else:
                    st.error("Incorrect answer(s). Please try again.")
            else:
                st.info("Username not found. Please try again!")
    else:
        st.popover("# Logout first to switch choice in User Menu")


if st.session_state["logged_in"]:
    st.markdown(
            "<h3 style='font-family:lato ; color:#4dd0e1; font-size:40px;'>💰Bank Management System</h3>",
            unsafe_allow_html=True)
    menu = ["Account Activity", "Loan", "FD", "About"] 
    choice = st.sidebar.selectbox("App Menu", menu)

    if choice == "Account Activity":
        st.markdown(
                    "<h3 style='font-family:verdana ; color:#FD2629; font-size:30px;'>Account Acticity</h3>",
                    unsafe_allow_html=True)
        choice = st.radio("Choose your action:", ["Withdraw", "Deposit", "Show Balance"])
        if choice == "Withdraw":
            st.markdown(
                "<h3 style='font-family:verdana ; color:#FD2629; font-size:30px;'>Withdraw</h3>",unsafe_allow_html=True)
            amount = st.number_input("Amount" , min_value=0, step=1)
            if st.button("Withdraw"):
                with open ("balance.txt", 'r') as file:
                    balance = int(file.read())
                    file.close()
                if amount <= balance:
                    balance -= amount
                    with open ("balance.txt","w") as file:
                        file.write(str(balance))
                        file.close()
                        st.success("Transaction successful. Available balance is ₹" + str(balance))
                else:
                    st.error("Insufficient balance. Available balance is ₹" + str(balance))
        elif choice == "Deposit":
            st.markdown(
                    "<h3 style='font-family:verdana ; color:#FD2629; font-size:30px;'>Deposit</h3>",
                    unsafe_allow_html=True)
            amount = st.number_input("Amount" , min_value=0, step=1)
            if st.button("Deposit"):
                with open ("balance.txt", 'r') as file:
                    balance = int(file.read())
                    file.close()
                balance += amount
                with open ("balance.txt", "r") as file:
                    balance = int(file.read())
                    file.close()
                balance += amount
                with open ("balance.txt", 'w') as file:
                    file.write(str(balance))
                    file.close()
                st.success("Available balance is ₹" + str(balance))
        elif choice == "Show Balance":
            with open("balance.txt", "r") as file:
                balance = int(file.read())
                st.info("available balance is ₹"+str(balance))

    elif choice == "Loan":
        st.markdown(
                    "<h3 style='font-family:verdana ; color:#FD2629; font-size:30px;'>Loan</h3>",
                    unsafe_allow_html=True)
        choice = st.radio("Choose your action:", ["Apply for Loan", "Loan Applicators"])
        if choice == "Apply for Loan":
            st.markdown(
                    "<h3 style='font-family:verdana ; color:#6EFD66; font-size:25px;'>Loan Application</h3>",
                    unsafe_allow_html=True)
            choice = st.radio("Enter:", ["Secured Loan", "Unsecured Loan"])
            if choice == "Secured Loan":
                st.markdown(
                    "<h3 style='font-family:verdana ; color:#6EFD66; font-size:20px;'>💰Secured Loan</h3>",unsafe_allow_html=True)
                name = st.text_input("Name :")
                amount = st.number_input("Amount  :", min_value=0, step=1)
                income = st.number_input("Salary :", min_value=0, step=1)
                property = st.number_input("Property Value :", min_value=0, step=1)
                tenure = st.number_input("Tenure (in years) :", min_value=1, step=1)
                date = st.datetime_input("Date", datetime.datetime.now())
                if st.button("Apply"):
                    if property / 100*80 >= amount:
                        emi = int((amount + (amount / 100*9)) / (tenure * 12))
                        if emi <= income:
                            st.success("Loan approved! Your EMI is ₹" + str(emi))
                            with open("loan_sl.csv", "a", newline="") as file:
                                fieldnames = ["Name", "Amount", "Income", "Property Value", "Tenure", "EMI", "Type","Date"]
                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                if file.tell() == 0:
                                    writer.writeheader()
                                writer.writerow({"Name": name, "Amount": amount, "Income": income, "Property Value": property, "Tenure": tenure, "EMI": emi, "Type": "Secured Loan", "Date" : date})
                            
                            rows =[]
                            for year in range (1, tenure+1):
                                closing_balance = amount-(emi*12*year)
                                if closing_balance<0:
                                    closing_balance = 0
                                rows.append([year,emi,closing_balance])
                            df = pd.DataFrame(rows, columns=["Year", "EMI", "Closing Balance"])
                            st.table(df)
                        
                        else:
                            st.error("Loan not approved. EMI exceeds your monthly income.")
                    else:
                        st.error("Loan not approved. Property value is insufficient for the requested loan amount.")
            elif choice == "Unsecured Loan":
                st.markdown(
                    "<h3 style='font-family:verdana ; color:#6EFD66; font-size:20px;'>💰Unsecured Loan</h3>",
                    unsafe_allow_html=True)
                name = st.text_input("Name :")
                amount = st.number_input("Amount :", min_value=0, step=1)
                if amount > 1000000:
                    st.error("Loan is available upto ₹100,000,0 only")
                salary = st.number_input("Salary", min_value=0, step=10)
                
                ITR = st.number_input("ITR (profit of 3 yrs) :", min_value=0, step=1)
                tenure = st.number_input("Enter the tenure in years :", min_value=1, step=1)
                date = st.datetime_input("Date", datetime.datetime.now())
                if st.button("Apply"):
                    if amount <= 1000000:
                        if amount>= ITR/60*100:
                            emi = int((amount + (amount / 100*12)) / (tenure*12))
                            if emi <= salary:
                                st.success("Loan approved! Your EMI is ₹" + str(emi))
                                with open("loan_ul.csv", "a", newline="") as file:
                                    fieldnames = ["Name", "Amount", "Salary", "ITR", "Tenure", "EMI", "Type","Date"]
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    if file.tell() == 0:
                                        writer.writeheader()
                                    writer.writerow({"Name": name, "Amount": amount, "Salary": salary, "ITR": ITR, "Tenure": tenure, "EMI": emi, "Type": "Unsecured", "Date" : date})
                                rows =[]
                                for year in range (1,tenure+1):
                                    closing_balance = amount-(emi*12*year)
                                    if closing_balance<0:
                                        closing_balance=0
                                    rows.append([year,emi,closing_balance])
                                df = pd.DataFrame(rows, columns=["Year", "EMI", "Closing Balance"])
                                st.table(df)
                            else:
                                st.error("Loan not approved. EMI exceeds your monthly salary.")
                        else:
                            st.error("Loan not approved. Requested amount exceeds the limit based on your ITR.")
        elif choice == "Loan Applicators":
            st.markdown(
                    "<h3 style='font-family:verdana ; color:#6EFD66; font-size:25px;'>Loan Applicators</h3>",
                    unsafe_allow_html=True)
            choice = st.radio("Type", ["Secured Loan", "Unsecured Loan"])
            if choice == "Secured Loan":
                st.markdown(
                    "<h3 style='font-family:verdana ; color:#6EFD66; font-size:20px;'>💰Secured Loan</h3>",
                    unsafe_allow_html=True)
                df = pd.read_csv("loan_sl.csv")
                if not df.empty:
                    df['Name'] = df["Name"].str.strip().str.capitalize()
                    st.dataframe(df)
            else:
                st.markdown(
                    "<h3 style='font-family:verdana ; color:#6EFD66; font-size:20px;'>💰Unsecured Loan</h3>",
                    unsafe_allow_html=True)
                df = pd.read_csv("loan_ul.csv")
                if not df.empty:
                    df['Name'] = df["Name"].str.strip().str.capitalize()
                    st.dataframe(df)
    elif choice == "FD" :
        st.markdown(
                    "<h3 style='font-family:verdana ; color:#FD2629; font-size:30px;'>Fixed Deposit</h3>",
                    unsafe_allow_html=True)
        
        name = st.text_input("Name")
        
        amount = st.number_input("Amount", min_value=0, step=10)
        age = st.number_input("Age", min_value=0, step=1)
        tenure = st.number_input("Tenure", min_value=0, step=1)

        compounding = 4
        if age<60:
            rate = 5
        else:
            rate = 6

        maturity = int(amount * (1+ rate/100/compounding) ** (tenure*compounding))
        
        if st.button("FD"):
            if len(name)>0:
                st.success(f"{name} your FD maturity amount after {tenure} years will be ₹{maturity}")     
            else:
                st.error("Name required")
    elif choice == "About":
        st.markdown(
            "<h3 style='font-family:Verdana; color:#4dd0e1; font-size:px;'>About</b> </h3>",
            unsafe_allow_html=True)
        st.write("This is the simple Bank Management System Simulation made with python. Here you can add your account, can see your balance, can withdraw or deposit your money, you can apply for loan or FD. Other options for bank will be added soon. Till that ...Enjoy!" \
        "\n\nMade with ❤️ by [Shashank Sul ](https://github.com/Shashank-creator7).\
        \nFor any queries or suggestions, feel free to reach out to me on Instagram.")
        st.markdown(
        """
        <a href="https://www.instagram.com/shashanksul_7/" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="30">
            shashanksul_7
        </p>
        """,
        unsafe_allow_html=True
        )
            
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        countdown = st.empty()
        for i in range(3, 0, -1):
            countdown.info(f'Logging out in {i} seconds')
            time.sleep(1)
        countdown.empty()
        st.rerun()

if choice == "Signup":
    if not st.session_state["logged_in"]:
        st.subheader("Signup")
        username = st.text_input("Enter username :" )
        if len(username)>0:

            with open ("baccounts.csv", "r") as file:
                reader = csv.DictReader(file)
                existing_username = [row["Username"] for row in reader]
                if username not in existing_username:
                    password = st.text_input("Enter password:")
                    if len(password)>0:
                        if st.button("Signup"):
                            with open("baccounts.csv", "a", newline="") as file:
                                fieldnames= ["Username", "Password"]
                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                if file.tell == 0:
                                    writer.writeheader()

                                writer.writerow({"Username":username, "Password":password})
                                st.success("Signup Successfully")
                    else:
                        st.info("Password must contain charecters")
                else:
                    st.info("Username already exists")
