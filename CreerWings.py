import streamlit as st
import mysql.connector
import pandas as pd
import datetime



# ------------------------
# DATABASE CONNECTION
# ------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Anshu@44066",
        database="CareerWings"
    )

# ------------------------
# STREAMLIT APP
# ------------------------
st.title("CareerWings Dashboard")

# Sidebar Menu
menu = ["View All Careers", "Search by ID","Search by Qualifications","Career","Register User","View Users"]
choice = st.sidebar.selectbox("Menu", menu)
Admin_Password='admin123'
# ------------------------
# VIEW ALL CAREERS
# ------------------------
if choice == "View All Careers":
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT career_pin, careers, qualifications, avg_salary, job_security FROM careers")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        df = pd.DataFrame(rows, columns=["Career_Id", "Career", "Qualifications", "Avg_salary(INR)", "Job_Security"])
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data found in careers table.")

# ------------------------
# SEARCH BY CAREER ID
# ------------------------
elif choice == "Search by ID":
    st.subheader("🔍 Search Career by ID")
    search_id = st.text_input("Enter Career ID (e.g., 1001, 1010, etc.)")

    if st.button("Search"):
        if search_id:
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT career_pin, careers, qualifications, avg_salary, job_security FROM careers WHERE career_pin = %s"
            cursor.execute(query, (search_id,))
            rows = cursor.fetchall()
            conn.close()

            if rows:
                df = pd.DataFrame(rows, columns=["Career_Id", "Career", "Qualifications", "Avg_salary(INR)", "Job_Security"])
                st.dataframe(df, use_container_width=True)
            else:
                st.error(f"No career found with ID {search_id}")
        else:
            st.warning("Please enter a Career ID.")

elif choice=="Search by Qualifications":
    st.subheader(" Search Career by Qualification")
    search_id=st.text_input("Enter Qualification")

    if st.button("Search"):
        if search_id:
            conn=get_connection()
            cursor=conn.cursor()
            sql="select career_pin,careers,qualifications,avg_salary,job_security from careers where qualifications like %s"
            rows=cursor.execute(sql,("%"+search_id+"%",))
            rows=cursor.fetchall()
            conn.close()
            
            if rows:
                df=pd.DataFrame(rows, columns=["Career_Id", "Career", "Qualifications", "Avg_salary(INR)", "Job_Security"])
                st.dataframe(df,use_container_width=True)
            else:
                st.warning("Please enter any Qualification")
elif choice=="Career":
 st.subheader(" Search career ")     
 search_id=st.text_input("Enter Career You want to explore")

 if st.button("Search"):
    if search_id:
        conn=get_connection()
        cursor=conn.cursor()
        sql="select * from careers where careers like %s"
        cursor.execute(sql,("%"+search_id+"%",))
        rows=cursor.fetchall()
        conn.close()

        if  rows:
            df=pd.DataFrame(rows,columns=["Career_Id", "Career", "Qualifications", "Avg_salary(INR)", "Job_Security"]) 
            st.dataframe(df,use_container_width=True)
        else:
            st.warning("please enter any career")       
elif choice == "Register User":
    st.subheader("📝 Register New User")

    # Form fields
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email ID")
    qualification = st.text_input("Qualification")
    dob = st.date_input(
    "Date of Birth",
    min_value=datetime.date(1950, 1, 1),  # earliest selectable date
    max_value=datetime.date(2015,1,1)       # latest selectable date
)
    password=st.text_input("Password")
    if st.button("Register"):
        if name and phone and email:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO Login (Name, PhoneNo, EmailId, qualifications, dob,password) VALUES (%s, %s, %s, %s, %s,%s)"
            cursor.execute(sql, (name, phone, email, qualification, dob,password))
            conn.commit()
            conn.close()
            st.success(f"User {name} registered successfully ✅")
        else:
            st.warning("Please fill all required fields")

elif choice == "View Users":
    st.subheader("👥 Registered Users")
    password=st.text_input("Enter Password", type="password")
    if st.button("submit"):
        if(password==Admin_Password):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Name, PhoneNo, EmailId, qualifications, dob FROM Login")
            rows = cursor.fetchall()
            conn.close()

            if rows:
              df = pd.DataFrame(rows, columns=["Name", "Phone", "Email", "Qualification", "Date of Birth"])
        
              st.dataframe(df, use_container_width=True)
            else:
              st.info("No users registered yet.")
