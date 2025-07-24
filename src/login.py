# login.py (UPDATED)
from utils.handler import connect_db
import mysql.connector
import streamlit as st


def user_register(username, password):
    if not username or not password:
        st.error("Username and password required!")
        return False

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, password) VALUES (%s, %s)",
                       (username, password))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        st.error("Username already exists!")
        return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False
    finally:
        if conn.is_connected():
            conn.close()


def doctor_register(username, password):
    if not username or not password:
        st.error("Username and password required!")
        return False

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctors (name, password) VALUES (%s, %s)",
                       (username, password))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        st.error("Username already exists!")
        return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False
    finally:
        if conn.is_connected():
            conn.close()


def user_login(username, password):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE name=%s", (username,))
        result = cursor.fetchone()

        if result and password == result[0]:
            return True
        st.error("Invalid credentials!")
        return False
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return False
    finally:
        if conn.is_connected():
            conn.close()


def doctor_login(username, password):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM doctors WHERE name=%s", (username,))
        result = cursor.fetchone()

        if result and password == result[0]:
            return True
        st.error("Invalid credentials!")
        return False
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return False
    finally:
        if conn.is_connected():
            conn.close()

