import mysql.connector
from mysql.connector import Error

# -----------------------------
# Contains all functions that interact with the DB
# -----------------------------

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="10.138.20.133",
            port ="3306",
            user="DBManager",
            password="DBManager123*",
            database="CustomerManagementDB"
        )

        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
        
    except Error as e:
        print(f"Error: {e}")
        return None
    
def run_query(query, params=None):
    conn = connect_to_db()

    if not conn:
        return None

    try: 
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())

        # Only fetch if select query, otherwise return number of affected rows
        if query.strip().lower().startswith("select"):
            result = cursor.fetchall()
        else:
            result = cursor.rowcount 


        conn.commit()
        cursor.close()
        conn.close()
        print(result)
        return result
    
    except Error as e:
        print(f"Error: {e}")
        if conn.is_connected():
            conn.rollback()
        return None
    
# SQL Code to get Default Users, and Admin Users
query = ''' 
        SELECT UserID, UserName, UserEmail, PhoneNumber, TypeID 
        FROM Users
        WHERE TypeID IN (%s, %s)
        '''

# SQL Code to Change Status of User to Admin
UpdateQuery = '''
        UPDATE Users
        SET TypeID = %s
        WHERE UserID = %s;
        '''

# SQL Code to Delete Admin
DeleteQuery =   '''
                DELETE FROM Users
                WHERE UserID = %s;
                '''

AddUserQuery =  '''
                INSERT INTO Users (UserName, UserEmail, PhoneNumber, UserPassword, TypeID)
                VALUES (%s, %s, %s, %s, 4)
                '''

GetUsernamePasswordQuery =  '''
                            SELECT UserName, UserPassword, TypeID
                            FROM Users
                            WHERE UserName = %s
                            '''