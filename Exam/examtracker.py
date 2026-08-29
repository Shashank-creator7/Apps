import streamlit as st
import csv
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt



# Initialize user 
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "switched" not in st.session_state:
    st.session_state["switched"] = False
if "show_budget" not in st.session_state:
    st.session_state.show_budget = False

# User login
# ======================================================================================
menu = ["Login", "Signup", "Forgot Password", "About"]
choice = st.sidebar.selectbox("User Menu", menu )
if choice == "Login":
    if not st.session_state["logged_in"]:
        username = st.text_input("Username", key = "login_username")
        password = st.text_input("Password", type= "password", key= "login_password")

        st.button("Login")
        found = False
        with open ("acc.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"] == username and row["Password"] == password:
                    found = True
                    break
            
            if found:
                st.session_state["logged_in"] = True
                st.success("Login Successfully")

                            #  🔧 FIX: clear inputs after successful login
                
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
        "<h3 style='font-family:lato ; color:#4dd0e1; font-size:40px;'>💰 Exam Tracker</h3>",
        unsafe_allow_html=True)

    menu = ['Add chapter', 'Syllabus Dashboard', 'Exam Tracker', "Track",'Chapter status', 'Marksheet and Performance', 'Analytics']
    choice = st.sidebar.selectbox("App Menu", menu)

    if choice == "Add chapter":
        subject = st.selectbox("Subject", ["Physics", "Chemistry", "Maths"])
        name = st.text_input("Name")
        grade = st.selectbox("Class", ['11', '12'])
        if st.button("Add"):
            with open ("Syllabus.csv", "a", newline='') as file:
                fieldname = ["Subject","Chapter" ,"Class"]
                writer = csv.DictWriter(file, fieldnames=fieldname)
                if file.tell == 0:
                    writer.writeheader()
                writer.writerow({"Subject":subject,"Chapter":name, "Class":grade})
            st.success("Chapter added successfully")
    if choice == 'Syllabus Dashboard':
        st.markdown(
            "<h3 style='font-family:verdana ; color:#6EFD66; font-size:25px;'>Syllabus Dashboard</h3>",unsafe_allow_html=True)
        choice = st.radio("Subject:",['Physics','Chemistry','Maths',"All"])
        


        if choice == 'Physics':
            df = pd.read_csv("dashboard.csv")
            if not df.empty:
                df["Chapters"] = df["Chapters"].str.strip().str.capitalize()
                st.dataframe(df)
        elif choice == "All":
            df = pd.read_csv("dashboard.csv")
            st.dataframe(df)
            df = pd.read_csv("dashboard.csv")

            df["StatusNumeric"] = df["Status"].map({"Complete": 1, "Incomplete": 0})

            # Group by Subject → calculate completion percentage
            grouped = df.groupby("Subject").agg(
                Completed=("StatusNumeric", "sum"),
                Total=("StatusNumeric", "count")
            ).reset_index()

            grouped["CompletionPercent"] = (grouped["Completed"] / grouped["Total"]) * 100

            # Pie chart data
            categories = grouped["Subject"]
            values = grouped["CompletionPercent"]

            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures circle
            st.pyplot(fig)
    if choice == "Track":
        df = pd.read_csv("syllabus.csv")
        df_sorted = df.sort_values(by="Subject")
        # updated_status = []
        # for i , row in track_df.iterrows():
        #     checked = st.checkbox(
        #         f"{row['Subject']} - {row['Chapter']}", 
        #         value=(row['Status'] == "Complete"),
        #         key=f"{row['Subject']}_{row['Chapter']}"
        #     )
        # if checked:
        #     updated_status.append("Complete")
        # else:
        #     updated_status.append("Incomplete")

# Add updated status back to DataFrame
        # df["Status"] = updated_status
        st.dataframe(df_sorted)
    if choice == "Chapter status":
        subject = st.selectbox("Subject", ["Physics", "Chemistry", "Maths"])
        chapter = st.text_input("Chapter")
        grade = st.selectbox("Class", ["11","12"])
        status = st.selectbox("Status", ["Completed","Incomplete"])
        if st.button("Update"):
            with open ("dashboard.csv",'a',newline="") as file:
                fieldname = ["Subject", "Chapter", "Class", 'Status']
                writer = csv.DictWriter(file, fieldnames=fieldname)
                if file.tell == 0:
                    writer.writeheader()
                writer.writerow({'Subject':subject, 'Chapter':chapter, 'Class':grade, "Status":status})
            st.success("Status Updated")
    