import streamlit as st
import mysql.connector

from mysql.connector import Error

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="10.136.13.57",
            port = "3306",
            user="DBManager",
            password="DBManager123*",
            database="CustomerManagementDB"
        )

        if connection.is_connected():
            st.write("Successfully connected to the database")
            return connection
        
    except Error as e:
        st.write(f"Error: {e}")
        return None
    
def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

if __name__ == "__main__":
    connection = connect_to_db()

    if connection:
        query = "select * from Company;"
        result = execute_query(connection, query)

        for row in result:
                st.write(row)

        connection.close()


    st.write("Hello World")

# movie = st.text_input("What is your favorite movie?")

# if movie:
#     st.write(f"Your favorite movie is {movie}!")

# def main():
#     st.write("Hello World")

# if __name__ == "__main__":
#     main()